---
id: computing-software.messaging-and-integration.ntfy.deprecations
name: deprecations
category: computing-software
field: messaging-and-integration
product: ntfy
tags: [ntfy, deprecations, env-topic, since-id, upgrade]
level: practitioner
status: docs-checked
description: "ntfy deprecations and behaviour changes: no active ones, plus the past env-topic, since-id and bare ntfy changes to avoid."
sources:
  - https://raw.githubusercontent.com/binwiederhier/ntfy/main/docs/deprecations.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Deprecations

The docs list no active deprecations. Previous ones:

## `ntfy publish --env-topic`

Active since 2022-06-20, behaviour changed in v1.30.1. The flag is being removed; `NTFY_TOPIC` still sets the topic.

```
NTFY_TOPIC=mytopic ntfy publish "this is the message"
```

## Android `since=<id>`

From Android app v1.14.0 the app uses `since=<id>` instead of a timestamp and does not work with servers older than v1.16.0. The `since=<timestamp>` endpoint still works. Run server v1.16.0 or newer with that app.

## Android WebSockets default (cancelled)

The planned switch to WebSockets was dropped on 2022-06-20; JSON stream remains the default. Nothing to do.

## Bare `ntfy`

Deprecated 2021-12-17, changed in v1.10.0: running `ntfy` alone no longer starts the server, including in Docker images. Use `ntfy serve`.

## Gotcha

The page says the bare-`ntfy` change also applies to Docker images; use `ntfy serve` wherever plain `ntfy` ran the server.

## Checked

2026-11-04. Confirmed against the ntfy deprecations page: no active deprecations, `--env-topic`, Android `since=<id>`, cancelled WebSockets default, `ntfy serve`, versions and dates. Removed: a claim about unit files and the Verify step.
Method: documentation only; no commands were run.
