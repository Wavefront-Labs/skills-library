---
id: computing-software.messaging-and-integration.ntfy.publish-basics
name: publish-basics
category: computing-software
field: messaging-and-integration
product: ntfy
tags: [ntfy, publish, curl, post, put, topic]
level: intro
status: docs-checked
description: "Publish an ntfy notification with curl or the ntfy CLI over HTTP POST or PUT; topics are created on the fly with no sign-up."
sources:
  - https://raw.githubusercontent.com/binwiederhier/ntfy/main/docs/publish.md
  - https://raw.githubusercontent.com/binwiederhier/ntfy/main/docs/deprecations.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Publishing to ntfy

Send with HTTP POST or PUT, or the ntfy CLI.

```
curl -d "Backup successful" ntfy.sh/mytopic
ntfy publish mytopic "Backup successful"
```

- Topics are created on the fly. There is no sign-up, so on an open server the topic name acts as the password.
- The request body is the message. Everything else (title, priority, tags, delay) is a header or query parameter; see the other publish skills.
- Message bodies over 4,096 bytes (default) or containing non-UTF-8 data are turned into attachments.
- On a self-hosted server use the full URL, for example `https://ntfy.example.com/mytopic`.
- `NTFY_TOPIC=mytopic ntfy publish "msg"` sets the topic from the environment; the `--env-topic` flag is deprecated and not needed.

## Gotchas

- A guessable topic name means anyone can read or post to it. Topic names allow only letters, numbers, underscores and dashes, up to 64 characters.
- The ntfy CLI does not support DELETE; use curl for cancelling or deleting.
- Header names are case-insensitive; query parameter names must be lowercase.

## Checked

2026-11-04. Confirmed against the ntfy publish page (Picking a topic, attachments for >4,096 bytes or non-UTF-8, parameter case rules, CLI DELETE note) and deprecations page (NTFY_TOPIC, --env-topic). Removed: the Verify step.
Method: documentation only; no commands were run.
