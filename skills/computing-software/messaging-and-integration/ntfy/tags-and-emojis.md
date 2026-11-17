---
id: computing-software.messaging-and-integration.ntfy.tags-and-emojis
name: tags-and-emojis
category: computing-software
field: messaging-and-integration
product: ntfy
tags: [ntfy, tags, emoji, x-tags, headers]
level: intro
status: docs-checked
description: "Add ntfy tags with X-Tags; short codes that match emoji become emoji, other tags are listed under the notification."
sources:
  - https://raw.githubusercontent.com/binwiederhier/ntfy/main/docs/publish.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Tags and emojis

Header: `X-Tags` with aliases `Tags`, `Tag`, `ta`. Value is a comma-separated list.

```
curl -H "X-Tags: warning,mailsrv13,daily-backup" -d "Backup of mailsrv13 failed" ntfy.sh/backups
```

- A tag that matches an emoji short code (`warning`, `rotating_light`, `skull`, `+1`, `-1`, `tada`) is converted and prepended to the title, or to the message if there is no title.
- Tags that do not match an emoji are listed below the notification text.
- Supported on Android, Apple and Firefox.

## Gotchas

- Non-ASCII tags need RFC 2047 encoding, either for the whole header or per tag (same scheme as titles).
- All tags together are limited to 512 bytes by default; exceeding it returns HTTP 400.
- Subscribers can filter on tags with `?tags=a,b`, which matches only messages having all listed tags.

## Checked

2026-11-04. Confirmed against the ntfy publish page (Tags and emojis: aliases, emoji conversion, other tags listed below, RFC 2047 note, limits table). Removed: the Verify step.
Method: documentation only; no commands were run.
