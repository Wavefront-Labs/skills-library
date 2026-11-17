---
id: computing-software.networking-hardware-and-wireless.bind9.rpz-triggers-and-actions
name: rpz-triggers-and-actions
category: computing-software
field: networking-hardware-and-wireless
product: bind9
tags: [networking-hardware-and-wireless, bind9, rpz, response-policy, policy-zone]
level: advanced
status: docs-checked
description: "BIND 9 response policy zones: up to 64 policy zones, five trigger types, and actions NXDOMAIN, NODATA, PASSTHRU, DROP and TCP-only."
sources:
  - https://bind9.readthedocs.io/en/latest/chapter6.html
  - https://bind9.readthedocs.io/en/latest/reference.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# rpz triggers and actions
Enable RPZ with `response-policy { zone "rpz.example.com"; };`. Up to 64 policy zones are allowed and are checked in order.

Triggers: `client-ip`, `qname`, `rpz-ip` (answer address), `rpz-nsdname` (name server name) and `rpz-nsip` (name server address).

Actions are set by the record in the policy zone:

- NXDOMAIN: `CNAME .`
- NODATA: `CNAME *.`
- PASSTHRU: `CNAME rpz-passthru.`
- DROP: `CNAME rpz-drop.`
- TCP-only: `CNAME rpz-tcp-only.`
- Local data: any other record.

A CNAME whose target is a wildcard such as `*.example.com.` is used as an ordinary CNAME with the asterisk replaced by the query name, which is useful for query logging on a walled garden's authoritative server.

## Checked

2026-11-04. Read the response-policy entry in the Administrator Reference Manual: 64 policy zone limit, trigger types and precedence order, and the CNAME encodings for PASSTHRU, DROP, TCP-only, NXDOMAIN, NODATA and local data confirmed. Corrected the wildcard CNAME sentence, which described it as redirecting a whole domain.

Method: documentation only; no commands were run.
