---
id: computing-software.email-administration.mailcow.mailcow-unbound-forwarder-and-redis-debugging
name: mailcow-unbound-forwarder-and-redis-debugging
category: computing-software
field: email-administration
product: mailcow
tags: [unbound, dns-forwarder, dnssec, external-dns, rbl-lookups, redis-cli, redis-monitor]
level: practitioner
status: docs-checked
description: "Point mailcow's Unbound resolver at an internal DNS service and inspect Redis with redis-cli MONITOR, KEYS and PING."
sources: ["https://docs.mailcow.email/manual-guides/Unbound/u_e-unbound-fwd/", "https://docs.mailcow.email/manual-guides/Redis/u_e-redis/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Unbound forwarding and Redis debugging in mailcow

Unbound: if you must use an external DNS service there are two methods.
- Method A: append a `forward-zone` with `name: "."` and one or more `forward-addr:` lines to `data/conf/unbound/unbound.conf`, then restart Unbound.
- Method B: copy `helper-scripts/docker-compose.override.yml.d/EXTERNAL_DNS/docker-compose.override.yml` to the mailcow directory, edit the IP, then `docker compose down` and `docker compose up -d`.
The docs warn against public resolvers (the 8.8.8.8 example is only an example): most blocklist servers limit requests from them, so many blacklist lookups fail. Only DNSSEC-validating DNS services work. The watchdog's `UNBOUND_THRESHOLD` checks that external names resolve and validate.

Redis: it is the key-value store for Rspamd settings and some mailcow data. Open a client with `docker compose exec redis-mailcow redis-cli`. Useful debugging commands inside it: `MONITOR` streams every request the server receives in real time (for example `SMEMBERS "BAYES_SPAM_keys"` calls from Rspamd), `KEYS <pattern>` lists matching keys (`KEYS *` for all) and `PING` tests the connection and answers `PONG`.

## Checked

2026-11-04. Confirmed on the Unbound and Redis pages: Method A forward-zone in data/conf/unbound/unbound.conf and restart of unbound-mailcow, Method B override file path, the public-resolver warning and DNSSEC-only requirement, redis-cli via redis-mailcow, and MONITOR, KEYS and PING. Removed: the claim about why mailcow runs its own resolver and the KEYS production warning (neither is on the pages). The UNBOUND_THRESHOLD sentence matches the Watchdog thresholds page.

Method: documentation only; no commands were run.
