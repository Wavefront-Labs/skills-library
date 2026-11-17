---
id: computing-software.software-engineering.desktop-ui-frameworks.desktop-resource-files-per-framework
name: desktop-resource-files-per-framework
category: computing-software
field: software-engineering
product: desktop-ui-frameworks
tags: [desktop-resource-files-per-framework, desktop-localisation, localisation, i18n, l10n, desktop-ui-frameworks]
level: practitioner
status: draft
description: "Use the native resource format of each stack: resx, ts/qm, JSON catalogs, fluent."
sources:
  - https://learn.microsoft.com/en-us/dotnet/core/extensions/localization
  - https://www.electronjs.org/docs/latest/api/app
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Localisation resources per framework

**Goal:** right tooling for each framework.

```text
WPF/WinUI: Strings.resx + Strings.de.resx, x:Uid in WinUI (.resw per language)
Qt: tr()/qsTr(), .ts via lupdate, .qm via lrelease
Electron/Tauri: JSON/ICU catalogs with i18next or Fluent; app.getLocale() / navigator.language; Tauri: plugin-os locale()
Rust: fluent-rs or gettext-rs
```

**Gotcha:** Concatenated sentences and hard-coded plurals break translation; use ICU or ordinal/plural rules per language.

## Verify
- A pseudo-locale build shows no untranslated or truncated strings.
