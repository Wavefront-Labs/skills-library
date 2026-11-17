---
id: computing-software.networking-hardware-and-wireless.powerdns.ixfrdist-yml-settings
name: ixfrdist-yml-settings
category: computing-software
field: networking-hardware-and-wireless
product: powerdns
tags: [powerdns, ixfrdist, ixfrdist-yml, acl, work-dir, axfr-timeout, webserver]
level: practitioner
status: docs-checked
description: "Configure ixfrdist.yml: listen, acl, work-dir, keep, axfr-timeout, axfr-max-records, compress, tcp-in-threads, uid and gid, domains entries and webserver keys, with defaults."
sources:
  - https://raw.githubusercontent.com/PowerDNS/pdns/master/docs/manpages/ixfrdist.yml.5.rst
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ixfrdist.yml settings

Defaults in brackets.
- `listen` (`127.0.0.1:53`, `[::1]:53`): TCP and UDP; IPv6 with a port uses brackets.
- `acl` (`127.0.0.0/8`, `::1/128`): who may query and transfer; no netmask means one host.
- `axfr-max-records` (0, unlimited): caps accepted AXFR size to limit memory.
- `axfr-timeout` (20 s): raise for slow links or large zones.
- `failed-soa-retry` (30 s): wait between SOA retries for never-transferred zones.
- `compress` (false): smaller responses, more CPU and memory.
- `work-dir` (current directory): stored as `ZONE/SERIAL`; set it explicitly and make it writable for the run user.
- `keep` (20): older copies and IXFR diffs kept per domain.
- `tcp-in-threads` (10): caps concurrent downstream AXFRs.
- `uid`, `gid`: drop privileges after binding sockets.
- `domains` (mandatory list): each entry needs `domain` and `master` (IP to transfer from); optional `max-soa-refresh` (seconds) and `notify` destinations.
- `webserver-address` (unset, no webserver): setting it starts one. `webserver-acl` (`127.0.0.0/8`, `::1/128`). `webserver-loglevel` (`normal`; also `none` for errors only, `detailed` for full requests and responses).

## Checked

2026-11-04. Read manpages/ixfrdist.yml.5.rst in full and confirmed every option, default and mandatory key including listen, acl, axfr-max-records, axfr-timeout, failed-soa-retry, compress, work-dir, keep, tcp-in-threads, uid, gid, domains and the webserver keys. Nothing removed.

Method: documentation only; no commands were run.
