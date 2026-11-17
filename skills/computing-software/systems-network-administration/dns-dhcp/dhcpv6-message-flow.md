---
id: computing-software.systems-network-administration.dns-dhcp.dhcpv6-message-flow
name: dhcpv6-message-flow
category: computing-software
field: systems-network-administration
product: dns-dhcp
tags: [dhcp, dhcpv6, solicit-advertise, dhcpv6-message-flow, ia-na, troubleshooting]
level: practitioner
status: verified
description: "Follow the DHCPv6 message flow (Solicit, Advertise, Request, Reply, Renew, Rebind, Release, Confirm) with RA M/O flags, multicast addresses and failure diagnosis."
sources:
  - https://www.rfc-editor.org/rfc/rfc9915
  - https://www.rfc-editor.org/rfc/rfc8415
  - https://www.wireshark.org/docs/dfref/d/dhcpv6.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# SOLICIT/ADVERTISE/REQUEST/REPLY flow

## Triggers
Router Advertisements carry the M flag (Managed address configuration: addresses are available via
DHCPv6) and the O flag (Other configuration; redundant when M is set) (RFC 4861). Hosts use them to
decide whether to run DHCPv6; behaviour varies by OS.

## Transport
Client UDP 546 -> `ff02::1:2` (All_DHCP_Relay_Agents_and_Servers) port 547 from its link-local
address. Relays forward to servers (unicast or `ff05::1:3`) wrapped in Relay-Forw / Relay-Repl.

## Messages
| # | Message | Purpose |
|---|---------|---------|
| 1 | SOLICIT | find servers; contains client DUID, IA_NA/IA_PD with IAID, ORO |
| 2 | ADVERTISE | offer with preference option (7); client picks highest preference |
| 3 | REQUEST | ask the chosen server (server ID option) |
| 7 | REPLY | commit addresses/prefixes with T1/T2 and lifetimes |
| 5 | RENEW | at T1, unicast/multicast to the original server |
| 6 | REBIND | at T2, to any server |
| 8 | RELEASE | give back |
| 9 | DECLINE | DAD found duplicate address |
| 4 | CONFIRM | after link change, check addresses still valid |
| 11 | INFORMATION-REQUEST | stateless options |

## Wireshark filters
```
dhcpv6
dhcpv6.msgtype == 1
dhcpv6.status_code != 0            # NoAddrsAvail (2), NoBinding (3), NotOnLink (4), NoPrefixAvail (6)
icmpv6.type == 134                 # RAs: check M/O flags
```

## Diagnosing
- Solicits but no Advertise: relay missing or not forwarding, server no subnet for the
  link (relay link-address not matching), firewall dropping UDP 547.
- Advertise with status NoAddrsAvail: pool exhausted or client class restrictions.
- Client ignores DHCPv6: RA M flag off.
- Address obtained but no default route: DHCPv6 does not give routes (the IANA DHCPv6 option registry
  has no router option); RAs must provide the router.

## Verify
- [ ] A capture shows the full exchange ending in REPLY with IA_NA addresses and status success, and the client configures the address. The IA Address option carries only address and lifetimes
  (Wireshark `dhcpv6.iaaddr.ip`, `.pref_lifetime`, `.valid_lifetime`), so the on-link prefix length comes
  from the RA, not DHCPv6.
