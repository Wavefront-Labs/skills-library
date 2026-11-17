---
id: computing-software.systems-network-administration.linux.local-dns-caching-nscd-dnsmasq-resolved
name: local-dns-caching-nscd-dnsmasq-resolved
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, nscd, dns-cache, systemd-resolved, dnsmasq, resolvectl, negative-caching]
level: practitioner
status: docs-checked
description: "Choose and operate a local DNS cache on Linux (systemd-resolved, dnsmasq, nscd, unbound): enable, inspect hit rates, flush stale entries and avoid double caching."
sources:
  - https://www.freedesktop.org/software/systemd/man/latest/resolvectl.html
  - https://man7.org/linux/man-pages/man8/nscd.8.html
  - https://thekelleys.org.uk/dnsmasq/docs/dnsmasq-man.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Local DNS caching

glibc does **not** cache DNS: every `getaddrinfo()` hits the configured nameserver unless a local cache sits in front.

## Options
| Cache | Where | Use when |
|---|---|---|
| systemd-resolved | stub at 127.0.0.53 | per-link DNS, optional DNSSEC and DNS over TLS |
| dnsmasq | 127.0.0.1 or LAN | small routers, split DNS, also DHCP |
| unbound | 127.0.0.1 | validating recursive resolver, prefetch |
| nscd | glibc NSS layer | caches passwd, group, hosts, services and netgroup lookups |

## systemd-resolved
```bash
resolvectl status                   # per-link servers, DNSSEC, current server
resolvectl statistics               # resolver and validation statistics
resolvectl flush-caches             # flush
resolvectl query example.com
ls -l /etc/resolv.conf              # should link to /run/systemd/resolve/stub-resolv.conf
```
Settings in `/etc/systemd/resolved.conf`: `Cache=yes|no-negative`, `DNSStubListener=yes`. `Cache=no-negative` avoids caching NXDOMAIN while a new record propagates.

## dnsmasq as a cache
```ini
# /etc/dnsmasq.d/cache.conf
listen-address=127.0.0.1
cache-size=10000
no-resolv
server=192.0.2.53
server=/corp.example.com/10.0.0.53   # split DNS
neg-ttl=60
```
`kill -USR1 $(pidof dnsmasq)` triggers a cache dump to the log (dnsmasq documents this under `-q`/`-d`).

## nscd
```bash
nscd -i hosts               # invalidate hosts cache
```
In `/etc/nscd.conf`, `enable-cache <service> yes|no` switches each database's cache. nscd does not cache the shadow file.

## Pitfalls
- Two caches stacked (resolved -> dnsmasq -> unbound) multiply TTL confusion and hide which layer is stale; keep one.
- Applications may cache in-process; flushing the OS cache does not clear those.

## Verify
- [ ] Second `dig @127.0.0.53 example.com` shows a low query time and decreasing TTL.
- [ ] After changing a record, `resolvectl flush-caches` makes the new value appear immediately.

## Checked
2026-10-27. Checked against systemd resolvectl(1), resolved.conf(5) and systemd-resolved.service(8) (current main), man-pages nscd(8) and nscd.conf(5) (mirror revisions dated 2015 and 2020), and the dnsmasq man page (updated 2025-02-05). Confirmed: resolvectl status, statistics, flush-caches, query; Cache= values yes, no-negative and no, DNSStubListener=; dnsmasq listen-address, cache-size (default 150 names), no-resolv, server=/domain/ip, neg-ttl and the SIGUSR1 cache dump; nscd invalidation with nscd -i database, per-database enable-cache, and that shadow is not cached. Removed: the nscd -g option, the SIGHUP cache-clear claim, the sssd interaction claim, the Java and container remarks and distribution defaults, which the documentation does not cover.

Method: documentation only; no commands were run.
