---
id: computing-software.messaging-and-integration.ntfy.rate-limit-config
name: rate-limit-config
category: computing-software
field: messaging-and-integration
product: ntfy
tags: [ntfy, rate-limit, visitor-limits, burst, replenish]
level: advanced
status: docs-checked
description: "Tune ntfy server rate limits: the visitor-* keys, their defaults, exempt hosts and the proxy dependency."
sources:
  - https://raw.githubusercontent.com/binwiederhier/ntfy/main/docs/config.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Rate limit configuration

| Key | Default |
|---|---|
| `global-topic-limit` | 15,000 |
| `visitor-subscription-limit` | 30 |
| `visitor-request-limit-burst` | 60 |
| `visitor-request-limit-replenish` | 5s |
| `visitor-request-limit-exempt-hosts` | empty |
| `visitor-email-limit-burst` | 16 |
| `visitor-email-limit-replenish` | 1h |
| `visitor-topic-creation-limit-burst` | 100 (0 disables) |
| `visitor-topic-creation-limit-replenish` | 1m |
| `visitor-attachment-total-size-limit` | 100M |
| `visitor-attachment-daily-bandwidth-limit` | 500M |
| `visitor-prefix-bits-ipv4` | 32 |
| `visitor-prefix-bits-ipv6` | 64 |

Also `visitor-message-daily-limit`, `visitor-subscriber-rate-limiting`, `message-size-limit` (default `4K`) and `message-delay-limit` (default `3d`).

```yaml
visitor-request-limit-exempt-hosts: "example.com"
```

## Gotchas

- Behind a proxy set `behind-proxy: true` or every visitor is the same IP.
- IPv6 visitors are grouped by prefix (default /64).
- `message-size-limit` of 4K is recommended because FCM and APNS have limits around 4 KB.
- `auth-access-cache: true` caches ACL checks in memory on high-volume servers.
- Servers sharing a database need synced clocks.

## Checked

2026-11-04. Confirmed against the ntfy config page (Rate limiting sections, config table): every key and default, IPv6 /64 grouping, message-size-limit 4K/FCM note, auth-access-cache, shared-database clock sync, HTTP 429 on limit. Removed: the Verify burst test.
Method: documentation only; no commands were run.
