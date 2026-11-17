---
id: computing-software.systems-network-administration.linux.firewalld-rich-rules
name: firewalld-rich-rules
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, firewalld, firewall-cmd, rich-rule, firewalld-rich-rules, source-restriction, rate-limit, firewalld-logging, port-forward, rhcsa, rhce, security, sysadmin]
level: practitioner
status: docs-checked
description: "Write firewalld rich rules for what zones and services can't express: per-source service access, reject vs drop, rate-limited logging, port forwarding, and priority ordering."
sources:
  - https://firewalld.org/documentation/man-pages/firewalld.richlanguage.html
  - https://firewalld.org/documentation/man-pages/firewall-cmd.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# firewalld rich rules

**Goal:** allow SSH only from the admin network, block one noisy host, log what is
dropped — without leaving the firewalld model or hand-writing nft.

## 1. Syntax
```
rule [family="ipv4|ipv6"] [priority="N"]
     [source [not] address="CIDR" | ipset="name" | mac="..."]
     [destination [not] address="CIDR"]
     [service name="ssh" | port port="8443" protocol="tcp" | protocol value="icmp" | forward-port ... | masquerade | icmp-block name="..."]
     [log [prefix="..."] [level="info"] [limit value="3/m"]] [audit]
     [accept | reject [type="icmp-admin-prohibited"] | drop | mark set="..."]
```
`family` is mandatory whenever a source or destination address is used, and for port or packet forwarding; without it a rule applies to IPv4 and IPv6. `log` takes `limit value="rate/duration"` and an optional `burst`; the default log level is `warning`.

## 2. Common rules
```bash
Z=public
# SSH only from the admin subnet (remove the open service first)
firewall-cmd --permanent --zone=$Z --remove-service=ssh
firewall-cmd --permanent --zone=$Z --add-rich-rule='rule family="ipv4" source address="10.0.99.0/24" service name="ssh" accept'
# Block one host completely, quietly
firewall-cmd --permanent --zone=$Z --add-rich-rule='rule family="ipv4" source address="203.0.113.45" drop'
# Log and reject a port with rate-limited logging
firewall-cmd --permanent --zone=$Z --add-rich-rule='rule family="ipv4" port port="3306" protocol="tcp" log prefix="DB-DENY " level="warning" limit value="5/m" reject'
# Rate-limit new connections to HTTP
firewall-cmd --permanent --zone=$Z --add-rich-rule='rule service name="http" accept limit value="50/s"'
# Port forward 8080 → internal host 10.0.20.5:80 (needs masquerade for return traffic if routed)
firewall-cmd --permanent --zone=$Z --add-rich-rule='rule family="ipv4" forward-port port="8080" protocol="tcp" to-port="80" to-addr="10.0.20.5"'
firewall-cmd --reload
firewall-cmd --zone=$Z --list-rich-rules
```
Remove with `--remove-rich-rule='<exact same string>'` — the text must match the listed form.

## 3. Ordering
Without a priority (or priority 0), rich rules are placed by action in the zone chains log, deny, allow, so a `drop` for a host
beats an `accept` for its subnet regardless of insertion order. `priority` (range −32768..32767, lower = earlier)
sorts rules: negative values run before the other firewalld primitives, positive values after them. Use priorities when you need "allow this one host, deny the rest of its subnet":
```bash
firewall-cmd --permanent --add-rich-rule='rule priority="-10" family="ipv4" source address="10.0.5.7" service name="ssh" accept'
firewall-cmd --permanent --add-rich-rule='rule priority="-5" family="ipv4" source address="10.0.5.0/24" service name="ssh" reject'
```

## Gotchas
- Quoting: wrap the whole rule in single quotes; values in double quotes.
- Many per-IP rules don't scale — use an ipset (`--new-ipset`, `source ipset="blocklist"`).
- A rule only applies to traffic that reaches its zone; a source bound to another zone with `--add-source` is handled by that zone instead.
- `log` without `limit` can flood the journal under a scan.

## Verify
- [ ] `firewall-cmd --list-rich-rules --permanent` equals the runtime list after `--reload`.
- [ ] From an allowed and a disallowed source, a TCP connect to port 22 succeeds and fails respectively; the kernel log shows the `DB-DENY` prefix for logged denials.

## Checked

Date: 2026-10-25. Documentation release: firewalld man page sources (firewalld/firewalld master, doc/xml: firewall-cmd, firewalld.richlanguage, firewalld.zone, firewalld.zones, firewalld.ipset; latest release tag v2.5.2, read 2026-10-25).
Confirmed: rule grammar elements (family, priority, source address/mac/ipset with `not`, service, port, forward-port, masquerade, log with prefix/level/limit/burst, accept/reject/drop/mark with limit); family requirement; priority range -32768..32767 with lower values first and negative values before, positive after, the firewalld primitives; zone chains zone_pre, zone_log, zone_deny, zone_allow, zone_post; `--add-rich-rule`, `--remove-rich-rule`, `--list-rich-rules`.
Removed as unconfirmed: the Red Hat URL (not readable here) and wording about journal queries.

Method: documentation only; no commands were run.
