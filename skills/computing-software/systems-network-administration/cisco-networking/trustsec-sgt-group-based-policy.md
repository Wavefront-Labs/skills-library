---
id: computing-software.systems-network-administration.cisco-networking.trustsec-sgt-group-based-policy
name: trustsec-sgt-group-based-policy
category: computing-software
field: systems-network-administration
product: cisco-networking
tags: [cisco, trustsec, security-group-tag, cts-role-based, sgacl, sxp, ise, segmentation]
level: practitioner
status: draft
description: "Segment by group instead of IP with Cisco TrustSec: SGT assignment via ISE, inline tagging and SXP propagation, SGACL enforcement on switches, and verifying the policy matrix."
sources:
  - https://www.cisco.com/c/en/us/td/docs/switches/lan/catalyst9300/software/release/17-9/configuration_guide/cts/b_179_cts_9300_cg.html
  - https://www.cisco.com/c/en/us/solutions/enterprise-networks/trustsec/index.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# TrustSec SGT group-based policy

A Security Group Tag (16-bit) is assigned to each endpoint at authentication. Policy is a matrix of
source SGT x destination SGT -> SGACL, enforced on switches regardless of IP or VLAN.

## 1. Classification (assign SGTs)
- Dynamic: ISE authorization result includes an SGT (Employees=4, Contractors=5, IoT=20...).
- Static for servers: `cts role-based sgt-map 10.50.0.0/24 sgt 100` or VLAN-to-SGT
  (`cts role-based sgt-map vlan-list 50 sgt 100`), or IP-SGT mappings published from ISE.

## 2. Propagation
- Inline tagging (CMD header in the Ethernet frame) between capable switches:
  ```
  interface Te1/1/1
   cts manual
    policy static sgt 2 trusted
  ```
- SXP (TCP 64999) where the path cannot tag: edge switch speaks SXP to the enforcement device
  (often ISE as SXP hub, or a firewall/border switch).
  ```
  cts sxp enable
  cts sxp default password 0 S3cret
  cts sxp connection peer 10.0.0.5 password default mode local speaker
  ```

## 3. Enforcement
```
cts role-based enforcement
cts role-based enforcement vlan-list 10-50
```
Policy (matrix and SGACLs) is downloaded from ISE (`cts authorization list` with a PAC/credentials).
Example SGACL `Deny-IoT-to-Users`: `deny ip` from SGT 20 to SGT 4. Enforcement happens at egress,
on the switch where the destination is attached.

## Verify
```
show cts role-based sgt-map all          ! IP-to-SGT bindings and source (LOCAL, SXP, CLI)
show cts role-based permissions          ! the downloaded matrix
show cts role-based counters             ! hits per src/dst SGT and permit/deny
show cts sxp connections brief
show access-session interface Gi1/0/5 details | include SGT
```

## Gotchas
- Start in monitor (`cts role-based monitor all`) to see would-be denies via counters before
  enforcing.
- Default rule (unknown-to-unknown) decides what happens to untagged traffic; keep it permit until
  classification is complete.
- Platforms differ in SGACL TCAM capacity and inline tagging support; check hardware.

## Verify
- [ ] Counters show expected denies between IoT and user groups, and permitted flows work.
