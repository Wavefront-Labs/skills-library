---
id: computing-software.systems-network-administration.cisco-networking.pat-nat-overload
name: pat-nat-overload
category: computing-software
field: systems-network-administration
product: cisco-networking
tags: [cisco, cisco-ios, nat, nat-overload, pat, port-address-translation, internet-edge, nat-timeouts]
level: practitioner
status: docs-checked
description: "Give a LAN internet access with PAT (NAT overload) on the IOS WAN interface, with translation timeouts, per-host entry limits, non-pattable traffic and SIP caveats."
sources:
  - https://www.cisco.com/c/en/us/support/docs/ip/network-address-translation-nat/13772-12.html
  - https://www.cisco.com/c/en/us/td/docs/ios-xml/ios/ipaddr_nat/configuration/xe-16/nat-xe-16-book/iadnat-addr-consv.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# PAT (NAT overload)

Overloading maps many inside addresses to one global address using different ports. Cisco's IOS XE NAT guide says
thousands of users can reach the Internet through one real global address this way. The router keeps TCP or UDP port
information so it can translate the global address back to the right local address.

```
ip access-list standard NAT-INSIDE
 permit 10.1.0.0 0.0.255.255
ip nat inside source list NAT-INSIDE interface GigabitEthernet0/0/0 overload
interface Gi0/0/0
 ip nat outside
interface range Gi0/0/1 , Vlan10 , Vlan20
 ip nat inside
```
- `ip nat inside source list <acl> interface <type> overload` overloads on the address of that interface; the pool form
  is `ip nat inside source list <acl> pool <name> overload`, and a pool of one address works the same way.
- The NAT guide says NAT does not support `permit ip any any` in an access list used with a NAT command; permit the
  inside networks instead.
- Do not put the interface's own address in a NAT pool. The interface address can be shared only through interface
  overload.

## Timeouts and limits
```
ip nat translation tcp-timeout 3600
ip nat translation udp-timeout 60
ip nat translation dns-timeout 30
ip nat translation max-entries host 10.1.0.25 500
```
Defaults from the IOS XE guide: the general `ip nat translation timeout` is 24 hours (it applies to half-entries); when
overloading is configured, UDP defaults to 300 seconds and TCP to 7440 seconds, but those apply only if the general
timeout has not been configured, and a configured general timeout overrides the TCP and UDP defaults unless you set
`tcp-timeout` or `udp-timeout` explicitly. Other timers: `finrst-timeout`, `icmp-timeout`, `syn-timeout`.
`ip nat translation max-entries` takes `{number | all-vrf number | host ip-address number | list listname number |
vrf name number}`, so one infected host can be capped with the `host` form.

## Gotchas
- PAT works only for protocols with known ports: ICMP, TCP and UDP. Other ("non-pattable") traffic creates a bind
  entry that consumes a whole address from the pool, a 1-to-1 translation. Permit only ICMP, TCP and UDP in the NAT
  access list so other protocols do not enter.
- SIP support is on by default for port 5060, so NAT interprets all packets on that port as SIP call messages and may
  corrupt other applications using it.
- Applications that embed IP addresses in the payload may not work through NAT at all.
- `show ip nat statistics` updates slowly with large numbers (1000 to 4000) of pools and mappings.

## Verify
```
show ip nat translations
show ip nat statistics
```
- [ ] Inside hosts reach the Internet; translations are extended entries with ports.

## Checked
Checked 2026-11-08 against Cisco's Configure NAT technote (document 13772) and the IOS XE 16 Configuring NAT for IP
Address Conservation chapter: overload syntax, ACL restriction, timeout defaults, `max-entries` syntax, non-pattable
traffic, SIP default. Corrected: the TCP default is 7440 s, not 86400; `max-entries all-host` is not a valid form
(the `host` and `list` forms are). Removed as unconfirmed: the 64k-port estimate, DHCP-address behaviour, router-originated
traffic, asymmetric routing with two ISPs, `no ip nat service sip`, and the `total`/`count` show variants.
Method: documentation only; no commands were run.
