---
id: computing-software.systems-network-administration.cisco-networking.getvpn-group-encryption
name: getvpn-group-encryption
category: computing-software
field: systems-network-administration
product: cisco-networking
tags: [cisco, cisco-ios, ios-xe, getvpn, group-encryption, gdoi, key-server, group-member, mpls-wan-encryption, tunnel-less-vpn]
level: practitioner
status: draft
description: "Encrypt a private MPLS WAN with GETVPN: GDOI key servers and group members, IP header preservation, policy ACLs, rekeying and cooperative KS redundancy."
sources:
  - https://www.cisco.com/c/en/us/td/docs/ios-xml/ios/sec_conn_getvpn/configuration/xe-16/sec-get-vpn-xe-16-book.html
  - https://www.cisco.com/c/dam/en/us/products/collateral/security/group-encrypted-transport-vpn/deployment_guide_c07_554713.pdf
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# GETVPN group encryption

## Concept
Group Encrypted Transport VPN uses GDOI (RFC 6407). Key servers (KS) distribute one set of IPsec
SAs to all group members (GMs). Traffic is encrypted any-to-any with **original IP headers
preserved** (tunnel-less), so the MPLS provider's routing and QoS still work. Suits private WANs,
not the internet (private addresses are visible and routed by the provider).

## Key server
```
crypto isakmp policy 10
 encryption aes 256
 hash sha256
 authentication pre-share
 group 19
crypto ipsec transform-set GET-TS esp-gcm 256
crypto ipsec profile GET-PROF
 set transform-set GET-TS
crypto key generate rsa label GETVPN-REKEY modulus 2048 exportable
ip access-list extended GET-POLICY
 deny udp any eq 848 any eq 848         ! GDOI
 deny tcp any any eq bgp
 deny tcp any eq bgp any
 permit ip 10.0.0.0 0.255.255.255 10.0.0.0 0.255.255.255
crypto gdoi group GET-GROUP
 identity number 1001
 server local
  rekey authentication mypubkey rsa GETVPN-REKEY
  rekey transport unicast
  sa ipsec 1
   profile GET-PROF
   match address ipv4 GET-POLICY
   replay time window-size 5
  address ipv4 10.255.0.10
  redundancy
   local priority 100
   peer address ipv4 10.255.0.11        ! cooperative KS
```

## Group member
```
crypto gdoi group GET-GROUP
 identity number 1001
 server address ipv4 10.255.0.10
 server address ipv4 10.255.0.11
crypto map GET-MAP 10 gdoi
 set group GET-GROUP
interface GigabitEthernet0/0          ! WAN to MPLS PE
 crypto map GET-MAP
```

## Gotchas
- Exclude routing protocol, GDOI (UDP 848) and management traffic from the policy, or GMs lose
  the routing adjacency to the PE before they register.
- Time-based anti-replay needs synchronised GMs (pseudotime from KS); NTP on all.
- Overlapping or NATed addresses break GETVPN; it needs routable private addressing end to end.
- Rekeys: multicast rekey needs a multicast-capable WAN; unicast rekey is simpler.

## Verify
```
show crypto gdoi                         ! KS: registered GMs, ACL, rekey; GM: registration status
show crypto gdoi ks members
show crypto gdoi gm
show crypto ipsec sa | include pkts
```
