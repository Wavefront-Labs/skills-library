---
id: computing-software.web-development.responsive-design.user-preference-media-features
name: user-preference-media-features
category: computing-software
field: web-development
product: responsive-design
tags: [prefers-contrast, user-preference-media, prefers-reduced-data, prefers-reduced-transparency, media-queries]
level: practitioner
status: gated
description: "Responding to user preference media features: prefers-contrast, prefers-reduced-transparency, prefers-reduced-data and others, with support notes and testing."
sources:
  - https://developer.mozilla.org/en-US/docs/Web/CSS/@media/prefers-contrast
  - https://developer.mozilla.org/en-US/docs/Web/CSS/@media/prefers-reduced-transparency
  - https://developer.mozilla.org/en-US/docs/Web/CSS/@media/prefers-reduced-data
  - https://www.w3.org/TR/mediaqueries-5/#mf-user-preferences
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# User preference media features

Media Queries Level 5 lets the OS tell your page how the user wants content presented. Motion and colour scheme are covered elsewhere; these are the rest.

## 1. prefers-contrast (Baseline 2022: Chrome 96, Firefox 101, Safari 14.1; low date 2022-05-31)
```css
@media (prefers-contrast: more) {
  :root { --border: #000; --text-muted: #333; }
  .card { border: 2px solid var(--border); box-shadow: none; }
  .btn-ghost { outline: 1px solid currentColor; }
}
@media (prefers-contrast: less) { :root { --text: #333; } }
```
- Values: `no-preference | more | less | custom` (run: Playwright accepts `contrast: 'more'` and `'no-preference'`; CDP emulation matched `more`, `less` and `custom`). `custom` matches when `forced-colors: active` uses a palette that is neither high nor low.
- macOS "Increase contrast" and iOS equivalents trigger `more` (gated: unconfirmed, source is paywalled or blocked); Windows contrast themes trigger `forced-colors: active` (handle that separately with system colours; Playwright `forced_colors='active'` reported `(forced-colors: active)` true but `prefers-contrast: no-preference`, so emulation does not reproduce `custom`).
- Typical fixes: darker secondary text, visible borders instead of subtle shadows, solid backgrounds instead of translucent ones.

## 2. prefers-reduced-transparency
```css
.glass { background: rgb(255 255 255 / .6); backdrop-filter: blur(12px); }
@media (prefers-reduced-transparency: reduce) { .glass { background: #fff; backdrop-filter: none; } }
```
Supported in Chromium 118+ and Firefox behind a flag (MDN compat data lists Safari as unsupported; run: CDP `Emulation.setEmulatedMedia` with `prefers-reduced-transparency: reduce` matched in Chromium 156). Write the solid version as the safe default if contrast is at stake.

## 3. prefers-reduced-data
Proposed (Data Saver / Save-Data); only behind a flag in Chromium (MDN compat data), unsupported elsewhere; the query did not match in Chromium 156 even with emulation. Use the `Save-Data: on` request header server-side (Chromium) to serve lighter images and skip autoplay video, and treat the media query as an enhancement:
```css
@media (prefers-reduced-data: reduce) { .hero { background-image: none; } }
```
`navigator.connection?.saveData` is the JS equivalent where available.

## 4. Others worth knowing
- `inverted-colors: inverted` (Safari only per MDN compat data: Safari 9.1, Firefox behind a flag): un-invert photos with `filter: invert(1)`.
- `scripting: none` to show no-JS fallbacks; `update: slow` for e-ink.
- `dynamic-range: high` for HDR images/video.

## 5. JS access and testing
`matchMedia("(prefers-contrast: more)")` with a `change` listener. DevTools > Rendering tab emulates `prefers-contrast`, `prefers-reduced-transparency`, `forced-colors`, `prefers-color-scheme`, and `prefers-reduced-motion`.

## Verify
- [ ] Each supported preference emulated in DevTools changes the UI as intended; text remains at least 4.5:1 in every combination; nothing important hidden under any preference.
