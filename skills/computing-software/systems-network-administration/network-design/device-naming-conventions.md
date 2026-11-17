---
id: computing-software.systems-network-administration.network-design.device-naming-conventions
name: device-naming-conventions
category: computing-software
field: systems-network-administration
product: network-design
tags: [network-design, documentation, naming-convention, hostnames, dns-naming, inventory]
level: practitioner
status: docs-checked
description: "Design a device naming convention for network gear: site, role, number and environment fields, DNS-safe characters, interface DNS names, and how to roll it out."
sources:
  - https://www.rfc-editor.org/rfc/rfc1178
  - https://www.rfc-editor.org/rfc/rfc1123
  - https://docs.netbox.dev/en/stable/models/dcim/device/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Device naming conventions

## Goals
A name should tell an on-call engineer where the device is and what it does, sort sensibly, be
DNS-safe, and stay valid when the device is replaced.

## Pattern
`<site>-<location>-<role><nn>[-<env>]`
| Field | Example | Notes |
|---|---|---|
| Site | `lon1`, `nyc2` | city or internal site code + number |
| Location | `b2f3` (building 2, floor 3), `dc1r12` (row 12) | optional for small sites |
| Role | `cr` core, `ds` distribution, `as` access, `fw`, `rtr`, `wlc`, `ap`, `lf` leaf, `sp` spine, `oob` | short, documented list |
| Number | `01`, `02` | two digits; pairs share odd/even (01 = A side) |
| Env | `-lab` | only where needed |
Example: `lon1-b2f3-as03`, `nyc2-dc1-lf12`, `lon1-fw01`.

## Rules
- Letters, digits and hyphens only (RFC 1123 lets a host name start with a letter or a digit);
  hosts must handle names up to 63 characters, so keep names well short of that.
- Do not encode model, serial, IP or vendor; they change on replacement.
- Same name in DNS, monitoring, the device hostname, CMDB/NetBox and configuration backups.
- Interface DNS names for traceroute readability: `xe-0-0-1.lon1-cr01.net.example.com`.
- Avoid names that leak too much on internet-facing PTRs if that matters for your threat model.

## Rollout
Publish the standard with the role code list; apply to new devices; rename existing ones during
maintenance with monitoring/DNS updated in the same change.

## Verify
- [ ] Automated check flags inventory names not matching the regex (e.g. `^[a-z]{3}\d-([a-z0-9]+-)?[a-z]{2,4}\d{2}(-[a-z]+)?$`).

## Checked

- Date: 2026-10-28
- Confirmed: RFC 1123 host-name syntax (letter or digit first) and the 63-character handling requirement.
- Removed: the IATA/UN-LOCODE claim, the lowercase and no-underscore rules (RFC 952 syntax not fetched). Pattern fields, role codes and examples are design conventions, not sourced claims.

Method: documentation only; no commands were run.
