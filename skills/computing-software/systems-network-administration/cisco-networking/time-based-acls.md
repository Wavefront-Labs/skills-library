---
id: computing-software.systems-network-administration.cisco-networking.time-based-acls
name: time-based-acls
category: computing-software
field: systems-network-administration
product: cisco-networking
tags: [cisco, cisco-ios, ios-xe, acl, time-range, periodic, absolute, ntp, scheduled-access]
level: practitioner
status: draft
description: "Apply IOS ACL entries only at certain times with time-range (periodic/absolute), make the clock trustworthy, and verify active/inactive entries."
sources:
  - https://www.cisco.com/c/en/us/td/docs/ios-xml/ios/sec_data_acl/configuration/xe-16/sec-data-acl-xe-16-book/sec-time-based-acl.html
  - https://www.cisco.com/c/en/us/support/docs/security/ios-firewall/23602-confaccesslists.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Time-based ACLs

## Configure
```
time-range BUSINESS-HOURS
 periodic weekdays 8:00 to 18:00
time-range CONTRACTOR
 absolute start 00:00 01 November 2026 end 23:59 30 November 2026
ip access-list extended GUEST-IN
 permit tcp 10.50.0.0 0.0.255.255 any eq 443 time-range BUSINESS-HOURS
 permit tcp host 10.60.0.25 host 10.0.0.10 eq 22 time-range CONTRACTOR
 deny ip any any
```
Periodic keywords: `daily`, `weekdays`, `weekend`, specific days (`Monday Wednesday`), times in 24 h.
A time-range can hold several periodic lines plus one absolute (absolute bounds the periodic ones).

## Clock is everything
The router's local time decides. Set:
```
clock timezone GMT 0
clock summer-time BST recurring last Sun Mar 1:00 last Sun Oct 2:00
ntp server 10.0.0.11
```
An unsynced or wrong-timezone clock opens or closes access at the wrong time.

## Gotchas
- `periodic 22:00 to 06:00` across midnight: use two periodic lines or `daily 22:00 to 23:59` + `daily 0:00 to 6:00`.
- Entries with an inactive time-range simply do not match; traffic falls through to later lines.
- Existing sessions are not cut when the range ends on stateless ACLs (packets are just denied after).
- Hardware switches apply time-based ACLs via TCAM reprogramming; check platform support.

## Verify
```
show time-range                    ! (active) / (inactive)
show access-lists GUEST-IN         ! entries marked (active)/(inactive)
show clock detail                  ! time source NTP
```
