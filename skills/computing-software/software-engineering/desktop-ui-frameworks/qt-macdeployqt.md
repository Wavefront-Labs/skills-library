---
id: computing-software.software-engineering.desktop-ui-frameworks.qt-macdeployqt
name: qt-macdeployqt
category: computing-software
field: software-engineering
product: desktop-ui-frameworks
tags: [qt-macdeployqt, qt-deployment, qt, qt6, deployment, desktop-ui-frameworks]
level: practitioner
status: docs-checked
description: "Bundle Qt frameworks into an app bundle and prepare it for signing and notarization."
sources:
  - https://doc.qt.io/qt-6/macos-deployment.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# macdeployqt

**Goal:** a relocatable .app.

```bash
macdeployqt App.app -qmldir=./qml -dmg
# sign during deployment: -codesign=<ident> -hardened-runtime -timestamp
# or -sign-for-notarization=<ident> (turns on hardened runtime, timestamp and codesign)
```

**Gotcha:** macdeployqt signs ad hoc (-codesign=-) by default; pass -sign-for-notarization=<ident> (needs internet) when you will notarize. It picks up the first .entitlements file in Contents/Resources, so keep at most one there. Run it from the app's directory so the .dmg volume name is just the app name.

## Checked
2026-11-03. Confirmed in the Qt for macOS deployment page: macdeployqt options -qmldir, -dmg, -codesign, -hardened-runtime, -timestamp, -sign-for-notarization, entitlements behaviour, dmg volume name. Removed: the codesign --deep, xcrun notarytool and spctl commands (Apple tools, not in the Qt pages) and the signing-order claim.

Method: documentation only; no commands were run.

## Verify
- The bundle runs on a Mac that has no Qt installed.
