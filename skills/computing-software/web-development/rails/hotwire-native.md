---
id: computing-software.web-development.rails.hotwire-native
name: hotwire-native
category: computing-software
field: web-development
product: rails
tags: [hotwire-native, turbo-native, mobile-apps, bridge-components, rails]
level: advanced
status: docs-checked
description: "Hotwire Native for Rails apps: web-first iOS and Android shells, path configuration rules and versioning, and bridge components."
sources:
  - https://native.hotwired.dev/
  - https://native.hotwired.dev/overview/path-configuration
  - https://native.hotwired.dev/overview/bridge-components
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Hotwire Native

Hotwire Native is a web-first framework for native mobile apps on iOS and Android. It wraps a web view in a native shell and renders HTML from your server; native navigation and transition animations between screens work out of the box. You build screens once in HTML and CSS and reuse them on every platform, including screens from an existing Hotwire web app. Web-side fixes and features ship without app store review. When the web is not enough, upgrade a screen with Bridge Components or a fully native screen.

## 1. Path configuration
A JSON file configures advanced navigation. It has two required top-level keys:
```json
{
  "settings": {},
  "rules": []
}
```
- `settings`: app-level items read when the file loads, such as feature flags or custom app information you want to control remotely.
- `rules`: entries with regex `patterns` that identify URLs and `properties` applied on navigation. Example from the docs: URLs matching `/new$` with `"context": "modal"` open in a modal screen instead of the default navigation stack.
```json
{
  "rules": [
    { "patterns": ["/new$"], "properties": { "context": "modal" } }
  ]
}
```
- Keep the file both locally (bundled with the app binary, for a smooth first launch) and remotely on your server, so behaviour can change without an app update.
- Version the file names and use one resource per platform, for example `/configurations/ios_v1.json` and `/configurations/android_v1.json`. On breaking changes point the new build at `*_v2.json` and keep old versions on the server for older clients.
- The iOS and Android pages and the path configuration reference list the built-in behaviours.

## 2. Bridge components (formerly Strada components)
A web view alone cannot tell the native app what the page is doing. A Bridge Component has two parts: a web component controller built with Stimulus and a native counterpart in Swift or Kotlin. They communicate through Hotwire Native's component framework, so web features can drive native ones: buttons in the top app bar, native menu sheets, platform APIs. Examples from the docs: native buttons that submit forms, and web dialogs shown as a UIActionSheet on iOS or BottomSheetDialog on Android. The framework is now included in Hotwire Native with no extra dependencies.

## 3. Choosing how native to go
Ship a purely web screen first, then progressively enhance specific features natively: Bridge Components when a feature needs a more responsive interaction, a fully native screen when it needs a high-fidelity experience.

## Verify
- [ ] Path configuration is bundled and served remotely, per-platform and versioned, and a rule change takes effect without an app release.

## Checked

2026-11-09. Read in full the Hotwire Native home, Path Configuration and Bridge Components pages. Confirmed the framework description, the settings and rules structure, the `/new$` modal rule, local plus remote and versioned file guidance, and the bridge component model. Removed, as not on these pages: the iOS Swift package and Android dependency setup, the navigator and activity classes, in-app-browser behaviour, the `pull_to_refresh_enabled`, `view_controller` and `presentation` properties, the turbo-rails helpers (`hotwire_native_app?`, `recede_or_redirect_to`), the JavaScript BridgeComponent sample, and authentication advice. Dropped the hotwire-native-ios GitHub source (not read).

Method: documentation only; no commands were run.
