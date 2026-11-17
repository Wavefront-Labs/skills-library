---
id: computing-software.systems-network-administration.cisco-networking.management-plane-protection
name: management-plane-protection
category: computing-software
field: systems-network-administration
product: cisco-networking
tags: [cisco, cisco-ios, ios-xe, management-plane-protection, mpp, control-plane-host, management-interface, device-hardening, in-band-management]
level: practitioner
status: draft
description: "Restrict IOS management protocols to specific interfaces with Management Plane Protection (control-plane host management-interface) and roll it out safely."
sources:
  - https://www.cisco.com/c/en/us/td/docs/ios-xml/ios/sec_data_mpp/configuration/xe-16/mpp-xe-16-book/mpp-mgmt-plane-prot.html
  - https://www.cisco.com/c/en/us/support/docs/ip/access-lists/13608-21.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Management Plane Protection (MPP)

## What it does
MPP designates which ingress interfaces accept management protocols. Management traffic arriving
on any other interface is dropped before it reaches the process, independent of VTY ACLs.

## Configure
```
control-plane host
 management-interface GigabitEthernet0/0/3 allow ssh snmp https
 management-interface GigabitEthernet0/0/1.900 allow ssh
```
Protocols: `beep`, `ftp`, `http`, `https`, `snmp`, `ssh`, `telnet`, `tftp`, `tl1`. Once any
management-interface is defined, those protocols are denied on all other interfaces.

## Restrictions (from the MPP configuration guide)
- Applies to in-band physical and logical interfaces (subinterfaces, tunnels) that receive the
  traffic. Loopbacks and virtual interfaces not tied to a physical interface are not supported
  as management interfaces.
- Dedicated out-of-band management ports (e.g. GigabitEthernet0 in Mgmt-intf VRF) are not
  covered; protect them with VRF and ACLs.
- Not on every platform; confirm with `control-plane host ?`.
- Combine with VTY `access-class`, SNMP ACLs and CoPP; MPP is one layer.

## Safe rollout
```
reload in 10                       ! safety net
conf t
 control-plane host
  management-interface GigabitEthernet0/0/3 allow ssh snmp https
end
! test SSH from your jump host via that interface; then
reload cancel
```

## Verify
```
show management-interface
show management-interface GigabitEthernet0/0/3 protocol ssh
```
- [ ] SSH arriving on a non-management interface is refused/times out.
- [ ] SNMP polling and HTTPS automation still work through the allowed interface.
