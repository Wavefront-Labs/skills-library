---
id: computing-software.systems-network-administration.cisco-networking.acl-and-security-configuration
name: acl-and-security-configuration
category: computing-software
field: systems-network-administration
product: cisco-networking
tags: [cisco, cisco-ios, ios-xe, acl, access-control-list, standard-acl, extended-acl, named-acl, ip-access-list, ipv6-acl, implicit-deny, object-group, access-class, vty, established, wildcard-mask, network-hardening, device-hardening, ssh, aaa, enable-secret, scrypt, port-security, dhcp-snooping, dynamic-arp-inspection, dai, ip-source-guard, storm-control, management-plane, copp, lockout-prevention]
level: advanced
status: draft
description: "Cisco IOS ACLs (extended named, placement, sequence edits, object-groups, IPv6 ND gotcha) plus device and edge hardening: SSH-only VTY, scrypt secrets, DHCP snooping, DAI, port security."
sources:
  - https://www.cisco.com/c/en/us/support/docs/security/ios-firewall/23602-confaccesslists.html
  - https://www.cisco.com/c/en/us/support/docs/ip/access-lists/13608-21.html
  - https://sec.cloudapps.cisco.com/security/center/resources/ios_hardening.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# ACL and security configuration on Cisco IOS — filter deliberately, never lock yourself out

**Goal:** write ACLs that permit exactly what a segment needs, apply them where they cost
least, and harden the switch/router itself and its edge ports. Vendor-neutral segmentation
policy (which zones talk to which) lives in
`computing-software.systems-network-administration.network-design.network-segmentation-strategy`.

## 0. Safety net first
Before touching an ACL on the interface you are connected through:
```
reload in 10        ! reboots to the saved config in 10 min unless cancelled
! ...make and test the change...
reload cancel
```
Alternatively use `configure replace` / archive rollback where available. Never apply an
empty or half-written ACL to a live interface: on IOS an applied but nonexistent ACL
permits all, but an ACL with one `permit` line denies everything else instantly.

## 1. ACL fundamentals that bite
- Every ACL ends with an **implicit `deny any`**. Add an explicit
  `deny ip any any log` only on low-rate ACLs; `log` is CPU-punted on many platforms.
- Wildcard masks are inverted subnet masks: /24 → `0.0.0.255`, /30 → `0.0.0.3`.
- **Standard** ACLs match source only: put them close to the destination (or on VTYs).
  **Extended** ACLs match src/dst/protocol/port: put them close to the source so dropped
  traffic does not cross the network.
- One ACL per interface, per direction, per protocol (IPv4/IPv6).
- Use **named ACLs with sequence numbers** so you can insert and delete lines:
```
ip access-list extended USERS-IN
 10 permit udp 10.10.0.0 0.0.255.255 host 10.99.0.53 eq domain
 20 permit tcp 10.10.0.0 0.0.255.255 host 10.99.0.53 eq domain
 30 permit tcp 10.10.0.0 0.0.255.255 10.50.0.0 0.0.255.255 eq 443
 40 deny   ip 10.10.0.0 0.0.255.255 10.0.0.0 0.255.255.255
 50 permit ip 10.10.0.0 0.0.255.255 any            ! internet via firewall
!
interface Vlan10
 ip access-group USERS-IN in
```
  Insert later with `ip access-list extended USERS-IN` then `35 permit ...`. Renumber with
  `ip access-list resequence USERS-IN 10 10`.
- The `established` keyword matches TCP with ACK/RST set: a crude return-traffic filter,
  not stateful. Use a firewall (or zone-based firewall) for real state.
- **Object-groups** keep large ACLs readable:
  `object-group network WEB-SERVERS` / `host 10.50.0.10` then
  `permit tcp any object-group WEB-SERVERS eq 443`. Platform support varies (unconfirmed on
  older Catalyst images).

## 2. IPv6 ACL gotcha
IPv6 ACLs end with implicit `permit icmp any any nd-na`, `permit icmp any any nd-ns` and
then `deny ipv6 any any`. If you add your own `deny ipv6 any any log` at the end, you kill
Neighbor Discovery and the interface stops working. Explicitly permit ND (and RA where
needed) before any final deny. Apply with `ipv6 traffic-filter NAME in`.

## 3. Lock down the device
```
hostname CORE1
ip domain name corp.example
crypto key generate rsa modulus 3072
ip ssh version 2
enable algorithm-type scrypt secret <ENABLE_SECRET>
username netadmin privilege 15 algorithm-type scrypt secret <PASSWORD>
login block-for 120 attempts 5 within 60
ip access-list standard MGMT-ONLY
 permit 10.99.10.0 0.0.0.255
line vty 0 15
 transport input ssh
 access-class MGMT-ONLY in
 login local
 exec-timeout 10 0
no ip http server
no ip http secure-server         ! unless you use the web UI/RESTCONF
service password-encryption      ! only obscures type 7; not real protection
```
Type 7 passwords are trivially reversible; use type 8/9 (`algorithm-type sha256|scrypt`).
Prefer AAA with TACACS+/RADIUS plus a local fallback account. Control-plane policing
(CoPP) protects the CPU from floods; many IOS-XE platforms ship a default policy.

## 4. Edge-port protection (access switches)
```
ip dhcp snooping
ip dhcp snooping vlan 10,20
no ip dhcp snooping information option   ! if upstream DHCP server rejects option 82
interface Te1/1/1                         ! uplink toward the real DHCP server
 ip dhcp snooping trust
 ip arp inspection trust
ip arp inspection vlan 10,20
interface range Gi1/0/1 - 24
 switchport port-security
 switchport port-security maximum 3      ! PC + phone (phone may count twice)
 switchport port-security violation restrict
 ip dhcp snooping limit rate 15
 storm-control broadcast level 5.00
```
- DHCP snooping blocks rogue DHCP servers and builds the binding table that DAI and
  IP Source Guard (`ip verify source`) use.
- **DAI drops ARP from hosts with static IPs** that are not in the snooping table: add
  `arp access-list` entries for printers/servers or trust those ports.
- Inserted option 82 makes some Windows/ISC DHCP servers silently drop requests; that is
  why the `no ... information option` line is often needed.
- `violation restrict` drops and logs; `shutdown` (default) err-disables the port.

## Verify
- [ ] `reload in` set before the change, cancelled after.
- [ ] `show access-lists USERS-IN` hit counters increment on intended lines; final deny counts make sense.
- [ ] Allowed flows tested from the source segment; one denied flow tested and logged.
- [ ] SSH only, from the management subnet only; telnet and HTTP refused.
- [ ] `show ip dhcp snooping binding` populated; a test rogue DHCP server is blocked.
- [ ] No IPv6 ACL breaks ND (`show ipv6 neighbors` still resolves).
