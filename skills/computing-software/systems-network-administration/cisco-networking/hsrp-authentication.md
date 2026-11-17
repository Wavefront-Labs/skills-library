---
id: computing-software.systems-network-administration.cisco-networking.hsrp-authentication
name: hsrp-authentication
category: computing-software
field: systems-network-administration
product: cisco-networking
tags: [cisco, cisco-ios, ios-xe, fhrp, hsrp, hsrp-authentication, md5-authentication, key-chain, gateway-security]
level: practitioner
status: draft
description: "Secure HSRP with MD5 key-string or key-chain authentication, roll keys without outages, and recognise auth mismatch symptoms."
sources:
  - https://www.cisco.com/c/en/us/td/docs/ios-xml/ios/ipapp_fhrp/configuration/xe-16/fhp-xe-16-book/fhp-hsrp-md5.html
  - https://www.cisco.com/c/en/us/support/docs/ip/hot-standby-router-protocol-hsrp/10583-62.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# HSRP authentication

## Why
Without authentication any host on the VLAN can send HSRP hellos with priority 255 and become
active gateway (man-in-the-middle). Plain-text auth (`standby 1 authentication cisco`, the
default "cisco") is visible in captures; use MD5.

## Configure
Key-string:
```
interface Vlan10
 standby version 2
 standby 10 ip 10.10.0.1
 standby 10 priority 110
 standby 10 preempt
 standby 10 authentication md5 key-string <SECRET>
```
Key chain (supports rollover):
```
key chain HSRP-KC
 key 1
  key-string <SECRET1>
  accept-lifetime 00:00:00 Jan 1 2026 infinite
  send-lifetime 00:00:00 Jan 1 2026 00:00:00 Jul 1 2026
 key 2
  key-string <SECRET2>
  accept-lifetime 00:00:00 Jun 1 2026 infinite
  send-lifetime 00:00:00 Jun 1 2026 infinite
interface Vlan10
 standby 10 authentication md5 key-chain HSRP-KC
```
Key chain lifetimes require NTP-synchronised clocks on both routers.

## Mismatch symptoms
- Both routers become Active (each ignores the other's hellos): duplicate gateway, MAC flaps.
- Log: `%HSRP-4-BADAUTH: Bad authentication from 10.10.0.3, group 10, remote state Active`.

## Changing keys without outage
Use a key chain with overlapping accept lifetimes, or briefly set the standby router to a lower
priority and change keys during a window; a mismatch otherwise creates a dual-active condition.

## Verify
```
show standby vlan 10        ! Authentication MD5, key-chain/key-string
show standby brief          ! one Active, one Standby
```
