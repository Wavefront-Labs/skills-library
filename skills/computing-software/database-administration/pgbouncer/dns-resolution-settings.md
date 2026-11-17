---
id: computing-software.database-administration.pgbouncer.dns-resolution-settings
name: dns-resolution-settings
category: computing-software
field: database-administration
product: pgbouncer
tags: [pgbouncer, dns, dns-max-ttl, c-ares, resolv-conf]
level: advanced
status: docs-checked
description: "dns_max_ttl, dns_nxdomain_ttl, dns_zone_check_period, resolv_conf and DNS backend facts such as EDNS0 and c-ares."
sources:
  - https://www.pgbouncer.org/config.html
  - https://www.pgbouncer.org/install.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: tune how PgBouncer caches and refreshes DNS.

PgBouncer resolves host names at connect time, which requires an asynchronous DNS implementation.

- `dns_max_ttl` (default 15.0 s): how long lookups are cached. The actual DNS TTL is ignored.
- `dns_nxdomain_ttl` (default 15.0 s): how long DNS errors and NXDOMAIN results are cached.
- `dns_zone_check_period` (default 0.0, disabled): period to check whether a zone serial changed. PgBouncer collects zones from host names (everything after the first dot); on a change all names under the zone are looked up again, and connections whose IP changed are invalidated. Works only with the c-ares backend (`--with-cares`).
- `resolv_conf` (default empty, OS defaults): custom resolv.conf path for DNS servers and options. Requires evdns (>= 2.0.3) or c-ares (>= 1.15.0); the library parses the file.

Backend comparison from the install docs: c-ares is parallel, supports EDNS0, /etc/hosts and SOA lookup; evdns (libevent 2.x) lacks EDNS0 and SOA lookup and does not check /etc/hosts updates; getaddrinfo_a (glibc 2.9+) and plain getaddrinfo lack SOA lookup, and getaddrinfo is not parallel and needs pthreads. EDNS0 is required for more than 8 addresses behind one name; enable it by adding `options edns0` to /etc/resolv.conf. c-ares is used by default if found; force with `--with-cares` or disable with `--without-cares`.

Inspect the cache with SHOW DNS_HOSTS and SHOW DNS_ZONES. When a host's resolution changes, existing server connections close on release and new ones use the new address.

## Checked

2026-11-03. Settings, defaults, values, console commands and column names were checked against the official PgBouncer pages cited in `sources` (config, usage, faq, install; fetched this batch), reading the prose against the page text. No wrong claims were found; nothing was removed.

Method: documentation only; no commands were run.
