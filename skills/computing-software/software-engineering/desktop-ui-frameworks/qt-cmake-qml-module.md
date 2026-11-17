---
id: computing-software.software-engineering.desktop-ui-frameworks.qt-cmake-qml-module
name: qt-cmake-qml-module
category: computing-software
field: software-engineering
product: desktop-ui-frameworks
tags: [qt-cmake-qml-module, qt-cmake, qt, qt6, cmake, desktop-ui-frameworks]
level: practitioner
status: docs-checked
description: "Package QML files and C++ types with qt_add_qml_module and load via the module URI."
sources:
  - https://doc.qt.io/qt-6/qt-add-qml-module.html
  - https://doc.qt.io/qt-6/qqmlapplicationengine.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# qt_add_qml_module

**Goal:** QML shipped in the executable.

```cmake
qt_add_qml_module(app
    URI Demo
    VERSION 1.0
    QML_FILES Main.qml Page.qml
    SOURCES backend.h backend.cpp)
# main.cpp
QQmlApplicationEngine engine;
engine.loadFromModule("Demo", "Main");   // since Qt 6.5
```

**Gotcha:** loadFromModule needs Qt 6.5 or newer. Files are compiled in as resources only when listed in QML_FILES (other files go in RESOURCES), under RESOURCE_PREFIX plus the target path; if the QTP0001 policy is NEW the prefix defaults to /qt/qml/.

## Checked
2026-11-03. Confirmed in the qt_add_qml_module and QQmlApplicationEngine pages: URI, VERSION, QML_FILES, SOURCES, RESOURCES and RESOURCE_PREFIX arguments, loadFromModule(uri, typeName) since 6.5, QTP0001 default prefix. Removed: the pre-6.5 qrc:/Demo/Main.qml URL (the real path depends on the resource prefix).

Method: documentation only; no commands were run.

## Verify
- The app starts without any QML files on disk beside the exe.
