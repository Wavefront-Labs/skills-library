---
id: computing-software.cloud-infrastructure-engineering.apache-apisix.uri-blocker
name: uri-blocker
category: computing-software
field: cloud-infrastructure-engineering
product: apache-apisix
tags: [apache-apisix, apisix, uri-blocker, block-rules, regex, security, plugin]
level: intro
status: docs-checked
description: "Reject requests by URI pattern in APISIX with uri-blocker: block_rules regex list, rejected_code, rejected_msg and case_insensitive."
sources:
  - https://raw.githubusercontent.com/apache/apisix/master/docs/en/latest/plugins/uri-blocker.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# uri-blocker

Attributes:
- `block_rules` (required): array of regex patterns matched against the request URI.
- `rejected_code`: default 403, minimum 200.
- `rejected_msg`: response body; must be non-empty if set.
- `case_insensitive`: false by default.

If the URI matches any pattern the request ends with `rejected_code`.

```json
{
  "uri": "/*",
  "plugins": {
    "uri-blocker": {
      "block_rules": ["admin\\.php", "secret.*"],
      "rejected_code": 404,
      "rejected_msg": "Not found",
      "case_insensitive": true
    }
  }
}
```

## Checked

2026-11-04: read the uri-blocker plugin page; block_rules (required, regex list), rejected_code default 403 with minimum 200, rejected_msg non-empty, case_insensitive default false, and the terminate-on-match behaviour match. Removed the unstated advice about escaping dots in JSON strings.

Method: documentation only; no commands were run.
