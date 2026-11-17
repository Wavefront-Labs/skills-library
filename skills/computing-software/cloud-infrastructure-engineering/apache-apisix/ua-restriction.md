---
id: computing-software.cloud-infrastructure-engineering.apache-apisix.ua-restriction
name: ua-restriction
category: computing-software
field: cloud-infrastructure-engineering
product: apache-apisix
tags: [apache-apisix, apisix, ua-restriction, user-agent, allowlist, denylist, bot-blocking, plugin]
level: intro
status: docs-checked
description: "Block or allow clients by User-Agent in APISIX with ua-restriction: allowlist or denylist regex, bypass_missing and the rejection message."
sources:
  - https://raw.githubusercontent.com/apache/apisix/master/docs/en/latest/plugins/ua-restriction.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ua-restriction

Attributes:
- `allowlist`: array of permitted user agents (regex supported).
- `denylist`: array of blocked user agents (regex supported).
- `bypass_missing`: false; true skips the check when no User-Agent header is sent.
- `message`: 1-1024 characters, default `Not allowed`.

Configure exactly one of `allowlist` or `denylist`.

```json
{
  "plugins": {
    "ua-restriction": {
      "bypass_missing": false,
      "denylist": ["bad-bot-1"],
      "message": "Blocked"
    }
  }
}
```

A rejected request receives HTTP 403 with a JSON body such as `{"message":"Blocked"}`.

## Checked

2026-11-04: read the ua-restriction plugin page; the attributes table (bypass_missing false, allowlist and denylist with regex and the exactly-one rule, message 1-1024 characters with default Not allowed) and the 403 JSON message response match. Reworded the allowlist or denylist rule to the page's wording.

Method: documentation only; no commands were run.
