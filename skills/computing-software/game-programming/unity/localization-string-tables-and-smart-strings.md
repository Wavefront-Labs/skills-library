---
id: computing-software.game-programming.unity.localization-string-tables-and-smart-strings
name: localization-string-tables-and-smart-strings
category: computing-software
field: game-programming
product: unity
tags: [unity, unity-localization, localization, string-tables, smart-strings, i18n, game-programming]
level: practitioner
status: docs-checked
description: "Unity Localization string tables and Smart Strings: table collections, preloading, selectors, formatters, arguments, nesting, locale formatting, character sets."
sources: ["https://docs.unity3d.com/Packages/com.unity.localization@1.5/manual/Smart/SmartStrings.html", "https://docs.unity3d.com/Packages/com.unity.localization@1.5/manual/StringTables.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Localization: string tables and Smart Strings

**Goal:** every user-facing string comes from a table, with plurals and variables handled per language. Localization
package 1.5 docs.

## String tables
- A String Table returns a localized string for a Key and a Locale. Each row holds a Key Id and a string entry for one
  Locale; an entry is a static string or a tokenized string for Smart Strings or `String.Format`. Unlike Asset Tables they
  need no additional loading step for their content.
- A **String Table Collection** is an Editor-only asset. Creating one makes a collection asset, a String Table asset per
  Locale, and one Shared Table Data asset that stores key names, Ids and Shared Metadata. Removing a table from the
  collection removes it from the Localization system but keeps its data.
- Extensions (Editor-only) attach extra data or importers/exporters; derive from `CollectionExtension` and add
  `StringTableCollectionExtensionAttribute`.
- **Preloading:** by default tables are not preloaded, so the first request loads the table asynchronously and the string
  may not be immediately available. Enable the **Preload** toggle in the Localization Tables window to have tables ready.
- Metadata: table-level via the button at the right of the column header; entry-level via the (⋮) button. Shared Metadata
  lives in Shared Table Data; locale-specific metadata lives in each table.

## Smart Strings
Smart Strings are a modified SmartFormat library, an alternative to `String.Format` with pluralization, gender
conjugation, lists and conditional logic, and named placeholders. Mark an entry smart through the (⋮) menu > Smart Format
in the Localization Tables window, the Smart field of the Localized String editor, or `entry.IsSmart = true` in an Editor
script (call `EditorUtility.SetDirty` on the table afterwards).

- A placeholder can have selectors, a formatter name, formatter options and a format.
- **Selectors** use dot notation: `{gameObject.name}`, `{1.gameObject.name}` (index 1 then Reflection). No index means
  argument 0. Sources are tried in order until one handles the selector, so order changes results (a dictionary key
  `Count` can resolve to a Reflection `Count` property if Reflection comes first).
- **Multiple arguments:** `localizedString.Arguments = new object[] { dict1, dict2 };` then `{0.Name}`, `{1.City}`;
  `{0:{Name}}` is the nested scope form. Persistent Variables let you define arguments without scripting.
- **Nesting:** `{User:{Name} ({Age})}`; inner scopes can reach outer scopes; an empty placeholder is the current value.
- **Formatters:** explicit by name, for example `{0:plural:1 Apple| Apples}` or `{0:p:...}`; implicit when no name is given,
  tried in list order. Explicit is preferred to avoid conflicts. Options go in brackets:
  `{0:choose(1|2|3):one|two|three}`. Custom formatters derive from `FormatterBase`.
- **Locale-aware formatting** uses the Locale of the entry's table: `{0:N}` gives 123,456,789.12 in English and
  123.456.789.12 in Spanish.

## Character sets
Unity can compute the distinct characters used by a String Table (including literal text in Smart Strings, ignoring
placeholders) to build a font atlas subset, for example for TextMeshPro Font Asset Creator. Export from the String Table
window, String Table Collection window or the Localization Tables window, or call `GenerateCharacterSet`.

## Checked
Date: 2026-11-07.
Read in full: Localization 1.5 "Smart Strings" and "String Tables" manual pages, including every code block. The package
index page (about 1,200 characters, a landing page) was dropped from sources.
Removed as unconfirmed: package install and Project Settings steps, Locale Generator and Startup Locale Selectors, Asset
Table setup, `LocalizeStringEvent` wiring and the `StringChanged`/`RefreshString` snippet, the exact `plural` syntax with
`|` forms for Russian, `{gender:choose(m|f):He|She}`, `LocalizationSettings.SelectedLocale`, `InitializationOperation`,
CSV/XLIFF/Google Sheets workflow, Pseudo-Locale, font fallback and Addressables build gotchas, and the invented Verify
checklist.
Method: documentation only; no commands were run.
