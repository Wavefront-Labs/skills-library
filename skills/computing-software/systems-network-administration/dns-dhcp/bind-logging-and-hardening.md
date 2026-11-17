---
id: computing-software.systems-network-administration.dns-dhcp.bind-logging-and-hardening
name: bind-logging-and-hardening
category: computing-software
field: systems-network-administration
product: dns-dhcp
tags: [dns, bind, named-conf, bind-logging, logging-channels, logging-categories, querylog, bind-hardening, version-hiding, allow-query, allow-transfer, minimal-responses, chroot, apparmor, blackhole, query-logging]
level: practitioner
status: docs-checked
description: "Set up useful BIND logging (channels, categories, query/security logs with rotation) and harden named: query/transfer/recursion ACLs, version hiding, sandboxing."
sources:
  - https://bind9.readthedocs.io/en/latest/reference.html
  - https://kb.isc.org/docs/bind-best-practices-authoritative
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# BIND logging and hardening

## Logging
```
logging {
    channel default_log { file "/var/log/named/default.log" versions 5 size 20m; severity info; print-time yes; print-category yes; print-severity yes; };
    channel security_log { file "/var/log/named/security.log" versions 5 size 20m; print-time yes; };
    channel xfer_log { file "/var/log/named/xfer.log" versions 3 size 10m; print-time yes; };
    channel dnssec_log { file "/var/log/named/dnssec.log" versions 3 size 10m; print-time yes; };
    channel query_log { file "/var/log/named/query.log" versions 5 size 100m; print-time yes; };
    channel syslog_out { syslog daemon; severity warning; };
    category default { default_log; syslog_out; };
    category security { security_log; };          // approval and denial of requests
    category xfer-in { xfer_log; }; category xfer-out { xfer_log; }; category notify { xfer_log; };
    category dnssec { dnssec_log; };
    category queries { query_log; };              // only active when querylog on
    category lame-servers { null; };              // noisy on resolvers
};
```
`rndc querylog on|off` toggles query logging; the `queries` category also enables it at startup unless the `querylog` option is set. It is costly at high QPS; consider dnstap for analytics. Ensure `/var/log/named` is writable by `named` and permitted by AppArmor/SELinux.

## Hardening checklist
```
acl trusted { 10.0.0.0/8; };
options {
    version "not disclosed";        // hide 'version.bind' (does not stop fingerprinting, reduces noise)
    hostname none; server-id none;
    allow-query { any; };           // authoritative public; 'trusted' for internal servers
    allow-transfer { none; };       // per zone: key-based to secondaries only
    allow-recursion { none; };      // authoritative-only servers: also 'recursion no;'
    allow-update { none; };
    minimal-responses yes;          // smaller answers, less amplification
    blackhole { 192.0.2.0/24; };    // no queries accepted from, none sent to these (not '!addr' to block others)
};
```
- Separate authoritative and recursive roles onto different servers/views.
- Run as an unprivileged user (`named -u <user>`); keep AppArmor/SELinux profiles on.
- `rndc` key with restricted `controls { inet 127.0.0.1 allow { localhost; } keys { rndc-key; }; };`.
- TSIG for transfers/NOTIFY/updates; `rate-limit` (RRL) on authoritative servers; patch promptly using ISC's security advisories.
- `named-checkconf -z` in CI before deploy.

## Verify
- [ ] `dig @server version.bind chaos txt` returns the masked string.
- [ ] Transfer attempt without TSIG logged in security.log and refused.
- [ ] Logs rotate and contain category/severity fields.

## Checked

Date: 2026-10-26. BIND 9 ARM sources in isc-projects/bind9 (main, 9.21 development line, latest tag v9.21.27, plus the bind-9.20 branch grammar), read on 2026-10-26. Confirmed: logging channel grammar (file versions/size, severity, print-*, syslog, null), category names (default, security, xfer-in, xfer-out, notify, dnssec, queries, lame-servers), rndc querylog on|off, querylog option, options-level allow-query/allow-transfer/allow-recursion/allow-update, blackhole semantics, minimal-responses, server-id/hostname none, controls grammar. Removed the unconfirmed chroot and CVE-list statements.

Method: documentation only; no commands were run.
