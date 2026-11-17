---
id: computing-software.web-development.frontend-development.favicons-and-theme-color
name: favicons-and-theme-color
category: computing-software
field: web-development
product: frontend-development
tags: [favicon-set, theme-color-meta, apple-touch-icon, svg-favicon, maskable-icon, html]
level: practitioner
status: docs-checked
description: "The minimal modern favicon set (ico, SVG, apple-touch-icon, manifest icons), dark-mode SVG favicons and theme-color meta with media queries."
sources:
  - https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Attributes/rel
  - https://developer.mozilla.org/en-US/docs/Web/Progressive_web_apps/Manifest/Reference/icons
  - https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Elements/meta/name/theme-color
  - https://developer.mozilla.org/en-US/docs/Web/Progressive_web_apps/Manifest/Reference/theme_color
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Favicons and theme-color

## 1. The small set that covers everything
```html
<link rel="icon" href="/favicon.ico" sizes="32x32">
<link rel="icon" href="/icon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="manifest" href="/manifest.webmanifest">
```
```json
{ "icons": [
  { "src": "/icon-192.png", "sizes": "192x192", "type": "image/png" },
  { "src": "/icon-512.png", "sizes": "512x512", "type": "image/png" },
  { "src": "/icon-mask.png", "sizes": "512x512", "type": "image/png", "purpose": "maskable" }
]}
```
- iOS does not use `rel="icon"`; it uses the non-standard `apple-touch-icon` link type.
- Maskable icon (`"purpose": "maskable"`): design it with a safe zone, because anything outside the safe zone can be masked away.

## 2. Dark-mode SVG favicon
```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32">
  <style>path{fill:#111} @media (prefers-color-scheme: dark){path{fill:#fff}}</style>
  <path d="..."/>
</svg>
```

## 3. theme-color
```html
<meta name="theme-color" content="#ffffff" media="(prefers-color-scheme: light)">
<meta name="theme-color" content="#0b0b0f" media="(prefers-color-scheme: dark)">
```
The colour may be applied to browser UI such as the toolbar, address bar and status bar; the manifest has a matching `theme_color` member.

## Gotchas
- Frameworks: the Next.js App Router has `favicon`, `icon` and `apple-icon` file conventions in `app/`; if you use them, do not also hand-write the links.
- Serve the manifest with `Content-Type: application/manifest+json` (`.webmanifest` extension).

## Verify
- [ ] The manifest response has `Content-Type: application/manifest+json` and every icon URL resolves.
- [ ] Tab icon correct in light and dark OS themes; iOS "Add to Home Screen" shows the opaque icon.

## Checked
2026-10-26. MDN rel page, manifest icons and theme_color references, manifest overview, and the Next.js app-icons file convention docs (main, 2026-10-26): confirmed meta theme-color takes a media attribute and can tint toolbar, address bar and status bar, the maskable purpose and safe zone, iOS using apple-touch-icon rather than rel=icon, the manifest media type, and the Next.js favicon/icon/apple-icon conventions. Removed unread-blog claims (32x32 ico trick, iOS black fill and padding, 80% safe zone, favicon caching and the root favicon.ico advice) and the DevTools panel claim.
Method: documentation only; no commands were run.
