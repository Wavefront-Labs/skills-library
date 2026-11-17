---
id: computing-software.systems-network-administration.cisco-networking.tacacs-plus-device-administration
name: tacacs-plus-device-administration
category: computing-software
field: systems-network-administration
product: cisco-networking
tags: [cisco, cisco-ios, aaa, tacacs-plus, aaa-authentication, aaa-new-model, local-fallback, ise, server-group]
level: practitioner
status: draft
description: "Point IOS device logins at TACACS+ (ISE or tac_plus) with a server group, source interface, key, and a local fallback account that only works when servers are down."
sources:
  - https://www.cisco.com/c/en/us/support/docs/security-vpn/terminal-access-controller-access-control-system-tacacs-/200565-Configure-TACACS-Authentication.html
  - https://www.rfc-editor.org/rfc/rfc8907
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# TACACS+ device administration

TACACS+ (TCP 49, RFC 8907) encrypts the whole body and separates authentication,
authorization and accounting, which is why it is used for admin logins (RADIUS is for network access).

## Configure (keep a console session open; test in a second vty)
```
aaa new-model
tacacs server ISE-1
 address ipv4 10.99.0.11
 key <TACACS_KEY>
 timeout 5
tacacs server ISE-2
 address ipv4 10.99.0.12
 key <TACACS_KEY>
aaa group server tacacs+ TACACS
 server name ISE-1
 server name ISE-2
 ip tacacs source-interface Loopback0      ! or Vlan99; must match the NAD IP in ISE
!
aaa authentication login default group TACACS local
aaa authentication login CONSOLE local
aaa authorization exec default group TACACS local if-authenticated
aaa authorization console
username breakglass privilege 15 algorithm-type scrypt secret <LONG_SECRET>
line con 0
 login authentication CONSOLE
line vty 0 15
 login authentication default
```
- `local` after the group is used **only** when no TACACS server responds, not when a server
  rejects the password. Good: a fired admin's local account cannot be used while ISE is up.
- `aaa authorization exec` lets TACACS assign privilege level 15 (shell profile `priv-lvl=15`);
  without it everyone lands at level 1.
- The console method list keeps local access if the network to ISE is down.

## Gotchas
- `aaa new-model` immediately applies default login authentication (local) to all lines; if
  there is no local user you lock yourself out.
- Source interface mismatch: ISE logs "Could not find selected Network Device" and rejects.
- Use `reload in 10` before the change on remote devices.

## Verify
```
test aaa group TACACS netadmin <PASSWORD> legacy
show tacacs                                ! per-server opens, errors, timeouts
show aaa servers
```
- [ ] TACACS login lands at the right privilege; local breakglass works only with servers unreachable.
