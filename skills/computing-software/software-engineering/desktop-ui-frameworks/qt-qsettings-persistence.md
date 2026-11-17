---
id: computing-software.software-engineering.desktop-ui-frameworks.qt-qsettings-persistence
name: qt-qsettings-persistence
category: computing-software
field: software-engineering
product: desktop-ui-frameworks
tags: [qt-qsettings-persistence, qt-widgets-basics, qt, qt6, qt-widgets, desktop-ui-frameworks]
level: practitioner
status: docs-checked
description: "Store user preferences with QSettings using organisation and application names."
sources:
  - https://doc.qt.io/qt-6/qsettings.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# QSettings persistence

**Goal:** persistent window state and options.

```cpp
QCoreApplication::setOrganizationName("Acme");
QCoreApplication::setApplicationName("Editor");
QSettings s;                                   // registry on Windows, property list on macOS, INI files on Unix
s.setValue("geometry", saveGeometry());
restoreGeometry(s.value("geometry").toByteArray());
s.beginGroup("net"); s.setValue("proxy", url); s.endGroup();
// portable: QSettings s("settings.ini", QSettings::IniFormat);
```

**Gotcha:** Set the organisation and application names before relying on the default constructor. INI files lose the number/string distinction, so values come back as strings: convert with toInt() or toDouble().

## Checked
2026-11-03. Confirmed in the QSettings page: registry on Windows, property lists on macOS and iOS, INI on Unix, default constructor after setOrganizationName/setApplicationName, saveGeometry example, IniFormat, string values from INI. Removed: the QSettings default-constructor-has-no-location claim and the unrelated layout.html source.

Method: documentation only; no commands were run.

## Verify
- Restart restores window position, and settings live in the expected platform store.
