---
id: computing-software.software-engineering.desktop-ui-frameworks.qt-linux-appimage-deploy
name: qt-linux-appimage-deploy
category: computing-software
field: software-engineering
product: desktop-ui-frameworks
tags: [qt-linux-appimage-deploy, qt-deployment, qt, qt6, deployment, desktop-ui-frameworks]
level: practitioner
status: draft
description: "Package a Qt app for Linux using linuxdeploy with the Qt plugin into an AppImage."
sources:
  - https://doc.qt.io/qt-6/windows-deployment.html
  - https://doc.qt.io/qt-6/macos-deployment.html
  - https://doc.qt.io/qt-6/linux-deployment.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Qt Linux AppImage deployment

**Goal:** one-file Linux distribution.

```bash
export QMAKE=<path-to-Qt>/bin/qmake
linuxdeploy --appdir AppDir -e build/app -d app.desktop -i app.png --plugin qt --output appimage
# Qt 6.5+ xcb plugin needs libxcb-cursor0 on the target (confirm)
```

**Gotcha:** Build on the oldest distro you support; AppImages inherit its glibc floor, and Wayland plugins must be included for Wayland-only desktops.

## Verify
- Run the AppImage on a different, clean distro.
