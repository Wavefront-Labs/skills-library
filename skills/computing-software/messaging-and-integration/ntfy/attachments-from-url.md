---
id: computing-software.messaging-and-integration.ntfy.attachments-from-url
name: attachments-from-url
category: computing-software
field: messaging-and-integration
product: ntfy
tags: [ntfy, attachments, x-attach, url, external-file]
level: intro
status: docs-checked
description: "Attach a file hosted elsewhere to an ntfy message with the X-Attach header; ntfy size and expiry limits do not apply."
sources:
  - https://raw.githubusercontent.com/binwiederhier/ntfy/main/docs/publish.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Attaching a file by URL

Header `X-Attach` (aliases `Attach`, `a`) points to an external file.

```
curl -X POST -H "Attach: https://f-droid.org/F-Droid.apk" ntfy.sh/mydownloads
```

- The filename is derived from the URL; override it with `X-Filename`.
- ntfy does not host the file, so the size and expiry limits for uploaded attachments do not apply.

## When to use which

- Use `X-Attach` when the file already has a stable public URL.
- Use a PUT body (see the attachments-local-file skill) when the file only exists on the publishing machine.

## Gotchas

- The attachment appears in the JSON message as an `attachment` object with `name` and `url`; `type`, `size` and `expires` are only set for files uploaded to the ntfy server.

## Checked

2026-11-04. Confirmed against the ntfy publish page (Attach file from a URL) and the subscribe API page (attachment object fields). Removed: a client-support claim, a link-rot gotcha and the Verify step, not on the pages.
Method: documentation only; no commands were run.
