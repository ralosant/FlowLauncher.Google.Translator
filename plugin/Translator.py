# -*- coding: utf-8 -*-
"""
Google Translate in Flowlauncher.

This plugin allows translation using Google Translate and copy it.
"""

from functools import lru_cache
import html
import json
import subprocess
import urllib.error
import urllib.parse
import urllib.request

from flowlauncher import FlowLauncher, FlowLauncherAPI


def is_lang_code(code):
    """Check if a string looks like an ISO 639-1 language code or locale."""
    if not code:
        return True
    code = code.lower()
    if code == "auto":
        return True
    if len(code) in (2, 3) and code.isalpha():
        return True
    if len(code) == 5 and code[:2].isalpha() and code[2] in ("-", "_") and code[3:].isalpha():
        return True
    return False


def is_valid_lang_spec(spec):
    """Check if the first token is a valid language specification with colon."""
    if ":" not in spec:
        return False
    parts = spec.split(":", 1)
    src, dst = parts[0].strip(), parts[1].strip()
    if not src and not dst:
        return False
    return is_lang_code(src) and is_lang_code(dst)


@lru_cache(maxsize=256)
def translate(to_translate, to_language="en", from_language="auto"):
    """Get translated query from Google Translate single API."""
    params = urllib.parse.urlencode({
        "client": "gtx",
        "sl": from_language,
        "tl": to_language,
        "dt": "t",
        "q": to_translate
    })
    url = f"https://translate.googleapis.com/translate_a/single?{params}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=5) as resp:
        raw_data = resp.read().decode("utf-8")
        data = json.loads(raw_data)

    sentences = data[0] if data and len(data) > 0 and data[0] else []
    translated_text = "".join(s[0] for s in sentences if s and s[0])

    detected_lang = from_language
    if len(data) > 2 and data[2]:
        detected_lang = data[2]

    return html.unescape(translated_text), detected_lang


def copy2clip(txt):
    """Put translation into clipboard safely using Windows clip command with UTF-16."""
    subprocess.run(["clip"], input=txt.strip().encode("utf-16le"), check=True)


class GoogTranslate(FlowLauncher):

    @property
    def settings(self):
        if hasattr(self, "rpc_request") and isinstance(self.rpc_request, dict):
            return self.rpc_request.get("settings", {})
        return {}

    def get_default_to_language(self):
        to_lang = self.settings.get("to_lang", "en")
        if to_lang and isinstance(to_lang, str) and to_lang.strip():
            return to_lang.strip()
        return "en"

    def query(self, query):
        results = []
        raw_query = query.strip()
        default_to_lang = self.get_default_to_language()

        if not raw_query:
            results.append({
                "Title": "Type text to translate",
                "SubTitle": f"Use ':target text' (e.g. :it hello) or 'source:target text'. Default target: {default_to_lang}",
                "IcoPath": "images/gt.png",
                "ContextData": "ctxData"
            })
            return results

        parts = raw_query.split(" ", 1)
        first_word = parts[0]
        from_language = "auto"
        to_language = default_to_lang
        text_to_translate = raw_query

        if is_valid_lang_spec(first_word):
            lang_parts = first_word.split(":", 1)
            src = lang_parts[0].strip()
            dst = lang_parts[1].strip()
            if src:
                from_language = src
            if dst:
                to_language = dst

            if len(parts) > 1 and parts[1].strip():
                text_to_translate = parts[1].strip()
            else:
                results.append({
                    "Title": f"Translate {from_language} -> {to_language}",
                    "SubTitle": "Type the text to translate...",
                    "IcoPath": "images/gt.png",
                    "ContextData": "ctxData"
                })
                return results

        try:
            translation, detected_lang = translate(
                text_to_translate, to_language, from_language
            )

            if not translation:
                results.append({
                    "Title": "No translation found",
                    "SubTitle": f"{detected_lang} -> {to_language}: {text_to_translate}",
                    "IcoPath": "images/gt.png",
                    "ContextData": "ctxData"
                })
            else:
                results.append({
                    "Title": f"{to_language}: {translation}",
                    "SubTitle": f"{detected_lang} -> {to_language}: {text_to_translate}",
                    "IcoPath": "images/gt.png",
                    "ContextData": "ctxData",
                    "JsonRPCAction": {
                        "method": "copy",
                        "parameters": [translation]
                    }
                })
        except urllib.error.URLError as e:
            results.append({
                "Title": "Network Error",
                "SubTitle": f"Could not connect to Google Translate: {getattr(e, 'reason', e)}",
                "IcoPath": "images/gt.png",
                "ContextData": "ctxData"
            })
        except Exception as e:
            results.append({
                "Title": "Translation Error",
                "SubTitle": f"{e}",
                "IcoPath": "images/gt.png",
                "ContextData": "ctxData"
            })

        return results

    def copy(self, ans):
        """Copy translation to clipboard."""
        try:
            copy2clip(ans)
            FlowLauncherAPI.show_msg("Copied to clipboard", ans)
        except Exception as e:
            FlowLauncherAPI.show_msg("Clipboard Error", str(e))


if __name__ == "__main__":
    GoogTranslate()

