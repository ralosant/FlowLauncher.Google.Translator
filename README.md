# FlowLauncher.Google.Translator

This plugin lets you translate text using [Google Translate](https://translate.google.com/) and copy results to the clipboard in [Flow Launcher](https://www.flowlauncher.com/).

## How to use it

1. Install this plugin via `pm install Google Translate`
2. Usage examples:
  - `tr <text>`: Auto-detects the source language and translates to your default language (configured in settings, default is English `en`).
    - Example: `tr ciao come va`
  - `tr :<to_lang> <text>`: Auto-detects the source language and translates to the specified target language.
    - Example: `tr :es hello my friend`
    - Example: `tr :it good morning`
  - `tr <from_lang>:<to_lang> <text>`: Translates from a specified source language to a target language.
    - Example: `tr en:de how are you?`
  - `tr <from_lang>: <text>`: Translates from a specified source language to the default language.
    - Example: `tr es: buenos días`

Select a result or press Enter to copy the translation to your clipboard.

## Settings

You can customize the default target language (`to_lang`, e.g. `it`, `en`, `es`, `fr`, `de`, `ja`, etc.) in the Flow Launcher plugin settings.

---

This plugin is a modified port of [Wox.Plugin.GoogleTranslate](https://github.com/laercioskt/Wox.Plugin.GoogleTranslate) created by [laercioskt](https://github.com/laercioskt).
