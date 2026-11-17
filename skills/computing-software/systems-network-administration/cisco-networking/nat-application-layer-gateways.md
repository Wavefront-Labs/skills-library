---
id: computing-software.systems-network-administration.cisco-networking.nat-application-layer-gateways
name: nat-application-layer-gateways
category: computing-software
field: systems-network-administration
product: cisco-networking
tags: [cisco, cisco-ios, ios-xe, nat, nat-alg, sip-alg, ftp-alg, dns-alg, nat-translation, voip-troubleshooting]
level: practitioner
status: draft
description: "Understand IOS NAT ALGs (FTP, SIP, H.323, DNS, etc.), the symptoms they cause, and how to disable specific ALGs such as SIP safely."
sources:
  - https://www.cisco.com/c/en/us/td/docs/ios-xml/ios/ipaddr_nat/configuration/xe-16/nat-xe-16-book/iadnat-applev-gateway.html
  - https://www.cisco.com/c/en/us/support/docs/ip/network-address-translation-nat/212137-Troubleshoot-Network-Address-Translation.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# NAT ALGs and when to disable them

## What an ALG does
Some protocols carry IP addresses and ports **inside the payload** (FTP PORT/PASV, SIP/SDP, H.323,
RTSP, DNS A records, Skinny). Plain NAT rewrites only headers, so the far end gets an
untranslated private address. The ALG inspects and rewrites the payload and opens pinholes for
secondary connections.

IOS XE NAT enables ALGs for: FTP, TFTP, DNS, SIP, SCCP (Skinny), H.323, RTSP, NetBIOS, PPTP,
ICMP and others by default on standard ports.

## When ALGs hurt
- **SIP ALG + a SIP-aware endpoint/SBC/provider that already handles NAT** (STUN, rport, SBC
  far-end NAT traversal): double rewrite, one-way audio, calls drop at 30 s, registration flaps.
  Most VoIP providers say disable SIP ALG.
- Encrypted payloads (FTPS, SIP over TLS) cannot be inspected: ALG does nothing; firewall must allow ports.
- Non-standard ports bypass the ALG (FTP on 2121) unless you map them.
- Performance: ALG traffic is processed in slower paths on some platforms.

## Disable per ALG (IOS XE)
```
no ip nat service sip udp port 5060
no ip nat service sip tcp port 5060
no ip nat service skinny tcp port 2000
show ip nat translations verbose
show platform hardware qfp active feature alg statistics sip   ! ASR/ISR XE
```
Map a non-standard port: `ip nat service ftp tcp port 2121`.

## Diagnose
1. Capture on inside and outside (`monitor capture`), compare SDP `c=` and `m=` lines or FTP PORT commands.
2. If outside still shows 10.x addresses, ALG is not applied; if addresses are rewritten twice,
   ALG + endpoint NAT handling conflict.
3. Check provider guidance before choosing; disabling SIP ALG with a provider that relies on it breaks inbound calls.

## Verify
- [ ] Test call: two-way audio for > 60 s, both inbound and outbound.
- [ ] `show running-config | include ip nat service` documents every change.
