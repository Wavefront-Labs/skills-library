---
id: computing-software.networking-hardware-and-wireless.unbound.rpz-triggers-and-actions
name: rpz-triggers-and-actions
category: computing-software
field: networking-hardware-and-wireless
product: unbound
tags: [networking-hardware-and-wireless, unbound, rpz, response-policy-zone, triggers, passthru, nxdomain]
level: advanced
status: docs-checked
description: "Understand RPZ policy content as Unbound supports it: the five trigger types, the actions and how addresses are written."
sources:
  - https://unbound.docs.nlnetlabs.nl/en/latest/topics/filtering/rpz.html
  - https://unbound.docs.nlnetlabs.nl/en/latest/manpages/unbound.conf.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# rpz triggers and actions
RPZ is a standard policy format written as DNS zone data, so policies can be shared and loaded by zone transfer. Unbound added RPZ in 1.10.0 (QNAME and Response IP triggers); 1.14.0 added the full trigger and action set.

Triggers (set by owner name):
- QNAME: the queried name.
- Client IP: suffix `.rpz-client-ip`.
- Response IP: suffix `.rpz-ip`.
- NSDNAME: suffix `.rpz-nsdname`.
- NSIP: suffix `.rpz-nsip`.
A netblock is written `<prefix-length>.<address in reverse>`; for IPv6 use `zz` for `::`. Use a length of 32 or 128 for a single address. For example `24.10.100.51.198.rpz-ip` is 198.51.100.10/24 (the manual's own example), and `32.10.zz.db8.2001.rpz-ip` is the IPv6 /32 form.
RPZ QNAME triggers are applied after any local-zone and before any auth-zone. Besides the actions below, A, AAAA, TXT and non-rpz CNAME records answer queries with that content.

Actions (set by record type and RDATA):
- NXDOMAIN: `CNAME .`
- NODATA: `CNAME *.`
- PASSTHRU: `CNAME rpz-passthru.` (exempts the name or address)
- DROP: `CNAME rpz-drop.`
- TCP-Only: `CNAME rpz-tcp-only.`
- Local Data: returns a preconfigured record; other types get NODATA.

Zones are evaluated in configured order; later zones apply only if earlier ones do not match. See rpz-zone-configuration for the Unbound clauses.

## Checked

2026-11-08. Read the RPZ topic page in full and the Response Policy Zone Options introduction of the unbound.conf manual. Replaced the vague address note with the real netblock encoding (prefix length first, zz for ::) and added the evaluation order relative to local-zone and auth-zone.

Method: documentation only; no commands were run.
