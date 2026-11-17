---
id: computing-software.web-development.frontend-development.pwa-share-target-and-file-handling
name: pwa-share-target-and-file-handling
category: computing-software
field: web-development
product: frontend-development
tags: [web-share-target, file-handling-api, protocol-handlers, launchqueue, pwa-capabilities, pwa]
level: practitioner
status: docs-checked
description: "Making an installed PWA a share target, file handler and protocol handler: manifest share_target, file_handlers with launchQueue, protocol_handlers, and support limits."
sources:
  - https://developer.mozilla.org/en-US/docs/Web/Progressive_web_apps/Manifest/Reference/share_target
  - https://developer.mozilla.org/en-US/docs/Web/Progressive_web_apps/Manifest/Reference/file_handlers
  - https://developer.mozilla.org/en-US/docs/Web/Progressive_web_apps/Manifest/Reference/protocol_handlers
  - https://developer.mozilla.org/en-US/docs/Web/API/Navigator/registerProtocolHandler
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Share target, file handling and protocol handlers

All three apply to **installed** PWAs (MDN). In browser-compat-data they are Chromium-only (share target from Chrome 89, protocol handlers 96, file handlers 102) and marked experimental, so treat them as enhancements.

## 1. Share target
```json
"share_target": {
  "action": "/share", "method": "POST", "enctype": "multipart/form-data",
  "params": { "title": "title", "text": "text", "url": "url",
              "files": [{ "name": "media", "accept": ["image/*", "video/*"] }] }
}
```
Handle the POST in the service worker (no server needed):
```js
self.addEventListener("fetch", e => {
  const url = new URL(e.request.url);
  if (e.request.method === "POST" && url.pathname === "/share") {
    e.respondWith((async () => {
      const form = await e.request.formData();
      await saveToIDB(form.getAll("media"), form.get("text"));
      return Response.redirect("/compose?shared=1", 303);
    })());
  }
});
```

## 2. File handling
```json
"file_handlers": [{ "action": "/open", "accept": { "text/csv": [".csv"], "application/json": [".json"] } }]
```
```js
if ("launchQueue" in window) launchQueue.setConsumer(async ({ files }) => {
  for (const handle of files) openFile(await handle.getFile());   // FileSystemFileHandle: can also write back
});
```

## 3. Protocol handlers
```json
"protocol_handlers": [{ "protocol": "web+notes", "url": "/open?link=%s" }]
```
The manifest `protocol` examples in MDN include `mailto`, `ms-word` and `web+jngl`. For the runtime equivalent, `navigator.registerProtocolHandler("web+notes", "/open?link=%s")`, a custom scheme must begin with `web+`, followed by at least one lowercase ASCII letter and nothing else, unless it is a safelisted scheme such as `mailto` or `magnet`. Decode and validate `%s` (it is attacker-controlled input).

## Verify
- [ ] DevTools > Application > Manifest lists share target / file handlers without errors.
- [ ] On Android, the installed app appears in the system share sheet and receives an image.

## Checked

Checked 2026-10-26 against mdn/content (main) manifest reference pages for `share_target`, `file_handlers` and `protocol_handlers`, Navigator.registerProtocolHandler and LaunchQueue, plus mdn/browser-compat-data.

- Confirmed: `share_target` requires `action` and `params`, supports `method` GET or POST, `enctype` for POST, and `params` of `title`, `text`, `url` and `files`; `file_handlers` entries require `action` and `accept` and are read at install time; `protocol_handlers` use `%s` for the URL; `launchQueue.setConsumer` is Chromium-only and experimental; `web+` scheme rule for `registerProtocolHandler`.
- Removed: the per-platform split (Android/ChromeOS versus desktop), the remark about apps placing the URL in `text`, and the OS prompt note. The Chrome developer pages were not readable and were dropped from sources.

Method: documentation only; no commands were run.
