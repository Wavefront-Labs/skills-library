---
id: computing-software.software-engineering.desktop-ui-frameworks.qt-cmake-autogen
name: qt-cmake-autogen
category: computing-software
field: software-engineering
product: desktop-ui-frameworks
tags: [qt-cmake-autogen, qt-cmake, qt, qt6, cmake, desktop-ui-frameworks]
level: practitioner
status: docs-checked
description: "Use AUTOMOC and AUTOUIC from qt_standard_project_setup and enable AUTORCC yourself for .qrc files."
sources:
  - https://doc.qt.io/qt-6/qt-standard-project-setup.html
  - https://doc.qt.io/qt-6/cmake-get-started.html
  - https://doc.qt.io/qt-6/resources.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# AUTOMOC AUTOUIC AUTORCC

**Goal:** Q_OBJECT classes, .ui and .qrc handled automatically.

```cmake
qt_standard_project_setup()            # sets CMAKE_AUTOMOC and CMAKE_AUTOUIC to ON (if not already defined)
set(CMAKE_AUTORCC ON)                  # not set by qt_standard_project_setup
qt_add_executable(app main.cpp widget.h widget.cpp widget.ui res.qrc)
```

**Gotcha:** qt_standard_project_setup() enables AUTOMOC and AUTOUIC only; a .qrc file added as a source is embedded only when CMAKE_AUTORCC is ON (the alternative is qt_add_resources).

## Checked
2026-11-03. Confirmed in the qt_standard_project_setup, Getting started with CMake and Qt resource system pages: AUTOMOC and AUTOUIC are set by qt_standard_project_setup, uic runs on .ui sources, .qrc sources need CMAKE_AUTORCC. Fixed: the skill claimed AUTORCC is also set by qt_standard_project_setup (it is not). Removed: vtable and mocs_compilation.cpp claims and the per-target AUTOMOC line (not in the Qt pages).

Method: documentation only; no commands were run.

## Verify
- The build runs moc for Q_OBJECT classes and the .qrc content is available at runtime.
