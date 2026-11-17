---
id: computing-software.systems-network-administration.pi-hole.dns-rate-limiting
name: dns-rate-limiting
category: computing-software
field: systems-network-administration
product: pi-hole
tags: [rate-limit, refused-reply, per-client-limit]
level: practitioner
status: docs-checked
description: "Understand FTL's per-client rate limiting (1000 queries per 60 seconds), its log messages, and how to change or disable it."
sources: ["https://docs.pi-hole.net/ftldns/configfile/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# DNS rate limiting

FTL limits each client independently. By default no more than **1000 queries in 60 seconds** are allowed; excess queries are answered with `REFUSED` and not processed further. Other clients keep working.

**Settings**

- `dns.rateLimit.count` (default `1000`): queries allowed per interval.
- `dns.rateLimit.interval` (default `60`): interval in seconds.

Example, one query per hour: `count = 1`, `interval = 3600`. Setting both values to zero disables rate limiting.

**How the window works.** The interval is relative to when FTL finished starting and advances in steps of the interval. A client that reaches the maximum is blocked until the end of the current interval. If it keeps sending enough queries while blocked, it stays blocked through the next interval. Once it requests fewer than the limit, it is unblocked.

**Log messages** in `/var/log/pihole/FTL.log`:

```text
Rate-limiting 10.0.1.39 for at least 44 seconds
Still rate-limiting 10.0.1.39 as it made additional 5007 queries
Ending rate-limitation of 10.0.1.39
```

**Checklist**

1. Search `FTL.log` for "Rate-limiting" when a device loses DNS.

## Checked

2026-11-03. Read the `dns.rateLimit` section of the FTL configuration reference: 1000 queries in 60 seconds, per-client, REFUSED reply, count 1 with interval 3600 example, both zero disables, interval mechanics, and the three FTL.log messages. Removed the advice items about raising the count for proxies and servers (not in the page).

Method: documentation only; no commands were run.
