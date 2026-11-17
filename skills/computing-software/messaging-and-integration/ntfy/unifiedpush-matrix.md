---
id: computing-software.messaging-and-integration.ntfy.unifiedpush-matrix
name: unifiedpush-matrix
category: computing-software
field: messaging-and-integration
product: ntfy
tags: [ntfy, unifiedpush, matrix, push-gateway, up]
level: advanced
status: docs-checked
description: "Use ntfy as a UnifiedPush distributor and Matrix push gateway, including the up header and ACLs needed on a private server."
sources:
  - https://raw.githubusercontent.com/binwiederhier/ntfy/main/docs/publish.md
  - https://raw.githubusercontent.com/binwiederhier/ntfy/main/docs/config.md
  - https://raw.githubusercontent.com/binwiederhier/ntfy/main/docs/subscribe/phone.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# UnifiedPush and Matrix

ntfy can act as a UnifiedPush distributor: apps that support UnifiedPush send messages through ntfy topics. On Android, select ntfy as the distributor in a supported app, optionally with your own server.

## Header

Apps set the `X-UnifiedPush` header or query parameter (aliases `unifiedpush`, `up`) to `1`. This is mostly equivalent to `Firebase: no`, and it auto-detects message encoding: binary messages are base64-encoded.

## Matrix gateway

ntfy accepts Matrix push at `/_matrix/push/v1/notify` and forwards each message to the ntfy topic in the message's `pushkey`. It works only with UnifiedPush and ntfy, so it is not a generic Matrix push gateway.

## Private server

UnifiedPush needs anonymous write access to its topics, which all start with `up`. Under `auth-default-access: "deny-all"`, allow the prefix (or each topic explicitly, for example `ntfy access '*' upYzMtZGZiYTY5 write-only`):

```
ntfy access '*' 'up*' write-only
```

Your user must be able to read `up*` as well.

## Gotchas

- Without that write access the application server cannot publish to its `up*` topic.
- One 403 topic blocks a multi-topic subscription; see troubleshooting-reconnecting.

## Checked

2026-11-04. Confirmed against the ntfy publish page (UnifiedPush header and aliases, base64 for binary, Matrix gateway endpoint, pushkey, not generic), config page (up* write-only ACL example) and phone page (select ntfy as distributor). Removed: the silent-failure claim and the Verify curl.
Method: documentation only; no commands were run.
