---
id: computing-software.software-engineering.desktop-ui-frameworks.electron-macos-notarize
name: electron-macos-notarize
category: computing-software
field: software-engineering
product: desktop-ui-frameworks
tags: [electron-macos-notarize, electron-packaging, electron, packaging, desktop-ui-frameworks]
level: practitioner
status: docs-checked
description: "Sign with a Developer ID certificate and notarize an Electron app with electron-builder or @electron/notarize."
sources:
  - https://www.electronjs.org/docs/latest/tutorial/code-signing
  - https://github.com/electron/notarize
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Electron macOS signing and notarization

**Goal:** Gatekeeper-approved app.

```bash
# electron-builder reads these environment variables for notarization
export APPLE_ID=<apple-id> APPLE_APP_SPECIFIC_PASSWORD=<app-password> APPLE_TEAM_ID=<team>
npx electron-builder --mac
stapler validate path/to/notarized.app
```

Electron Forge and `@electron/packager` do the same through `osxSign` and `osxNotarize` (`@electron/osx-sign` and `@electron/notarize` underneath).

**Gotcha:** notarization needs the app signed with hardened runtime and the `com.apple.security.cs.allow-jit` entitlement. `com.apple.security.cs.allow-unsigned-executable-memory` is only for Electron 11 and below. Without credentials electron-builder skips notarization with a warning, so set them before the build starts.

## Verify
- `stapler validate` reports the ticket is valid.

## Checked
2026-11-03. Confirmed in the Electron code signing tutorial, the `@electron/notarize` README and the electron-builder notarization page: the two-step sign then notarize flow, `osxSign`/`osxNotarize`, `APPLE_ID`, `APPLE_APP_SPECIFIC_PASSWORD` and `APPLE_TEAM_ID`, `xcrun notarytool` as the backend, hardened runtime plus `allow-jit`, the Electron 11 limit on `allow-unsigned-executable-memory`, `stapler validate`, and skipped notarization without credentials. Removed: the claim that `allow-unsigned-executable-memory` is needed, `spctl` output expectations, the `dist/mac/App.app` path, and the claim that one unsigned helper fails the whole submission (not in the pages read).
Method: documentation only; no commands were run.
