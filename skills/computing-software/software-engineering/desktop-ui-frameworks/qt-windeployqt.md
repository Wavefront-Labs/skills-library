---
id: computing-software.software-engineering.desktop-ui-frameworks.qt-windeployqt
name: qt-windeployqt
category: computing-software
field: software-engineering
product: desktop-ui-frameworks
tags: [qt-windeployqt, qt-deployment, qt, qt6, deployment, desktop-ui-frameworks]
level: practitioner
status: docs-checked
description: "Gather Qt DLLs, plugins and QML imports next to a Windows executable with windeployqt."
sources:
  - https://doc.qt.io/qt-6/windows-deployment.html
  - https://doc.qt.io/qt-6/qt-generate-deploy-app-script.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# windeployqt

**Goal:** a runnable Windows folder.

```bash
windeployqt --release --qmldir ./qml build/Release/app.exe
# optional: --no-translations --dir dist   (compiler runtime is copied by default; --no-compiler-runtime turns it off)
# CMake alternative: qt_generate_deploy_app_script() (since Qt 6.3, Windows/macOS/Linux)
```

**Gotcha:** windeployqt (in the Qt install's bin folder) scans the executable for dependencies; without --qmldir QML imports are not scanned, and third-party libraries are not covered. For MSVC release builds ship the official Visual C++ Redistributable, not loose runtime DLLs.

## Checked
2026-11-03. Confirmed in the Qt for Windows deployment and qt_generate_deploy_app_script pages: --release, --qmldir, --no-translations, --dir, --compiler-runtime and --no-compiler-runtime, Visual C++ Redistributable note, qt_generate_deploy_app_script since 6.3. Removed: the mixed-kit claim.

Method: documentation only; no commands were run.

## Verify
- Run the exe on a clean VM without Qt installed.
