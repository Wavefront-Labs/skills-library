---
id: computing-software.systems-network-administration.cisco-networking.ibns2-identity-policy-maps
name: ibns2-identity-policy-maps
category: computing-software
field: systems-network-administration
product: cisco-networking
tags: [cisco, cisco-ios, ios-xe, ibns2, identity-policy-map, c3pl, policy-map-type-control-subscriber, access-session, 802-1x, mab, authentication-convert-to]
level: practitioner
status: draft
description: "Write IBNS 2.0 (C3PL) identity policies on Catalyst: control-subscriber policy maps, events, class-maps, service templates, and converting legacy config."
sources:
  - https://www.cisco.com/c/en/us/td/docs/ios-xml/ios/san/configuration/xe-16/san-xe-16-book/san-ibns2.html
  - https://community.cisco.com/t5/security-knowledge-base/ibns-2-0-deployment-guide/ta-p/3640652
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# IBNS 2.0 identity policy maps

## Building blocks
| Element | Role |
|---|---|
| `class-map type control subscriber` | conditions: method (dot1x/mab), result-type (timeout, aaa-timeout), authorization status |
| `policy-map type control subscriber` | event -> class -> ordered actions |
| `service-template` | local authorization bundles (VLAN, ACL, timers, critical) |
| `access-session` interface commands | host mode, closed/open, port control |

## Typical concurrent-friendly policy (dot1x then MAB)
```
class-map type control subscriber match-all DOT1X_FAILED
 match method dot1x
 match result-type method dot1x authoritative
class-map type control subscriber match-all DOT1X_NO_RESP
 match method dot1x
 match result-type method dot1x agent-not-found
class-map type control subscriber match-all MAB_FAILED
 match method mab
 match result-type method mab authoritative
policy-map type control subscriber PMAP_DOT1X_MAB
 event session-started match-all
  10 class always do-until-failure
   10 authenticate using dot1x priority 10
 event authentication-failure match-first
  10 class DOT1X_NO_RESP do-until-failure
   10 terminate dot1x
   20 authenticate using mab priority 20
  20 class DOT1X_FAILED do-until-failure
   10 terminate dot1x
   20 authenticate using mab priority 20
  30 class MAB_FAILED do-until-failure
   10 terminate mab
   20 authentication-restart 60
 event agent-found match-all
  10 class always do-until-failure
   10 terminate mab
   20 authenticate using dot1x priority 10
 event authentication-success match-all
  10 class always do-until-failure
   10 activate service-template DEFAULT_LINKSEC_POLICY_SHOULD_SECURE   ! optional
interface Gi1/0/5
 switchport access vlan 20
 switchport voice vlan 100
 access-session host-mode multi-auth
 access-session closed
 access-session port-control auto
 dot1x pae authenticator
 mab
 service-policy type control subscriber PMAP_DOT1X_MAB
```

## Converting legacy config
```
authentication display new-style       ! view legacy config as IBNS 2.0 (reversible)
authentication convert-to new-style    ! one-way conversion, creates policies
```
Run convert in a maintenance window; it rewrites all interface authentication config.

## Gotchas
- Event ordering: `match-first` stops at first matching class; `match-all` runs all.
- `do-until-failure` stops the action list at the first failed action; `do-all` keeps going.
- Interface templates (`template` + `source template`) keep 48 ports consistent.

## Verify
```
show policy-map type control subscriber PMAP_DOT1X_MAB
show access-session interface Gi1/0/5 details
```
