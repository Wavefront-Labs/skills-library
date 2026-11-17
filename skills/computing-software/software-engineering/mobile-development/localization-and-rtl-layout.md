---
id: computing-software.software-engineering.mobile-development.localization-and-rtl-layout
name: localization-and-rtl-layout
category: computing-software
field: software-engineering
product: mobile-development
tags: [mobile-development, mobile-ui, localization, rtl-layout, string-catalogs, plurals, internationalization]
level: practitioner
status: draft
description: "Localize Android and iOS apps: string resources and String Catalogs, plurals and formatting, per-app language, RTL mirroring, pseudolocales and translation workflows."
sources:
  - https://developer.android.com/guide/topics/resources/localization
  - https://developer.android.com/guide/topics/resources/app-languages
  - https://developer.apple.com/documentation/xcode/localizing-and-varying-text-with-a-string-catalog
  - https://developer.apple.com/design/human-interface-guidelines/right-to-left
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Localization and RTL layout

**Goal:** the app reads naturally in every supported language, handles plurals, dates and numbers per locale, and mirrors correctly for Arabic and Hebrew.

## 1. Externalise every user-visible string
Android `res/values/strings.xml`, `res/values-de/strings.xml`:
```xml
<string name="order_title">Order %1$s</string>
<plurals name="items_count">
    <item quantity="one">%d item</item>
    <item quantity="other">%d items</item>
</plurals>
```
```kotlin
stringResource(R.string.order_title, order.id)
pluralStringResource(R.plurals.items_count, n, n)
```
iOS String Catalogs (`Localizable.xcstrings`, Xcode 15+): SwiftUI `Text("Order \(id)")` literals are extracted automatically at build; plural variants are configured per language in the catalog.
```swift
Text("^[\(count) item](inflect: true)")              // automatic grammar agreement (some languages)
String(localized: "order.title", defaultValue: "Order \(id)", comment: "Title of order detail screen")
```
Always give translators context comments; never concatenate fragments ("You have " + n + " items") because word order differs.

## 2. Plurals and formatting
- Languages have up to six plural categories (Arabic: zero, one, two, few, many, other); never `if n == 1`.
- Dates/numbers/currency via locale-aware formatters: `DateTimeFormatter.ofLocalizedDate`, `NumberFormat.getCurrencyInstance(locale)`, Swift `.formatted(.currency(code:))`, `Date.FormatStyle`.
- Sorting and case: `Collator`/`localizedStandardCompare`.

## 3. Per-app language
Android 13+: `AppCompatDelegate.setApplicationLocales(LocaleListCompat.forLanguageTags("de"))` and declare `android:localeConfig` (or `generateLocaleConfig = true` in AGP). iOS: users choose per-app language in Settings; declare supported localizations in the project.

## 4. RTL
- Android: `android:supportsRtl="true"`, use `start`/`end` (never `left`/`right`) in layouts and paddings; Compose uses start/end by default and mirrors automatically. Mirror directional icons with `autoMirrored = true`.
- iOS: leading/trailing constraints, SwiftUI mirrors automatically; flip directional images (`.flipsForRightToLeftLayoutDirection(true)` or asset "Mirrors" setting). Do not mirror media playback controls, clocks, or logos.
- Bidirectional text: wrap embedded LTR content (phone numbers, codes) with Unicode isolates (`BidiFormatter` on Android).

## 5. Testing
- Pseudolocales: Android `en-XA` (accented, expanded text) and `ar-XB` (RTL) enabled via `pseudoLocalesEnabled true` in debug builds; Xcode scheme options for double-length pseudolanguage and right-to-left pseudolanguage.
- Screenshot tests per locale catch truncation and overlap; German and Finnish expand text 30%+.

## 6. Workflow
Export to XLIFF (`xcodebuild -exportLocalizations`) or sync strings with a TMS (Crowdin, Lokalise, Phrase) in CI; lint for missing translations (`MissingTranslation` lint on Android, catalog state "Needs Review" on iOS).

## Gotchas
- Hard-coded strings in code or images slip through; enable lint `HardcodedText` and review.
- Server-provided text must also be localized (send `Accept-Language`).
- Formatting with `%d` in a format string expecting localized digits differs across locales; use the formatter APIs.

## Verify
- The app runs in pseudolocales without truncation or untranslated strings, Arabic layout mirrors correctly, and plural strings render properly for 0, 1, 2, 5 and 11 in Arabic/Russian/Polish.
