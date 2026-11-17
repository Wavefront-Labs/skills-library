---
id: computing-software.messaging-and-integration.ntfy.subscribe-filters
name: subscribe-filters
category: computing-software
field: messaging-and-integration
product: ntfy
tags: [ntfy, filters, priority, tags, subscribe]
level: practitioner
status: docs-checked
description: "Filter an ntfy subscription by id, message, title, priority or tags, and the AND versus OR matching rules."
sources:
  - https://raw.githubusercontent.com/binwiederhier/ntfy/main/docs/subscribe/api.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Subscription filters

Filters are case-insensitive and can be sent as HTTP headers or query parameters.

| Filter | Aliases | Matching |
|---|---|---|
| `id` | `X-ID` | exact message ID |
| `message` | `X-Message`, `m` | exact message string |
| `title` | `X-Title`, `t` | exact title string |
| `priority` | `X-Priority`, `prio`, `p` | any listed priority (OR), comma-separated |
| `tags` | `X-Tags`, `tag`, `ta` | all listed tags (AND), comma-separated |

```
curl -s "ntfy.sh/mytopic/json?priority=high,urgent"
curl -s "ntfy.sh/mytopic/json?tags=warning,backup"
```

The first returns messages with priority high OR urgent. The second only messages with both tags.

## Gotchas

- `message` and `title` are exact matches, not substring.
- Filters combine with `poll=1`, for example `ntfy.sh/mytopic/json?poll=1&id=pbkiz8SD7ZxG`.
- In the CLI client config the equivalent is the `if:` key, for example `priority: high,urgent`.

## Checked

2026-11-04. Confirmed against the ntfy subscribe API page (Filter messages table, OR for priority, AND for tags, all-parameters list) and CLI page (if: priority: high,urgent). Removed: the Verify step.
Method: documentation only; no commands were run.
