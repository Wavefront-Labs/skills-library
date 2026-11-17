---
id: computing-software.software-engineering.desktop-ui-frameworks.qt-creator-kits-debug
name: qt-creator-kits-debug
category: computing-software
field: software-engineering
product: desktop-ui-frameworks
tags: [qt-creator-kits-debug, qt-creator, qt, desktop-ui-frameworks]
level: practitioner
status: docs-checked
description: "Create a kit (device, compiler, Qt version, debugger) and start QML debugging in Qt Creator."
sources:
  - https://doc.qt.io/qtcreator/creator-targets.html
  - https://doc.qt.io/qtcreator/creator-debugging-qml.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Qt Creator kits and debugging

**Goal:** a working build/debug setup.

```text
Preferences > Kits > Add (or Clone), set device, compiler, Qt version and debugger, then Apply
Make Default sets the kit used when Qt Creator cannot choose one
Projects > Build Settings > QML debugging and profiling: Enable
Run Settings > Debugger Settings > QML debugger: Automatic or Enabled (C++ debugger too for both)
Debug > Start Debugging > Start Debugging of Startup Project (F5)
```

**Gotcha:** QML debugging opens a TCP port; anyone who can reach it can run JavaScript in the app, so firewall it. With CMake or qmake, release configurations do not include QML debugging by default.

## Checked
2026-11-03. Confirmed in the Qt Creator pages Add kits and Debugging Qt Quick projects: kit contents, Preferences > Kits and Make Default, QML debugging build and run settings, the start command and F5, the security note on the TCP port. Removed: the CMAKE_BUILD_TYPE argument, the QML Profiler line, pretty-printer and warning-triangle claims, and named debugger/compiler lists (not in the pages).

Method: documentation only; no commands were run.

## Verify
- A breakpoint in a JavaScript function stops the running application.
