---
id: computing-software.systems-network-administration.cisco-networking.ipsec-vpn-troubleshooting
name: ipsec-vpn-troubleshooting
category: computing-software
field: systems-network-administration
product: cisco-networking
tags: [cisco, cisco-ios, vpn, ipsec, ipsec-troubleshooting, ike-sa, ikev2, ikev1, isakmp, show-crypto-ipsec-sa, debug-crypto, proposal-mismatch, nat-t, encaps-decaps, phase-1, phase-2, conditional-debug]
level: advanced
status: draft
description: "Troubleshoot IOS site-to-site IPsec: phase 1 vs phase 2 failures, reading crypto SA output, encaps without decaps, proposal/PSK/ID mismatches, NAT-T, scoped debugs."
sources:
  - https://www.cisco.com/c/en/us/support/docs/security-vpn/ipsec-negotiation-ike-protocols/5409-ipsec-debug-00.html
  - https://www.cisco.com/c/en/us/support/docs/security-vpn/ipsec-negotiation-ike-protocols/115935-asa-ikev2-debugs.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# IPsec VPN troubleshooting

Work in order: underlay reachability, phase 1 (IKE SA), phase 2 (IPsec SAs), then traffic
selection and routing.

## 1. Underlay
`ping <peer> source <wan-if>`; UDP 500 and 4500 (NAT-T) and ESP (protocol 50) allowed by every
firewall/ACL in the path. If the peer is behind NAT, only UDP 500/4500 pass, ESP is
encapsulated in 4500.

## 2. Phase 1
```
show crypto ikev2 sa              ! READY = good; IN-NEG stuck = negotiation failing
show crypto isakmp sa             ! IKEv1: QM_IDLE = good; MM_NO_STATE = no reply / mismatch
```
Failures and causes:
| Symptom | Cause |
|---|---|
| no SA at all | no interesting traffic (policy-based), wrong peer IP, UDP 500 blocked |
| MM_NO_STATE / IN-NEG | proposal mismatch (encryption, PRF/hash, DH group) |
| AUTH failure | pre-shared key mismatch, wrong identity (address vs FQDN), cert issues |
| works then drops | DPD failing, lifetimes mismatched, NAT keepalives missing |

## 3. Phase 2
```
show crypto ipsec sa peer 203.0.113.20
!   local  ident (addr/mask/prot/port): (10.10.0.0/255.255.0.0/0/0)
!   remote ident (addr/mask/prot/port): (10.20.0.0/255.255.0.0/0/0)
!   #pkts encaps: 1520, #pkts decaps: 0
```
- **encaps increase, decaps 0**: we send, peer is not sending back. Peer routing to us, peer
  NAT exemption missing (traffic NATted before encryption), or peer's firewall policy.
- **decaps increase, encaps 0**: the reverse on our side: route to the remote subnet does not
  point into the tunnel, or our NAT translates it first (`deny` the VPN traffic in the NAT ACL).
- Proxy-ID / traffic selector mismatch (policy-based): crypto ACLs must be exact mirrors;
  the error shows "proxy identities not supported" / TS_UNACCEPTABLE.
- PFS group mismatch: phase 1 up, phase 2 fails.

## 4. Debug safely
```
debug crypto condition peer ipv4 203.0.113.20     ! limit debugs to one peer
debug crypto ikev2
debug crypto ikev2 error
debug crypto ipsec
undebug all
```
Log to buffer (`logging buffered 1000000 debugging`, `no logging console`) before debugging on
a busy head-end.

## Clear
`clear crypto session remote 203.0.113.20` re-negotiates one peer; avoid `clear crypto sa`
globally on a hub.

## Verify
- [ ] IKE SA READY/QM_IDLE, IPsec SA with both encaps and decaps rising.
- [ ] NAT exemption in place on both sides (`show ip nat translations` has no VPN flows).
- [ ] Rekey and DPD behave over a lifetime period.
