---
id: computing-software.networking-hardware-and-wireless.arista-eos.aaa-tacacs
name: aaa-tacacs
category: computing-software
field: networking-hardware-and-wireless
product: arista-eos
tags: [arista-eos, aaa, tacacs, radius, authorization]
level: practitioner
status: draft
description: "Configure EOS AAA with TACACS+/RADIUS authentication, command authorization, accounting and local fallback."
sources: ["https://www.arista.com/en/support/product-documentation", "https://www.arista.com/en/um-eos/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# AAA with TACACS+ and local fallback
Goal: centralised login with a safety net.

```
username admin privilege 15 role network-admin secret sha512 <hash-placeholder>
tacacs-server host 192.0.2.50 key 7 <encrypted-placeholder>
aaa group server tacacs+ TAC
   server 192.0.2.50
aaa authentication login default group TAC local
aaa authorization exec default group TAC local
aaa accounting commands all default start-stop group TAC
```

```
show aaa
show users
show tacacs
```

- Keep `local` as the last method so a down server does not lock everyone out.
- Roles: `network-admin`, `network-operator`; custom roles with `role` blocks.
- Use `management ssh` with `vrf MGMT` when servers are reachable via the management VRF (`tacacs-server host ... vrf MGMT`).

Gotcha: `aaa authentication login default group TAC` without `local` locks you out when TACACS is unreachable. Add a local break-glass user first.

Operational tip: test each AAA path (TACACS success, TACACS unreachable, local only) in the lab and record the break-glass account's custody. Rotate shared keys on a schedule.

## Verify
- Log in with a TACACS user and `show users` shows it; stop the server briefly to confirm local fallback works.
