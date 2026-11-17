---
id: computing-software.messaging-and-integration.ntfy.message-title
name: message-title
category: computing-software
field: messaging-and-integration
product: ntfy
tags: [ntfy, title, x-title, rfc-2047, headers]
level: intro
status: docs-checked
description: "Set an ntfy message title with the X-Title header and handle non-ASCII titles with RFC 2047 encoding."
sources:
  - https://raw.githubusercontent.com/binwiederhier/ntfy/main/docs/publish.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Message title

Header: `X-Title`, with aliases `Title`, `ti`, `t`. The default title is the topic short URL such as `ntfy.sh/mytopic`.

```
curl -H "Title: Dogs are better than cats" -d "Oh my ..." ntfy.sh/controversial
```

Supported on Android, Apple and Firefox clients.

## Non-ASCII titles

Some HTTP clients mangle non-ASCII header values and clients then show `?`. Encode the value as RFC 2047:

- Base64: `=?UTF-8?B?8J+HqfCfh6o=?=`
- Quoted-printable: `=?UTF-8?Q?=C3=84pfel?=`

## Limits

The limits table says the title is limited to 1 KB and all tags combined to 512 bytes; requests exceeding either are rejected with HTTP 400.

## Checked

2026-11-04. Confirmed against the ntfy publish page (Message title, RFC 2047 note, limits table): header and aliases, default title, platform marker, both encoding examples, size limits and HTTP 400. Removed: the words "by default" on the limit, and the Verify step.
Method: documentation only; no commands were run.
