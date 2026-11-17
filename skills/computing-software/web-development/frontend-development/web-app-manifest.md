---
id: computing-software.web-development.frontend-development.web-app-manifest
name: web-app-manifest
category: computing-software
field: web-development
product: frontend-development
tags: [progressive-web-app, pwa, web-app-manifest, manifest-json, maskable-icons, display-standalone, app-shortcuts, start-url, theme-color]
level: practitioner
status: docs-checked
description: "Writing a web app manifest that passes installability: icons incl. maskable, display modes, start_url/scope/id, shortcuts, screenshots and theme colours."
sources:
  - https://developer.mozilla.org/en-US/docs/Web/Progressive_web_apps/Manifest
  - https://developer.mozilla.org/en-US/docs/Web/Progressive_web_apps/Manifest/Reference/id
  - https://developer.mozilla.org/en-US/docs/Web/Progressive_web_apps/Manifest/Reference/icons
  - https://developer.mozilla.org/en-US/docs/Web/Progressive_web_apps/Guides/Making_PWAs_installable
  - https://w3c.github.io/manifest/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Web app manifest

**Goal:** the app installs with correct name, icons, colours and launch URL on Android, desktop Chromium and iOS.

## 1. Minimal manifest that installs
```json
{
  "id": "/",
  "name": "Acme Tasks",
  "short_name": "Tasks",
  "start_url": "/?source=pwa",
  "scope": "/",
  "display": "standalone",
  "background_color": "#ffffff",
  "theme_color": "#1d4ed8",
  "icons": [
    { "src": "/icons/192.png", "sizes": "192x192", "type": "image/png" },
    { "src": "/icons/512.png", "sizes": "512x512", "type": "image/png" },
    { "src": "/icons/maskable-512.png", "sizes": "512x512", "type": "image/png", "purpose": "maskable" }
  ]
}
```
Link it from every page: `<link rel="manifest" href="/manifest.webmanifest">`. The W3C spec registers `application/manifest+json` as the media type and the `.webmanifest` extension.

## 2. Field notes
- **`id`** is the app's identity. MDN: if it is missing or invalid, `start_url` is used, so changing `start_url` later can change the identity. It is resolved against the origin of `start_url` and any fragment is ignored. Set `id` once and don't change it.
- **`scope`**: navigations outside it open in a browser tab/custom tab. Put the manifest-linked pages inside.
- **`display`**: `standalone` (no browser UI) is the usual; `minimal-ui` keeps back/reload; `display_override: ["window-controls-overlay"]` for desktop title-bar apps.
- **Maskable icons**: an icon with `purpose: "maskable"` whose important content sits inside the safe zone, defined by the W3C spec as a circle centred on the icon with a radius of 40% of the icon size. Keep a separate `any` icon for contexts that don't mask.
- **`shortcuts`**: each `{name, url, icons}`; MDN advises a few important shortcuts because platforms may truncate long lists.
- **`screenshots`** with `form_factor: "wide"|"narrow"` enable the richer install dialog in Chromium.
- `theme_color` in the manifest sets the app's theme colour; the `<meta name="theme-color">` tag covers the browser tab UI and can use a `media` attribute for dark mode.

## 3. iOS specifics
MDN: on iOS 16.4 and later, PWAs can be installed from the Share menu in Safari, Chrome, Edge, Firefox and Orion (earlier iOS only Safari), and Safari on macOS 14 (Sonoma) and later offers File > Add to Dock. There is no programmatic install prompt in Safari.

## 4. Installability (Chromium)
MDN's installability criteria for Chromium-based browsers: served over HTTPS (or localhost), a manifest with `name` or `short_name`, `icons` including a 192px and a 512px icon, `start_url`, `display` and/or `display_override`, and `prefer_related_applications` false or absent. MDN says a service worker is not a requirement for installability.

## Verify
- [ ] DevTools > Application > Manifest shows no errors or warnings, maskable preview looks right.
- [ ] Install on Android: splash uses background_color + icon, launches at start_url in standalone.
- [ ] Desktop install shows the app name and icon in the OS app list.

## Checked
Checked 2026-10-26 against MDN Progressive web apps manifest reference pages (id, icons, shortcuts, screenshots form_factor, prefer_related_applications), MDN Making PWAs installable (Chromium criteria, iOS 16.4 install from the Share menu, Safari Add to Dock), and the W3C Web Application Manifest spec (media type, safe zone circle radius 40%). Removed unconfirmed items: maskable.app tool, the 'up to ~4 shortcuts' figure, apple-touch-icon 180x180 and transparency rules, and the claim that Safari reads name, display and start_url from the manifest. The manifest JSON was not validated by a tool.

Method: documentation only; no commands were run.
