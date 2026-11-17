---
id: computing-software.collaboration-platform-administration.zulip.tornado-sharding-configuration
name: tornado-sharding-configuration
category: computing-software
field: collaboration-platform-administration
product: zulip
tags: [tornado-sharding, refresh-sharding, realm-hosts, event-queue]
level: sme
status: docs-checked
description: "Shard Zulip's Tornado real-time service by organization hostname, regex or multi-port large realm in zulip.conf, then apply with refresh-sharding-and-restart."
sources: ["https://zulip.readthedocs.io/en/latest/production/system-configuration.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Tornado sharding

Tornado handles real-time push. One instance serves roughly 1000 to 1500 concurrent active users depending on message volume. The `[tornado_sharding]` section of `/etc/zulip/zulip.conf` sets how many instances run and which organizations map to them. Instances listen on ports starting at 9800.

Assign organizations by subdomain, or by full hostname for organizations using `REALM_HOSTS`:

```
[tornado_sharding]
9800 = realm-a realm-b
9801 = realm-c
9802 = realm-host.example.net
```

Or by regular expression over the fully-qualified hostname:

```
[tornado_sharding]
9800_regex = ^realm-(a|b)\.example\.com$
9801_regex = ^other(-option)?\.example.com$
```

A very large single organization can span shards by joining ports with an underscore:

```
[tornado_sharding]
9800 = small-realm
9801_9802 = very-large-realm
```

Applying takes two steps: first `scripts/zulip-puppet-apply`, then a separate `scripts/refresh-sharding-and-restart`. Sharding changes do not take effect without the second.

## Checked

2026-11-08. Checked: read against the Zulip system-configuration page (docs/production/system-configuration.md, read in full). Removed: a closing paragraph about when to shard and per-realm mapping that the page does not state.

Method: documentation only; no commands were run.
