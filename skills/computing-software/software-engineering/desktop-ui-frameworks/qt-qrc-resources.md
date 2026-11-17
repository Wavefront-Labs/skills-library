---
id: computing-software.software-engineering.desktop-ui-frameworks.qt-qrc-resources
name: qt-qrc-resources
category: computing-software
field: software-engineering
product: desktop-ui-frameworks
tags: [qt-qrc-resources, qt-resources-i18n, qt, qt6, i18n, desktop-ui-frameworks]
level: practitioner
status: docs-checked
description: "Embed images, QML and data in the binary with qrc and qt_add_resources."
sources:
  - https://doc.qt.io/qt-6/resources.html
  - https://doc.qt.io/qt-6/qt-add-resources.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Qt resource system (.qrc)

**Goal:** single-binary assets.

```cmake
# a .qrc XML file added as a source needs CMAKE_AUTORCC ON; qt_add_resources needs no .qrc
qt_add_resources(app "assets" PREFIX "/" FILES icons/save.svg data/defaults.json)
# C++
QIcon icon(":/icons/save.svg");
QFile f(":/data/defaults.json"); f.open(QIODevice::ReadOnly);
```

**Gotcha:** By default rcc embeds files as C++ arrays, which can be a problem for large resources; rcc -binary produces an .rcc archive that can be loaded at runtime instead.

## Checked
2026-11-03. Confirmed in the Qt Resource System and qt_add_resources pages: AUTORCC for .qrc sources, qt_add_resources(target name PREFIX FILES ...), :/ paths composed of prefix plus file path, C++-array embedding and rcc -binary. Removed: the read-only claim and the .qrc XML example (not shown in the pages).

Method: documentation only; no commands were run.

## Verify
- QFile::exists on the :/ path is true at runtime.
