---
id: computing-software.networking-hardware-and-wireless.powerdns.lua-records-setup
name: lua-records-setup
category: computing-software
field: networking-hardware-and-wireless
product: powerdns
tags: [powerdns, lua-records, enable-lua-records, shared-state, include, record-syntax]
level: practitioner
status: docs-checked
description: "Enable and write PowerDNS LUA records: global or per-zone enabling, shared state, syntax, include(), and trust, AXFR, DNSSEC caveats."
sources:
  - https://raw.githubusercontent.com/PowerDNS/pdns/master/docs/lua-records/index.rst
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# LUA records setup

Enable:
- `enable-lua-records` in config (enables all zones), or `enable-lua-records=shared` for all zones with Lua state reuse (one state per UDP thread plus one for TCP; the docs cite up to 10x QPS in non-scientific tests). By default every query gets a fresh state.
- Per zone: metadata `ENABLE-LUA-RECORDS` set to `1`.
- `enable-lua-record-updates`: only if needed.
- The geoip backend must be in `launch` for geographic functions.

Syntax: `<name> IN LUA <selector-type> "<lua snippet>"`. The snippet is evaluated as the argument of `return`; start it with `;` to write a full script with its own `return`. Use type `LUA` itself for config records holding variables, loaded elsewhere with `include('recordname')`. `qname` is available (`qname:toString()`); `qtype` is not. TTLs are honoured.

Caveats:
- Never serve LUA records from untrusted zones; use TSIG on AXFR even from trusted sources.
- LUA records cannot be queried directly, and servers without support serve them as plain data, leaking content.
- Keep each quoted segment of a long snippet to 255 bytes or less, or AXFR chunking can break the code.
- Answers are signed on the fly, so the key must be on the answering server; presigned zones cannot hold LUA records.
- On gmysql and gpgsql, double single quotes (`''`) in INSERT/UPDATE.
- Health checks run asynchronously in the background.

## Checked

2026-11-08. Read in full: PowerDNS docs lua-records/index.rst. Confirmed enabling globally or per zone with ENABLE-LUA-RECORDS, the shared state model and its 10x claim, geoip in launch, the record syntax and semicolon full-script form, include(), qname and qtype, TTLs, the AXFR 255 byte warning, the trust, TSIG and enable-lua-record-updates note, the pre-signed zone limit, direct-query refusal, non-supporting servers and the SQL quote doubling. Removed the unconfirmed true/1 values for the setting.

Method: documentation only; no commands were run.
