---
id: computing-software.software-engineering.tauri.tauri-deep-linking-plugin
name: tauri-deep-linking-plugin
category: computing-software
field: software-engineering
product: tauri
tags: [deep-linking-plugin, tauri, deep-links, mobile]
level: advanced
status: docs-checked
description: "Register a Tauri app as the handler for custom schemes or app/universal links, handle opened URLs, and test deep links on desktop, iOS and Android."
sources:
  - "https://v2.tauri.app/plugin/deep-linking/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Tauri deep linking plugin

Goal: open your app from URLs. Install with `pnpm tauri add deep-link` (or `cargo add tauri-plugin-deep-link@2.0.0` plus `.plugin(tauri_plugin_deep_link::init())`).

## Configuration

Under `tauri.conf.json > plugins > deep-link`:

```json
{
  "plugins": {
    "deep-link": {
      "mobile": [
        { "scheme": ["ovi"], "appLink": false },
        { "scheme": ["https"], "host": "your.website.com", "pathPrefix": ["/open"], "appLink": true }
      ],
      "desktop": { "schemes": ["something", "my-tauri-app"] }
    }
  }
}
```

A custom scheme on mobile needs no host or server. Verified links need a server file:
- Android app links: `.well-known/assetlinks.json` with `package_name` set to `tauri.conf.json > identifier` with `-` replaced by `_`, and the app's SHA256 certificate fingerprints.
- iOS universal links: HTTPS `.well-known/apple-app-site-association` served as `application/json`, with `appIDs` of `<team id>.<bundle id>`. Check with `curl -v https://app-site-association.cdn-apple.com/a/v1/<host>`.

## Desktop

On Linux and Windows a deep link arrives as a command line argument to a new process. For a single instance, enable the `deep-link` feature on `tauri-plugin-single-instance` and register it as the first plugin. Verify URLs against the format you expect, since users can pass a fake link; Tauri only handles statically configured schemes, so check runtime-registered ones yourself via `Env::args_os`.

## Listening

```javascript
import { getCurrent, onOpenUrl } from '@tauri-apps/plugin-deep-link';
const startUrls = await getCurrent();
await onOpenUrl((urls) => { console.log('deep link:', urls); });
```

Rust: `app.deep_link().get_current()?` and `app.deep_link().on_open_url(|event| ...)`. The list usually holds one URL.

## Runtime registration and testing

Deep links only fire for installed desktop apps. On Linux and Windows call `app.deep_link().register("my-app")?` or `register_all()?` (statically configured schemes, also useful in dev). Not possible on macOS: test the bundled app in `/Applications`. Trigger with `start <scheme>://url` (Windows), `xdg-open <scheme>://url` (Linux), `xcrun simctl openurl booted https://<host>/path` (iOS simulator), `adb shell am start -a android.intent.action.VIEW -d https://<host>/path <bundle-identifier>` (Android).

Capability: `deep-link:default`, usually with `core:event:default`.

## Checked
2026-11-07. Confirmed claim by claim against https://v2.tauri.app/plugin/deep-linking/ (page text including code blocks and tabs read in full).
Method: documentation only; no commands were run.
