---
id: computing-software.systems-network-administration.cisco-networking.arp-acls-and-dai-rate-limits
name: arp-acls-and-dai-rate-limits
category: computing-software
field: systems-network-administration
product: cisco-networking
tags: [cisco, cisco-ios, ios-xe, dynamic-arp-inspection, dai, arp-acl, dai-rate-limit, arp-inspection-filter, static-ip-hosts, err-disabled]
level: practitioner
status: docs-checked
description: "Make Dynamic ARP Inspection work for static-IP hosts with ARP ACLs, set per-port ARP rate limits, and recover from DAI err-disable, per the Catalyst 9300 17.9 guide."
sources:
  - https://www.cisco.com/c/en/us/td/docs/switches/lan/catalyst9300/software/release/17-9/configuration_guide/sec/b_179_sec_9300_cg/configuring_dynamic_arp_inspection.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ARP ACLs and DAI rate limits

Syntax below is from the Catalyst 9300 IOS XE 17.9 security guide; other platforms and releases may differ.

## ARP ACLs for static hosts
DAI checks ARP against the DHCP snooping binding database. In non-DHCP environments, or for hosts with static IPs, use an ARP ACL:
```
arp access-list STATIC-HOSTS
 permit ip host 10.10.0.10 mac host 0011.2233.4455
 permit ip host 10.10.0.11 mac host 0011.2233.4466
exit
ip arp inspection vlan 10
ip arp inspection filter STATIC-HOSTS vlan 10 [static]
```
- An ARP ACL ends in an implicit `deny ip any mac any`. No ARP ACLs are defined or applied by default.
- ARP ACLs take precedence over DHCP snooping bindings: an ACL deny drops the packet even if a valid binding exists.
- Without `static`, a packet that matches no ACL clause is decided by the DHCP bindings. With `static`, implicit denies become explicit, DHCP bindings are not used, and only ACL permits pass.
- DAI is disabled on all VLANs by default; `ip arp inspection vlan <range>` enables it (VLAN range 1 to 4094).
- A static host behind a link to a switch that does not run DAI: keep that link untrusted and permit the host with an ARP ACL.

## Trust and rate limits
- All interfaces are untrusted by default. Trusted interfaces skip validation and are not rate limited; configure inter-switch links as trusted (`ip arp inspection trust`). Wrongly untrusted links can cause lost connectivity; wrongly trusted ones leave a security hole.
- Default limit on untrusted interfaces: 15 pps, burst interval 1 second. When exceeded the port goes error-disabled and stays so until you intervene.
```
interface Gi1/0/5
 ip arp inspection limit rate 100 burst interval 1   ! rate 0-2048 pps, interval 1-15 s
interface Te1/1/1
 ip arp inspection trust
errdisable recovery cause arp-inspection
errdisable recovery interval 300
```
- `ip arp inspection limit none` makes the rate unlimited. The guide says to rate limit incoming trunk ports, with higher rates for their aggregation across several DAI VLANs, and warns that a high limit on one VLAN can let a denial of service hit other VLANs through the error-disabled port.
- Error-disable recovery is off by default; the interval defaults to 300 seconds (range 30 to 86400). `errdisable detect cause arp-inspection` is also listed.
- Without an explicit limit, changing trust state changes the limit to that state's default; `no ip arp inspection limit` reverts to default.
- On an EtherChannel the limit applies to the port channel and is cumulative across members, and in a stack it is counted per switch, so the effective limit can be higher than configured.

## Extra validation
`ip arp inspection validate {[src-mac] [dst-mac] [ip]}` (no checks by default): `src-mac` compares Ethernet source with ARP sender MAC; `dst-mac` compares Ethernet destination with target MAC in responses; `ip` rejects 0.0.0.0, 255.255.255.255 and multicast addresses (sender in requests and responses, target in responses). At least one keyword is required, and each command overrides the previous one, so list all wanted checks in a single command.

## Verify
```
show arp access-list STATIC-HOSTS
show ip arp inspection vlan 10
show ip arp inspection statistics vlan 10     ! forwarded, dropped, ACL and DHCP permit/deny, validation failures
show ip arp inspection interfaces             ! trust state and rate limit
show ip dhcp snooping binding
show ip arp inspection log
```

## Checked
Date: 2026-11-08
Read in full: Cisco Catalyst 9300 17.9 "Configuring Dynamic ARP Inspection" chapter (restrictions, concepts, defaults table, all four procedures, monitoring and verification tables).
Confirmed: every default, range and command above, ACL-over-binding precedence, `static` semantics, implicit deny, trust guidance, EtherChannel and stack rate notes, validate keywords and override behaviour, errdisable recovery defaults, verification commands.
Removed: the `ip source binding` static-binding alternative, the syslog message names (`%SW_DAI-4-PACKET_RATE_EXCEEDED`, `%PM-4-ERR_DISABLE`), the gratuitous-ARP warning about clustered servers, `show errdisable recovery`, and the "never rate-limit trunks" advice (the guide says the opposite). A second source (Catalyst 6500 technote) returns 404 and was dropped.
Method: documentation only; no commands were run.
