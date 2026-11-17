---
id: computing-software.software-engineering.desktop-ui-frameworks.electron-builder-config
name: electron-builder-config
category: computing-software
field: software-engineering
product: desktop-ui-frameworks
tags: [electron-builder-config, electron-packaging, electron, packaging, desktop-ui-frameworks]
level: practitioner
status: docs-checked
description: "Configure electron-builder via electron-builder.yml, per-platform targets and the publish provider."
sources:
  - https://www.electronjs.org/docs/latest/tutorial/application-distribution
  - https://www.electronforge.io/
  - https://www.electron.build/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# electron-builder configuration

**Goal:** multi-platform installers from one config file.

```yaml
# electron-builder.yml (default config path; or the "build" key in package.json)
appId: com.example.app
win:   { target: [nsis] }
mac:   { target: [dmg, zip] }
linux: { target: [AppImage, deb] }
publish: { provider: github }
# run: npx electron-builder --win --x64
```

**Gotcha:** the option layout changed between electron-builder major versions. In v27 the macOS signing options (`hardenedRuntime`, `entitlements`, and so on) live under `mac.sign`, and `notarize` stays on `mac`. Check the docs for the installed version before copying signing config, and run `electron-builder migrate-schema` when upgrading.

## Verify
- The installer runs and the app starts.

## Checked
2026-11-03. Confirmed in the electron-builder docs (configuration, mac, cli, publish, notarization): `electron-builder.yml` is the default config file, `package.json` `build` key is supported, `appId`, mac targets `dmg` and `zip` (the defaults), `--win` and `--x64` flags, `publish` with `provider: github`, AppImage and deb targets, the v27 move of signing options under `mac.sign`, `notarize` staying on `mac`, and `migrate-schema`. Removed: `publisherName`, `hardenedRuntime`/`notarize` as flat mac keys, the `files` list and the native-module rebuild gotcha (not confirmed in pages read).
Method: documentation only; no commands were run.
