---
id: computing-software.web-development.frontend-development.app-badging-and-manifest-shortcuts
name: app-badging-and-manifest-shortcuts
category: computing-software
field: web-development
product: frontend-development
tags: [app-badging, manifest-shortcuts, window-controls-overlay, setappbadge, pwa-capabilities, pwa]
level: practitioner
status: docs-checked
description: "Installed PWA OS integration: App Badging API for unread counts, manifest shortcuts for jump lists, and Window Controls Overlay for desktop title bars."
sources:
  - https://developer.mozilla.org/en-US/docs/Web/API/Badging_API
  - https://developer.mozilla.org/en-US/docs/Web/Progressive_web_apps/Manifest/Reference/shortcuts
  - https://developer.mozilla.org/en-US/docs/Web/Progressive_web_apps/Manifest/Reference/display_override
  - https://developer.mozilla.org/en-US/docs/Web/API/Window_Controls_Overlay_API
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# App badging, shortcuts and window controls overlay

## 1. Badging
```js
if ("setAppBadge" in navigator) {
  unread > 0 ? navigator.setAppBadge(unread) : navigator.clearAppBadge();
}
```
- Badges apply to installed web apps. Browser-compat-data: Chrome 81, Safari 17 on macOS and Safari 16.4 for web apps saved to the iOS Home Screen; no Firefox support. `setAppBadge()` with no argument shows an unnumbered flag (a colored circle, for example); in Safari, passing `0` clears the badge.

## 2. Shortcuts (jump list / long-press menu)
```json
"shortcuts": [
  { "name": "New invoice", "short_name": "New", "url": "/invoices/new?source=shortcut",
    "icons": [{ "src": "/icons/new-96.png", "sizes": "96x96" }] },
  { "name": "Inbox", "url": "/inbox" }
]
```
`name` and `url` are required; the URL can be relative. Supported in Chrome 96 and Safari 17.4 (browser-compat-data). Add a query parameter to the URL to measure use.

## 3. Window Controls Overlay (desktop)
```json
"display_override": ["window-controls-overlay"], "display": "standalone"
```
```css
.titlebar {
  position: fixed; left: env(titlebar-area-x, 0); top: env(titlebar-area-y, 0);
  width: env(titlebar-area-width, 100%); height: env(titlebar-area-height, 40px);
}
```
Listen to `navigator.windowControlsOverlay.ongeometrychange` to re-layout. `display_override` is tried before `display`, which is the fallback. Chrome 105 only (browser-compat-data), and marked experimental.

## Verify
- [ ] Badge appears on the taskbar/dock or Home Screen icon after `setAppBadge()`.
- [ ] Shortcuts appear in the OS menu after reinstall.

## Checked

Checked 2026-10-26 against mdn/content (main) Badging API, manifest `shortcuts` and `display_override`, Window Controls Overlay API pages, and mdn/browser-compat-data (including the Safari notes for badges on Home Screen web apps).

- Fixed: the iOS notification-permission requirement, the service-worker badge advice and the "changes take a day" note are not in the pages checked and were removed; support is now stated from the compatibility data. `app-region` lines were removed (no checked page documents them).
- Confirmed: `setAppBadge()` without an argument shows an unnumbered flag; `shortcuts` require `name` and `url`; `titlebar-area-*` environment variables position content in the title bar area; `display_override` entries are considered before `display`.

Method: documentation only; no commands were run.
