---
id: computing-software.cybersecurity-defensive.system-hardening.management-plane-protection
name: management-plane-protection
category: computing-software
field: cybersecurity-defensive
product: system-hardening
tags: [network-device-hardening, management-plane-protection, oob-management, copp, vty-acl, mgmt-vrf, control-plane-policing]
level: advanced
status: draft
description: "Protect network device management and control planes: dedicated management VRF or OOB network, VTY and API ACLs, MPP, CoPP rate limits and jump-host access only."
sources: ["Cisco Guide to Harden Cisco IOS Devices - Management Plane and Control Plane", "NSA Network Infrastructure Security Guide - Out-of-band management", "CISA guidance on protecting network device management interfaces"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Management plane protection

**Goal:** device management interfaces are reachable only from a dedicated management network via jump hosts, and the control plane cannot be overwhelmed.

## Architecture
- Out-of-band (OOB) management network or a management VRF; admin access only via hardened jump hosts/PAM with MFA and session recording.
- Never expose SSH, HTTPS, NETCONF/RESTCONF or SNMP management of network devices or firewalls to the internet; widely exploited appliance management bugs (e.g. IOS XE WebUI CVE-2023-20198) show why.

## Device config (Cisco examples)
```
vrf definition Mgmt-vrf
interface GigabitEthernet0/0
 vrf forwarding Mgmt-vrf
 ip address 10.250.1.10 255.255.255.0
ip access-list standard MGMT-ONLY
 permit 10.250.0.0 0.0.255.255
 deny any log
line vty 0 15
 access-class MGMT-ONLY in vrf-also
 transport input ssh
ip ssh source-interface GigabitEthernet0/0
logging source-interface GigabitEthernet0/0 vrf Mgmt-vrf
```
Management Plane Protection (on supporting IOS): `control-plane host` / `management-interface Gi0/0 allow ssh snmp` restricts which interfaces accept management protocols.

## Control-plane policing (CoPP)
Classify traffic to the route processor (routing protocols, management, ICMP, undesirable) and police each class; most platforms ship a default CoPP policy (Catalyst 9000 system-defined) - review before modifying.
Also: routing protocol authentication (OSPF/BGP MD5 or TCP-AO, `neighbor x password`), GTSM `ttl-security hops 1` for eBGP.

## Other vendors
Juniper: loopback `lo0` firewall filter protecting RE; Palo Alto: management interface profile and permitted IPs; Fortinet: `trusted hosts` on admin accounts and `allowaccess` per interface.

## Verify
- [ ] From a user VLAN, `nmap -p22,23,80,443,830,161 <device>` shows filtered/closed.
- [ ] `show policy-map control-plane` counters show policing active.
- [ ] Admin logins in TACACS+ logs originate only from jump hosts.
