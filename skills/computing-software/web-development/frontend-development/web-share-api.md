---
id: computing-software.web-development.frontend-development.web-share-api
name: web-share-api
category: computing-software
field: web-development
product: frontend-development
tags: [device-apis, web-share-api, navigator-share, mobile, pwa]
level: practitioner
status: docs-checked
description: "Opening the native share sheet with navigator.share: feature detection, sharing files with canShare, user-activation rules, AbortError handling and fallbacks."
sources:
  - https://developer.mozilla.org/en-US/docs/Web/API/Navigator/share
  - https://developer.mozilla.org/en-US/docs/Web/API/Navigator/canShare
  - https://w3c.github.io/web-share/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Web Share API

## 1. Share a link
```js
shareBtn.hidden = !navigator.share;          // or show a fallback menu
shareBtn.addEventListener("click", async () => {
  const data = { title: document.title, text: "Check this out", url: location.href };
  try { await navigator.share(data); }
  catch (e) { if (e.name !== "AbortError") copyLinkFallback(data.url); }   // AbortError = user closed the sheet
});
```
Requirements (MDN): secure context, transient activation (call it directly in the click handler), and the `web-share` Permissions Policy (iframes need `allow="web-share"`). It throws `NotAllowedError` without activation or when blocked by policy, `InvalidStateError` if the document is not fully active or another share is in progress, and `AbortError` when the user dismisses the sheet.

## 2. Share files
```js
const file = new File([blob], "chart.png", { type: "image/png" });
if (navigator.canShare?.({ files: [file] })) await navigator.share({ files: [file], title: "Chart" });
```
Prepare the file **before** the click so `navigator.share()` runs while the user activation is still valid. MDN lists usually shareable types (for example PDF, common audio, image, text and video formats) but says to always test with `navigator.canShare()`.

## 3. Support
Support varies by browser and platform (check MDN's compatibility table for `Navigator.share` and its file-sharing parameter, which Firefox does not support per browser-compat-data); always feature-detect and have a fallback (copy link button, mailto:).

## 4. Receiving shares
Installed web apps can receive shares via `share_target` in the web app manifest; browser-compat-data marks it experimental and supported in Chromium browsers only.

## 5. Pitfalls
- `url` should be absolute and canonical (strip tracking params unless intended).
- Receiving apps decide how to combine `title`, `text` and `url`; test with your target apps.

## Verify
Test on iOS Safari and Android Chrome; confirm cancel does not show an error and the fallback appears in browsers without support.

## Checked

Checked 2026-10-26 against MDN Navigator.share(), Navigator.canShare() (mdn/content main) and MDN browser-compat-data (api/Navigator.json and manifests/webapp/share_target.json): secure context, `web-share` permissions policy, transient activation, the three error names, the shareable file types list and the Chromium-only experimental `share_target`. Removed the unconfirmed per-browser platform list and the claim about Safari consuming activation.

Method: documentation only; no commands were run.
