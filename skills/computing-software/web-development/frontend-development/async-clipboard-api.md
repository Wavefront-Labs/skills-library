---
id: computing-software.web-development.frontend-development.async-clipboard-api
name: async-clipboard-api
category: computing-software
field: web-development
product: frontend-development
tags: [device-apis, clipboard-api, copy-paste, permissions, javascript]
level: practitioner
status: docs-checked
description: "Copying and pasting with navigator.clipboard: secure context and user-activation rules, writeText vs ClipboardItem for images/HTML, paste events, and fallback UX."
sources:
  - https://developer.mozilla.org/en-US/docs/Web/API/Clipboard_API
  - https://developer.mozilla.org/en-US/docs/Web/API/ClipboardItem
  - https://w3c.github.io/clipboard-apis/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Async Clipboard API

## 1. Copy text
```js
async function copy(text, button) {
  try {
    await navigator.clipboard.writeText(text);
    announce("Copied to clipboard");              // live region; also change button label briefly
  } catch (err) {
    selectForManualCopy(text);                     // show a selected input as fallback
  }
}
button.addEventListener("click", () => copy(code.textContent, button));
```
Requirements: secure context (HTTPS/localhost). Writing needs transient user activation in Firefox and Safari; in Chromium it needs either transient activation or the granted `clipboard-write` permission. Call it directly from the click handler.

## 2. Rich content
```js
await navigator.clipboard.write([new ClipboardItem({
  "text/plain": new Blob([plain], { type: "text/plain" }),
  "text/html": new Blob([html], { type: "text/html" }),
})]);
// a ClipboardItem value may also be a Promise that resolves to a Blob or string, so the write can start inside the gesture while you fetch
new ClipboardItem({ "image/png": fetch(url).then(r => r.blob()) });
```
`ClipboardItem.supports()` always returns true for `text/plain`, `text/html` and `image/png`; other types (for example `image/svg+xml`) need a `ClipboardItem.supports(type)` check first. Custom formats use a type starting with `web ` (the rest must be a valid MIME type).

## 3. Read/paste
- `navigator.clipboard.readText()` needs the `clipboard-read` permission in Chromium (a prompt); Firefox and Safari instead show an ephemeral "Paste" context-menu prompt and require transient activation. Prefer listening to the `paste` event, which needs no permission:
```js
editor.addEventListener("paste", e => {
  const files = [...e.clipboardData.files];           // pasted screenshots
  const html = e.clipboardData.getData("text/html");
  if (files.length) { e.preventDefault(); upload(files); }
});
```
- Sanitise pasted HTML before inserting it.

## 4. Legacy fallback
`document.execCommand()` is deprecated; MDN says to prefer the Clipboard API. Use the legacy copy command only when the async API is missing.

## 5. Permissions Policy
For iframes that access the clipboard, the `clipboard-read` and `clipboard-write` Permissions-Policy features must be allowed (for example `allow="clipboard-write; clipboard-read"`).

## Verify
Test on Safari iOS and desktop, Firefox, Chromium; paste into a plain text editor and a rich editor to check both formats.

## Checked

Checked 2026-10-26 against the MDN Clipboard API, Clipboard.write(), ClipboardItem constructor and ClipboardItem.supports() pages (mdn/content main): secure-context requirement, per-browser activation and permission rules, always-supported MIME types, `web ` custom-format prefix, Promise values in ClipboardItem, execCommand deprecation, and iframe Permissions-Policy. Removed the unconfirmed Safari-synchronous-write and DOMPurify claims.

Method: documentation only; no commands were run.
