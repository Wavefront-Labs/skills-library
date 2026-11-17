---
id: computing-software.game-programming.godot.localization-with-translationserver
name: localization-with-translationserver
category: computing-software
field: game-programming
product: godot
tags: [godot, godot-ui, translationserver, csv-translations, po-files, game-programming]
level: practitioner
status: docs-checked
description: "Localise Godot games: CSV and gettext PO translations, tr() and auto-translate, TranslationServer locale switching, pluralisation, fonts for scripts and pseudolocalisation."
sources: ["https://docs.godotengine.org/en/stable/tutorials/i18n/internationalizing_games.html", "https://docs.godotengine.org/en/stable/tutorials/i18n/localization_using_gettext.html", "https://docs.godotengine.org/en/stable/classes/class_node.html", "https://docs.godotengine.org/en/stable/classes/class_translationserver.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Localisation with TranslationServer

**Goal:** every player-facing string translatable, switchable at runtime, with the right fonts and
plural forms.

## Formats
- **CSV**: spreadsheet-style translations imported by the editor (see the Importing translations page).
- **gettext PO/POT**: tooling such as Poedit, Transifex and Weblate, plus context and plurals. Generate the
  POT via Project > Project Settings > Localization > Template Generation (Add the scenes and scripts
  to scan; it picks up `tr()`, `tr_n()`, `atr()`, `atr_n()` calls).
Add translation files in Project Settings > Localization > Translations (locale is inferred from the
`Language:` header of a PO/MO file).

## In code and scenes
- Nodes have `auto_translate_mode` (`AUTO_TRANSLATE_MODE_INHERIT` default, `ALWAYS`, `DISABLED`); Controls
  translate their text by default. Put the key or source string in `text`.
- Scripts: `tr("MENU_PLAY")`, plurals `tr_n("ONE_COIN", "N_COINS", n) % n`, context
  `tr("Open", "door")`.
- Format after translating: `tr("HP_LEFT").format({"hp": hp})` — don't concatenate sentence fragments.

## Switching locale
```gdscript
TranslationServer.set_locale("fr")
# Controls update automatically; for strings built in code, listen:
func _notification(what):
    if what == NOTIFICATION_TRANSLATION_CHANGED: _refresh_texts()
```
Default to the player's language from `OS.get_locale_language()`; if unavailable Godot uses the
Project Settings > General > Internationalization > Locale > Fallback, or `en` if empty.

## Fonts and layout
- Use the font fallback system to cover other scripts; `layout_direction` on Controls overrides mirroring for RTL.
- Test longer translations in containers with autowrap and minimum sizes.

## Testing
- Enable pseudolocalization in the advanced Project Settings (longer strings, accented characters,
  placeholders kept) to find untranslated and clipped text.
- `godot --language fr` / `TranslationServer.set_locale` in a debug menu.

## Gotchas
- Keys vs source text: keys are stable but unreadable in scenes; source-text-as-key breaks when
  English copy changes. Pick one per project.
- Remapping assets per locale (voice audio, textures): Localization > Remaps.

## Verify
- [ ] Pseudolocale run shows no untranslated or clipped strings.
- [ ] Switching locale at runtime updates menus and HUD without restart.

## Checked
2026-10-28, Godot docs `stable` (latest release tag 4.7.2-stable). Confirmed from the Internationalizing games and Localization using gettext tutorials and the Node and TranslationServer class pages: Template Generation, Localization > Translations, Remaps, tr()/tr_n() usage, auto_translate_mode values, NOTIFICATION_TRANSLATION_CHANGED, OS.get_locale_language(), fallback locale, pseudolocalization in advanced settings, --language, layout_direction. Fixed: POT Generation is Template Generation; Crowdin replaced by Transifex (the docs name Transifex and Weblate); auto_translate_mode belongs to Node, no 4.3+ gate stated. Removed: CSV column layout and .translation detail, HarfBuzz, 30% longer strings, brackets in pseudolocalization, Resource property gotcha, ConfigFile advice.
Method: documentation only; no commands were run.
