---
id: computing-software.systems-network-administration.cisco-networking.ipsec-dead-peer-detection
name: ipsec-dead-peer-detection
category: computing-software
field: systems-network-administration
product: cisco-networking
tags: [cisco, cisco-ios, ios-xe, ipsec, dpd, dead-peer-detection, ikev2-dpd, isakmp-keepalive, vpn-failover, rfc3706]
level: practitioner
status: draft
description: "Configure IPsec dead peer detection on IOS (IKEv1 isakmp keepalive, IKEv2 dpd periodic/on-demand) so stale SAs clear and backup peers take over."
sources:
  - https://datatracker.ietf.org/doc/html/rfc3706
  - https://www.cisco.com/c/en/us/td/docs/ios-xml/ios/sec_conn_ike2vpn/configuration/xe-16/sec-flex-vpn-xe-16-book/sec-cfg-ikev2-flex.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Dead peer detection (DPD)

## Why
Without DPD, if the peer reboots or the path dies, the local router keeps sending traffic into
stale IPsec SAs until they expire (up to the SA lifetime, often an hour). DPD detects the dead
peer, deletes the SAs and lets a backup peer or route take over.

## IKEv1
```
crypto isakmp keepalive 10 3 periodic     ! every 10 s, retry interval 3 s
! or on-demand (default): only when traffic is sent and nothing received
crypto map VPN 10 ipsec-isakmp
 set peer 203.0.113.1
 set peer 198.51.100.1                    ! backup peer used after DPD declares the first dead
```

## IKEv2
```
crypto ikev2 dpd 10 3 periodic            ! global
crypto ikev2 profile P1
 dpd 10 3 on-demand                       ! per profile overrides global
```
- `periodic`: R-U-THERE messages at the interval regardless of traffic (faster detection, more overhead).
- `on-demand`: only sent when there is outbound traffic and no inbound for the interval (default, scales better).
Detection time is roughly interval + retries x retry-interval (IOS sends up to 5 retries).

## Design notes
- Hub with thousands of spokes: on-demand on the hub, periodic on spokes that need fast failover.
- Both sides should run DPD; the side without it keeps stale SAs.
- Route-based VPN (VTI) with a routing protocol over the tunnel detects failure via the protocol
  too; DPD clears the SA so the tunnel can re-establish.
- NAT-T keepalives (`crypto isakmp nat keepalive 20`) are different: they keep NAT mappings open.

## Verify
```
show crypto ikev2 sa detailed | include DPD
show crypto isakmp sa detail
debug crypto ikev2 / debug crypto isakmp   ! "DPD" R-U-THERE / ACK messages
```
- [ ] Unplug the peer's WAN: SAs clear within the expected time and the backup path takes traffic.
