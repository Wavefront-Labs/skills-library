---
id: computing-software.software-engineering.objective-c.localizable-strings
name: localizable-strings
category: computing-software
field: software-engineering
product: objective-c
tags: [objective-c, objc-localization, localizable-strings]
level: practitioner
status: draft
description: "Localize user-visible text with NSLocalizedString, Localizable.strings, stringsdict plurals, genstrings and string catalogs."
sources:
  - https://developer.apple.com/documentation/foundation
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Localization
**Goal:** externalize UI text for translation.

```objc
self.title = NSLocalizedString(@"settings.title", @"Title of the settings screen");
NSString *msg = [NSString stringWithFormat:NSLocalizedString(@"items.count.format", @"Items count"), (long)count];
```
```
/* Localizable.strings (en.lproj) */
"settings.title" = "Settings";
```
- Macros: `NSLocalizedString(key, comment)`, `NSLocalizedStringFromTable`, `NSLocalizedStringFromTableInBundle`; the comment helps translators.
- `genstrings -o en.lproj Sources/*.m` extracts keys from the macros; Xcode export/import localizations (`xcodebuild -exportLocalizations`) creates XLIFF.
- Plurals use `Localizable.stringsdict` with `NSStringLocalizedFormatKey` and `NSStringPluralRuleType`; do not build plurals with `if count == 1`.
- Xcode 15 and later support String Catalogs (`.xcstrings`) which manage keys, plurals and translation state in one file.
- Format numbers/dates with formatters respecting the locale; use positional specifiers (`%1$@`) when order differs between languages.
- Support right-to-left via leading/trailing constraints.
- Test with scheme options: App Language and "Show non-localized strings".

## Gotchas
- Using a variable as the key defeats `genstrings`.
- Concatenating translated fragments breaks grammar in other languages.

## Self-check
Run with the pseudo-language scheme option and look for untranslated or truncated strings.
