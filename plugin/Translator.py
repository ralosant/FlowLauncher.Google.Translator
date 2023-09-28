# -*- coding: utf-8 -*-
"""
Google Translate in Flowlauncher.

This plugin allows translation using Google Translate and copy it.
"""

from flowlauncher import FlowLauncher, FlowLauncherAPI
import urllib.parse
import urllib.request
import html
import re
import textwrap
import subprocess


def translate(to_translate, to_language="auto", from_language="auto", wrap_len="200"):
    """Get translated query from Google translate."""
    agent = {'User-Agent': "Edge, Brave, Firefox, Chrome, Opera"}
    base_link = "https://translate.google.com/m?tl=%s&sl=%s&q=%s"
    to_translate = urllib.parse.quote(to_translate)
    link = base_link % (to_language, from_language, to_translate)
    request = urllib.request.Request(link, headers=agent)
    raw_data = urllib.request.urlopen(request).read()
    data = raw_data.decode("utf-8")
    expr = r'class="result-container">(.*?)<'
    re_result = re.findall(expr, data)
    if len(re_result) == 0:
        result = ""
    else:
        result = html.unescape(re_result[0])
    return "\n".join(textwrap.wrap(result, int(wrap_len) if wrap_len.isdigit() else 200))


def copy2clip(txt):
    """Put translation into clipboard."""
    cmd = 'echo '+txt.strip()+'|clip'
    return subprocess.check_call(cmd, shell=True)


class GoogTranslate(FlowLauncher):

    def query(self, query):
        results = []
        try:
            urllib.request.urlopen("https://translate.google.com/")
            # Online or Normal workflow
            if len(query.strip()) == 0:
                results.append({
                    "Title": ":es text to translate",
                    "SubTitle": "use: 'tr :es your expresion' to translate from auto-detected to Spanish",
                    "IcoPath": "Images/gt.png", "ContextData": "ctxData"})
            else:
                from_language = "auto"
                to_language = "em"
                parts = query.split(" ", 1)

                if len(parts) > 1:
                    languages, query = parts
                    lang_parts = languages.split(":")

                    if len(lang_parts) > 1:
                        from_language, to_language_candidate = lang_parts
                        if from_language:
                            from_language = from_language.strip()
                        if to_language_candidate:
                            to_language = to_language_candidate.strip()
                    elif len(lang_parts) == 1:
                        to_language = lang_parts[0].strip()
                else:
                    query = query.strip()

                if len(query.strip()) == 0:
                    results.append({
                        "Title": ":es text to translate",
                        "SubTitle": "use: 'tr :es your expresion' to translate from auto-detected to Spanish",
                        "IcoPath": "Images/gt.png", "ContextData": "ctxData"})
                else:
                    translation = translate(
                        query.strip(), to_language, from_language, "200")

                    results.append({
                        "Title": to_language + ": " + translation,
                        "SubTitle": from_language + ": " + query,
                        "IcoPath": "Images/gt.png",
                        "ContextData": "ctxData",
                        "JsonRPCAction": {"method": "copy", "parameters": [translation], }})
        except:
            # Offline or input error
            results.append({
                "Title": "Invalid Notation or No Internet Connection",
                "SubTitle": "Please, Verify and try again",
                "IcoPath": "Images/gt.png", "ContextData": "ctxData"})

        return results

    def copy(self, ans):
        """Copy translation to clipboard."""
        FlowLauncherAPI.show_msg("Copied to clipboard", copy2clip(ans))


if __name__ == "__main__":
    GoogTranslate()
