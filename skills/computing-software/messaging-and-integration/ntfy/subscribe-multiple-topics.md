---
id: computing-software.messaging-and-integration.ntfy.subscribe-multiple-topics
name: subscribe-multiple-topics
category: computing-software
field: messaging-and-integration
product: ntfy
tags: [ntfy, multiple-topics, subscribe, ordering, comma-separated]
level: practitioner
status: docs-checked
description: "Subscribe to several ntfy topics in one request, the 150 topic cap, and the message ordering caveat."
sources:
  - https://raw.githubusercontent.com/binwiederhier/ntfy/main/docs/subscribe/api.md
  - https://raw.githubusercontent.com/binwiederhier/ntfy/main/docs/troubleshooting.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Multiple topics in one request

Comma-separate topics in the URL:

```
curl -s ntfy.sh/mytopic1,mytopic2/json
```

- Up to 150 distinct topics; duplicates are ignored.
- The `open` event lists topics as a comma-separated string; other events carry a single `topic`.

## Ordering gotcha

Replayed messages across topics are ordered by `time`, which has one-second granularity. Order between topics within the same second is undefined. If you need a total order, sort by `time` and fall back to the order received. Each topic's own messages stay in publish order.

## One 403 blocks all

Because all topics share one request, one topic returning `403 Forbidden` fails the whole request. On mobile (self-hosted) all topics can show "Reconnecting" and notifications arrive late (30+ minutes). Every subscribed topic must be readable by the logged-in user or `everyone`.

## Checked

2026-11-04. Confirmed against the ntfy subscribe API page (Subscribe to multiple topics: 150 cap, duplicates, ordering by time) and troubleshooting page (Reconnecting, single 403 blocks the joined request). Removed: the Verify commands.
Method: documentation only; no commands were run.
