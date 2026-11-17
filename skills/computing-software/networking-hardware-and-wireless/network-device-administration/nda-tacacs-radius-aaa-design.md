---
id: computing-software.networking-hardware-and-wireless.network-device-administration.nda-tacacs-radius-aaa-design
name: nda-tacacs-radius-aaa-design
category: computing-software
field: networking-hardware-and-wireless
product: network-device-administration
tags: [tacacs-plus-aaa, radius-device-admin, local-fallback-account]
level: advanced
status: draft
description: "Centralise device login with TACACS+ or RADIUS, per-command authorisation and accounting, with a local fallback account."
sources:
  - https://www.cisco.com/
  - https://www.juniper.net/documentation/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Device AAA

- TACACS+ separates authentication, authorisation (per command/privilege level) and accounting, and encrypts the full payload; RADIUS (RFC 2865) is more widely supported but combines authN/authZ and encrypts only the password.
- Use at least two servers with timeouts and failover; keep a local fallback account with a strong secret stored in a vault so you can get in if AAA is down.
- Map role groups (read-only, operator, admin) to privilege levels or Junos login classes.
- Accounting logs satisfy audit requirements: record commands and who ran them.
- Test AAA failure by blocking the server from the device; the local fallback must work, and keep the console `login local` fallback.

## Verify
- [ ] A read-only user cannot enter config mode and the accounting log shows their commands.
