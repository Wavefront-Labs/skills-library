---
id: computing-software.systems-network-administration.linux.bind-query-logging
name: bind-query-logging
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, bind, bind9, named, named-logging, query-log, logging-channels, rndc-querylog, dnstap, dns-server, troubleshooting, sysadmin]
level: practitioner
status: docs-checked
description: "Configure BIND logging: channels and categories, separate query, security and transfer logs with rotation, toggling query logging with rndc, and dnstap for high-volume capture."
sources:
  - https://bind9.readthedocs.io/en/latest/reference.html
  - https://bind9.readthedocs.io/en/latest/manpages.html
  - https://github.com/isc-projects/bind9/blob/main/doc/arm/logging-categories.inc.rst
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# BIND query logging and log channels

**Goal:** know who asked what, which transfers ran and what was refused — in separate,
rotated files — without slowing a busy server.

## 1. logging block
```
logging {
    channel default_log {
        file "/var/log/named/default.log" versions 5 size 50m;
        severity info;
        print-time yes; print-severity yes; print-category yes;
    };
    channel query_log {
        file "/var/log/named/queries.log" versions 10 size 100m;
        severity info;
        print-time iso8601-utc;
    };
    channel security_log { file "/var/log/named/security.log" versions 5 size 20m; severity info; print-time yes; };
    channel xfer_log     { file "/var/log/named/xfer.log" versions 5 size 20m; severity info; print-time yes; };

    category default      { default_log; };
    category queries      { query_log; };
    category query-errors { query_log; };
    category security     { security_log; };       # denied queries, transfers, updates
    category xfer-in      { xfer_log; };
    category xfer-out     { xfer_log; };
    category notify       { xfer_log; };
    category lame-servers { null; };              # noise on recursive servers
};
```
`versions N size S` makes named rotate its own files — do not add logrotate for them as well.
Create the directory writable by the user `named` runs as (the user name and any SELinux label are distro-specific).

## 2. Turning query logging on/off
```bash
rndc querylog on       # "rndc querylog" without an argument toggles (backward compatible); also: options { querylog yes; };
rndc status            # server status
rndc querylog off
```
At startup, directing `category queries` to a channel also enables query logging unless the `querylog` option is set. `rndc responselog on` additionally logs the rcode of earlier queries.
A line looks like:
`client @0x7f91b8005490 127.0.0.1#62536 (www.example.com): query: www.example.com IN AAAA +E(0)K (127.0.0.1)`
Flags: `+`/`-` recursion desired set/not set, `S` signed, `E(#)` EDNS version, `T` TCP, `D` DO bit, `C` CD bit, `V` valid server cookie, `K` client cookie without a valid server cookie; then the destination address.

## 3. High volume: dnstap
For permanent capture use dnstap, which needs a BIND build with dnstap support (`fstrm` and `protobuf-c`):
```
options { dnstap { auth; client response; resolver query; }; dnstap-output file "/var/log/named/dnstap.fstrm" size 100m versions 5; };
```
`dnstap-output` is set only in `options` and cannot be changed by `rndc reload`/`reconfig` once set. Read with `dnstap-read -y <file>` (detailed YAML; the default is a short summary).

## 4. Useful greps
```bash
grep -c 'query:' queries.log                                  # volume
awk '/query:/{print $(NF-3)}' queries.log | sort | uniq -c | sort -rn | head   # top names (position varies by version; test)
grep 'denied' security.log                                    # refused recursion/transfers
grep 'Transfer status' xfer.log
```

## Gotchas
- If named does not start after a logging change, check the journal and that the log directory is writable by named's user.
- `severity dynamic` follows the server's global debug level, so it is handy for temporary debug detail.

## Verify
- [ ] After `rndc querylog on`, a `dig @server name` appears in queries.log with the client IP.
- [ ] A refused transfer from an unauthorised host appears in security.log; files rotate at the configured size.

## Checked
Checked 2026-10-27 against the BIND 9 Administrator Reference source (github.com/isc-projects/bind9, main branch, doc/arm and bin/rndc, bin/tools).
- Specifying the `queries` category enables query logging at startup unless `querylog` is set; `rndc querylog [on|off]` toggles when given no argument. The earlier statement that the category alone does not start logging was wrong.
- Query log flag letters (`+`/`-`, `S`, `E(#)`, `T`, `D`, `C`, `V`, `K`) and example line format are from the logging-categories page.
- `print-time` accepts `iso8601-utc`; `severity dynamic` follows the global debug level; `null` channel; categories `security`, `xfer-in`, `xfer-out`, `notify`, `lame-servers`, `query-errors`.
- `dnstap` and `dnstap-output ... size ... versions` are options-level; `dnstap-read -y` prints YAML.
- Removed unconfirmed claims: throughput cost, distro user names and SELinux labels, chroot path, `rndc status` wording.
Method: documentation only; no commands were run.
