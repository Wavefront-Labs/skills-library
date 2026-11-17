---
id: computing-software.systems-network-administration.cisco-networking.disable-unused-ios-services
name: disable-unused-ios-services
category: computing-software
field: systems-network-administration
product: cisco-networking
tags: [cisco, cisco-ios, disable-unused-services, no-ip-http-server, device-hardening, cdp, small-servers, proxy-arp, ip-redirects]
level: practitioner
status: draft
description: "Harden an IOS/IOS-XE device by disabling unused services: HTTP server, small servers, finger, source routing, proxy ARP, redirects, and CDP on untrusted ports."
sources:
  - https://www.cisco.com/c/en/us/support/docs/ip/access-lists/13608-21.html
  - https://sec.cloudapps.cisco.com/security/center/resources/ios_xe_hardening_guide
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Disable unused IOS services

Every listening service is attack surface. The IOS-XE web UI alone has had critical
remotely exploitable bugs (CVE-2023-20198); disable what you do not use.

```
no ip http server
no ip http secure-server              ! unless WebUI/RESTCONF is needed (then restrict it)
no service tcp-small-servers
no service udp-small-servers
no ip finger
no service pad
no ip bootp server
no ip source-route
no service config
no ip domain lookup                   ! or point it at a real resolver
service tcp-keepalives-in
service tcp-keepalives-out
service password-encryption           ! cosmetic, but hides type-0 from shoulder surfing
interface GigabitEthernet0/0/0         ! internet-facing
 no ip proxy-arp
 no ip redirects
 no ip unreachables
 no ip directed-broadcast
 no cdp enable
 no lldp transmit
 no lldp receive
```

## If the web server is needed (RESTCONF, WebUI)
```
ip http secure-server
ip http access-class ipv4 MGMT-HOSTS
ip http authentication local
ip http max-connections 5
```
Never expose it to the internet.

## Find listeners
```
show control-plane host open-ports
show ip sockets               ! older IOS
show udp
```
Anything listening you cannot name is a finding.

## Verify
- [ ] `show control-plane host open-ports` lists only SSH, SNMP (if used), NTP and needed protocols.
- [ ] External nmap scan of the WAN address shows no open management ports.
