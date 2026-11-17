---
id: computing-software.systems-network-administration.wireshark.dhcp-bootp-statistics
name: dhcp-bootp-statistics
category: computing-software
field: systems-network-administration
product: wireshark
tags: [wireshark, dhcp-statistics, dhcp, bootp, statistics]
level: practitioner
status: verified
description: "Count DHCP message types with Wireshark Statistics > DHCP (BOOTP-DHCP) and tshark -z dhcp,stat to spot NAK storms, missing ACKs and rogue servers."
sources:
  - https://www.wireshark.org/docs/dfref/d/dhcp.html
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# DHCP/BOOTP statistics

Statistics > BOOTP-DHCP counts packets per DHCP message type (Discover, Offer, Request, ACK, NAK,
Decline, Release, Inform).

## tshark
```
tshark -r dhcp.pcapng -q -z dhcp,stat
tshark -r dhcp.pcapng -q -z dhcp,stat,"dhcp.option.dhcp_server_id == 10.0.0.53"
```
(Wireshark 4.4.1 rejects `-z bootp,stat` as an invalid argument; older releases used `bootp,stat` and `bootp.*` fields.
Run on a synthetic capture with a Discover, two Offers from different servers, a Request, an ACK and a NAK: the
table counted Discover 2, Offer 2, Request 1, ACK 1, NAK 1, and the filtered form counted only that server's packets.)

## Ratios that tell a story
| Observation | Meaning |
|-------------|---------|
| Discovers >> Offers | server not reached (relay/helper missing) or pool exhausted |
| Offers but few Requests | client rejecting offers (wrong subnet, option problem) or Offers not reaching client |
| Many NAKs | clients roaming between VLANs with old leases, or two authoritative servers disagreeing |
| Declines | address conflicts in the pool |
| Informs high | clients that already have an address and only ask for options (DHCPINFORM, RFC 2131); normal in moderation |

## Find rogue servers
```
dhcp.option.dhcp == 2
tshark -r dhcp.pcapng -Y "dhcp.option.dhcp==2" -T fields -e dhcp.option.dhcp_server_id -e eth.src | sort | uniq -c
```
More than one server ID offering on a segment without failover configured = rogue or misconfiguration (the command
listed both test servers with their MACs).

## Per-transaction view
Group by transaction ID: `dhcp.id == 0x3903f326` shows a full DORA. Missing ACK after Request points
at the server or relay; delayed Offer (>1 s) at the relay or server load.

## Verify
- [ ] After the fix, Discover:Offer:Request:ACK ratios are close to 1:1:1:1 (minus renewals that skip Discover).
