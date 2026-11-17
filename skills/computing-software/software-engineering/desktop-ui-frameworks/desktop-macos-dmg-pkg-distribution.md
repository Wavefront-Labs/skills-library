---
id: computing-software.software-engineering.desktop-ui-frameworks.desktop-macos-dmg-pkg-distribution
name: desktop-macos-dmg-pkg-distribution
category: computing-software
field: software-engineering
product: desktop-ui-frameworks
tags: [desktop-macos-dmg-pkg-distribution, desktop-installers, installer, code-signing, windows, macos, desktop-ui-frameworks]
level: practitioner
status: draft
description: "Create a signed dmg, notarize and staple it."
sources:
  - https://learn.microsoft.com/en-us/windows/msix/
  - https://wixtoolset.org/docs/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# macOS distribution dmg and pkg

**Goal:** Gatekeeper-friendly distribution.

```bash
hdiutil create -volname App -srcfolder dist/App.app -ov -format UDZO App.dmg
codesign --sign "Developer ID Application: <name>" --options runtime --timestamp App.dmg
xcrun notarytool submit App.dmg --keychain-profile notary --wait
xcrun stapler staple App.dmg
spctl -a -t open --context context:primary-signature -vv App.dmg
```

**Gotcha:** Stapling embeds the ticket so first launch works offline; skipping it causes slow or failed first runs without network.

## Verify
- A downloaded copy opens with no Gatekeeper warning.
