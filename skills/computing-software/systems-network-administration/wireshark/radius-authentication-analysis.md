---
id: computing-software.systems-network-administration.wireshark.radius-authentication-analysis
name: radius-authentication-analysis
category: computing-software
field: systems-network-administration
product: wireshark
tags: [wireshark, radius-analysis, radius, aaa, 802-1x, protocol-analysis]
level: practitioner
status: verified
description: "Analyse RADIUS in Wireshark: Access-Request/Accept/Reject/Challenge flow, attributes and VSAs, shared-secret decoding, response times and retransmissions."
sources:
  - https://www.rfc-editor.org/rfc/rfc2865
  - https://www.rfc-editor.org/rfc/rfc2866
  - https://www.wireshark.org/docs/dfref/r/radius.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# RADIUS analysis

Ports: UDP 1812 auth / 1813 accounting (legacy 1645/1646), CoA 3799; RadSec TCP 2083 (TLS).

## Filters
```
radius
radius.code == 1             # Access-Request; 2 Accept; 3 Reject; 11 Challenge; 4/5 Accounting
radius.code == 3
radius.req.dup               # retransmitted request
radius.time > 1              # response time
radius.User_Name == "jdoe"
radius.Calling_Station_Id    # client MAC (802.1X) or phone number
```
`tshark -q -z radius,rtd` (GUI: Statistics, RADIUS response time) gives min/max/avg per message type.

## Decoding hidden attributes
Set the shared secret: Preferences > Protocols > RADIUS > Shared Secret (`radius.shared_secret`; `radius.validate_authenticator` is off by
default). Wireshark then decodes User-Password and can validate authenticators. Wrong secret in the NAS: the server cannot verify the request and RFC 2865 says such packets are silently discarded
(no reply, NAS retransmits); server logs usually name an authenticator problem.

## Flow patterns
- 802.1X/EAP: Access-Request with EAP-Message, Access-Challenge, repeated many times (TLS inside
  EAP), then Accept with VLAN attributes (Tunnel-Type 13, Tunnel-Medium-Type 6,
  Tunnel-Private-Group-Id) or dACL/VSAs (`Cisco-AVPair`).
- Reject: check `Reply-Message` and server logs; the packet rarely says why.
- No reply at all: firewall, wrong server IP on NAS, or unknown client (NAS not defined on server).

## Accounting
Start/Interim/Stop records with Acct-Session-Id; mismatched Stop records explain stale sessions.

## Verify
- [ ] Request/response pairs have matching identifiers and response times under the NAS retransmit timeout (check the NAS configuration).

## Checked (2026-10-22)
- Built Access-Request/Reject/Accept and Accounting-Request packets with scapy and ran on Wireshark 4.4.1: `radius.code == 1` matched 2, `== 3` 1, `== 4` 1, `radius.time > 0.3` the 0.51 s reject, `radius.User_Name == "jdoe"` and `radius.Calling_Station_Id` matched, `radius.req.dup` matched 0 (no retransmits sent); Tunnel-Type 13, Tunnel-Medium-Type 6 and Tunnel-Private-Group-Id 20 decoded from the Access-Accept; `tshark -q -z radius,rtd` printed Access min 10 ms, max 510 ms, avg 260 ms; prefs `radius.shared_secret` and `radius.validate_authenticator` exist in `tshark -G defaultprefs`.
- RFC 2865 code table (1 Request, 2 Accept, 3 Reject, 11 Challenge) and RFC 2866 (4 Accounting-Request, 5 Accounting-Response), legacy ports 1645/1646 mentioned in those RFCs, IANA port registry (radius 1812, radius-acct 1813, radsec 2083, radius-dynauth 3799), IANA RADIUS attribute names for 18, 31, 40, 44, 64, 65, 81, RFC 3580 (`Tunnel-Type=VLAN (13)`, `Tunnel-Medium-Type=802`) and RFC 2865 "silently discarded" wording all read. The CoA port 3799 is registered as radius-dynauth.
- Not tested: EAP flows, Cisco-AVPair VSAs and the failure-cause bullets (interpretation).
