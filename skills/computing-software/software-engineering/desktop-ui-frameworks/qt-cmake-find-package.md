---
id: computing-software.software-engineering.desktop-ui-frameworks.qt-cmake-find-package
name: qt-cmake-find-package
category: computing-software
field: software-engineering
product: desktop-ui-frameworks
tags: [qt-cmake-find-package, qt-cmake, qt, qt6, cmake, desktop-ui-frameworks]
level: practitioner
status: docs-checked
description: "Configure a Qt 6 project with find_package, qt_standard_project_setup and qt_add_executable."
sources:
  - https://doc.qt.io/qt-6/cmake-get-started.html
  - https://doc.qt.io/qt-6/qt-standard-project-setup.html
  - https://doc.qt.io/qt-6/qt-add-executable.html
  - https://doc.qt.io/qt-6/macos-deployment.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Qt 6 find_package and qt_standard_project_setup

**Goal:** a minimal modern Qt CMake project.

```cmake
cmake_minimum_required(VERSION 3.16)
project(app LANGUAGES CXX)
find_package(Qt6 REQUIRED COMPONENTS Widgets Network)
qt_standard_project_setup()
qt_add_executable(app main.cpp mainwindow.cpp)
target_link_libraries(app PRIVATE Qt6::Widgets Qt6::Network)
# configure: cmake -DCMAKE_PREFIX_PATH=<path-to-Qt>/<version>/<platform> -S . -B build
# or use the qt-cmake script from the Qt install, which sets CMAKE_PREFIX_PATH for you
```

**Gotcha:** CMake finds Qt through CMAKE_PREFIX_PATH (delete CMakeCache.txt when changing it); building for Apple platforms needs cmake_minimum_required 3.21.1 or newer.

## Checked
2026-11-03. Confirmed in the Getting started with CMake, qt_standard_project_setup, qt_add_executable and Qt for macOS deployment pages: the minimum-version line used by the official example is 3.16, CMAKE_PREFIX_PATH and the qt-cmake script, the 3.21.1 floor for Apple platforms. Fixed: cmake_minimum_required 3.21 replaced by the documented 3.16. Removed: the Could not find Qt6Config and MSVC/MinGW kit claim.

Method: documentation only; no commands were run.

## Verify
- cmake --build build succeeds and the binary starts.
