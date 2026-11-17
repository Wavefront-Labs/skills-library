---
id: computing-software.systems-network-administration.cisco-networking.bgp-session-security-md5-gtsm
name: bgp-session-security-md5-gtsm
category: computing-software
field: systems-network-administration
product: cisco-networking
tags: [cisco, bgp, bgp-md5, ttl-security, gtsm, tcp-ao, maximum-prefix, peering-security]
level: practitioner
status: docs-checked
description: "Protect BGP sessions on IOS: TCP MD5 passwords versus TCP-AO, GTSM ttl-security, maximum-prefix limits, and what happens when you change an MD5 password."
sources:
  - https://www.rfc-editor.org/rfc/rfc5082
  - https://www.rfc-editor.org/rfc/rfc5925
  - https://www.rfc-editor.org/rfc/rfc7454
  - https://www.cisco.com/c/en/us/td/docs/ios-xml/ios/iproute_bgp/command/irg-cr-book/bgp-m1.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# BGP session security

RFC 7454 (BGP operations and security) covers session protection: authenticate the TCP session, make spoofing
harder with TTL security, and cap what a peer can send. Protecting the TCP session is NOT REQUIRED by RFC 7454 even
at shared networks such as IXPs, but operators are recommended to weigh the trade-offs and apply it where appropriate.
The cost is the extra configuration and key management.

## TCP MD5 password (RFC 2385)
```
router bgp 109
 neighbor 10.108.1.1 password <shared-secret>
```
- Same password on both peers, or the session is not made. The IOS page says up to 25 characters, case-sensitive,
  first character not a number, and no "number-space-anything" form (the space after the number can break
  authentication).
- Missing password on one side logs `%TCP-6-BADAUTH: No MD5 digest from <peer>:<port> to <local>:179`; different
  passwords log `Invalid MD5 digest`.
- Changing the password on an established session does not tear it down. The local router keeps trying with the new
  password until the hold-down timer expires (default 180 s), so set the same password on the remote router within
  that time. A new hold timer value only takes effect after a session reset.

## TCP-AO (RFC 5925)
- Obsoletes TCP MD5; RFC 7454 says TCP-AO SHOULD be preferred when implemented (MD5 remains the most used because
  vendors support it).
- Keys are Master Key Tuples with a SendID and a RecvID; the TCP-AO option carries the KeyID, and the RFC's examples
  use HMAC-SHA1 and AES-CMAC as MACs. A connection uses either TCP-AO or TCP MD5, never both at once; a TCP
  implementation that supports MD5 must support TCP-AO.
- TCP-AO cannot interoperate natively across NAT/NAPT devices, which change addresses or ports.
- The IOS XE TCP-AO key-chain syntax is not covered by the Cisco command page used here; look it up in the platform
  BGP configuration guide for your release.

## GTSM / ttl-security (RFC 5082)
Instead of TTL 1, the speakers send BGP packets with TTL 255 and the receiver checks for 255; a packet from a host
that is not directly connected cannot arrive with TTL 255. RFC 7454: implement it on directly connected peerings;
it must be configured on both ends; on multihop peerings it works with a suitable TTL but is weaker because anyone
inside the TTL diameter can spoof it.
```
router bgp 109
 neighbor 10.0.0.1 ttl-security hops 1
```
IOS page: `hops` is 1-254 and the router derives the TTL from it (hops 2 accepts TTL 253 or higher). It protects the
incoming direction only, packets below the value are dropped silently with no ICMP, it is not supported for iBGP
peers, and it cannot be combined with `neighbor ebgp-multihop` on the same peer. It does not help against a peer
compromised inside your network.

## Prefix limits
```
router bgp 40000
 neighbor 192.168.3.3 maximum-prefix 2000 restart 30
```
Syntax: `maximum [threshold] [discard-extra] [restart minutes] [warning-only]`. Warning threshold defaults to 75 percent
(1-100). Disabled by default; when exceeded the session is torn down, and without `restart` it stays down until
`clear ip bgp`. `restart` is 1-65535 minutes; `warning-only` only logs. `discard-extra` was added in IOS XE 17.13.1a.

## Verify
- [ ] Session reaches Established after the change, with no `%TCP-6-BADAUTH` messages on either side.
- [ ] `show ip bgp neighbors <ip>` lists the session (the Cisco page names this command for TCP and BGP connection
  details).

## Checked
Date: 2026-11-08. Read in full or in the relevant sections: RFC 7454 section 5 (session protection, GTSM), RFC 5082
introduction and GTSM text, RFC 5925 abstract, key and middlebox sections, and the Cisco IOS BGP command reference
entries `neighbor password`, `neighbor ttl-security`, `neighbor maximum-prefix`, `neighbor ebgp-multihop`.
Confirmed: items stated above with their page sources.
Removed: the IOS XE TCP-AO key-chain config and `hmac-sha-256` (RFC 5925 names HMAC-SHA1 and AES-CMAC), "IOS XE
16.x+", `password 7`, "dropped in hardware", the 80 percent warning (default is 75), the PeeringDB advice, "MD5
through NAT works", the iBGP loopback `hops 2` advice (unsupported for iBGP), the CoPP note, `show tcp brief` and the
`include` filter command.
Method: documentation only; no commands were run.
