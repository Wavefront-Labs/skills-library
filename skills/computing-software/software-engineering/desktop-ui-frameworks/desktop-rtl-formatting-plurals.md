---
id: computing-software.software-engineering.desktop-ui-frameworks.desktop-rtl-formatting-plurals
name: desktop-rtl-formatting-plurals
category: computing-software
field: software-engineering
product: desktop-ui-frameworks
tags: [desktop-rtl-formatting-plurals, desktop-localisation, localisation, i18n, l10n, desktop-ui-frameworks]
level: practitioner
status: draft
description: "Support right-to-left layouts, locale formats and plural rules."
sources:
  - https://learn.microsoft.com/en-us/dotnet/core/extensions/localization
  - https://www.electronjs.org/docs/latest/api/app
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# RTL, number and date formatting

**Goal:** correct behaviour in ar, he, de, ja.

```text
WPF: FlowDirection=RightToLeft; Qt: QGuiApplication::setLayoutDirection(Qt::RightToLeft)
Web: <html dir="rtl">, CSS logical properties (margin-inline-start)
Formats: Intl.NumberFormat / DateTimeFormat; .NET CultureInfo; QLocale::toString
Plurals: Intl.PluralRules; Qt %n in tr(); resx needs separate keys
```

**Gotcha:** Do not mirror icons that show real-world direction (media play, clocks); mirror only directional arrows and layout.

## Verify
- The UI mirrors correctly with Arabic pseudo-locale.
