---
id: computing-software.systems-network-administration.network-design.sip-and-rtp-port-ranges
name: sip-and-rtp-port-ranges
category: computing-software
field: systems-network-administration
product: network-design
tags: [network-design, rtp-port-range, sip, rtp, rtcp, srtp, voip-firewall, sip-alg]
level: practitioner
status: docs-checked
description: "Plan firewall and NAT handling for SIP signalling and RTP media: port ranges per platform, SIP ALG pitfalls, one-way audio causes and SBC placement."
sources:
  - https://www.rfc-editor.org/rfc/rfc3261
  - https://www.rfc-editor.org/rfc/rfc3550
  - https://www.rfc-editor.org/rfc/rfc3711
  - https://learn.microsoft.com/en-us/microsoftteams/prepare-network
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# SIP and RTP port ranges

## Signalling
- SIP: port 5060 for UDP and TCP, 5061 for TLS (RFC 3261). Use TLS toward carriers and over the internet.

## Media
RTP and RTCP use a port pair: RFC 3550 says the RTCP stream uses the next higher (odd) port number from the even RTP
port. The RTP port range is configured per platform (PBX, phone system, SBC) and per SIP trunk provider: read the
platform's or provider's documentation for the exact range, and open exactly that range on the firewall.
For Microsoft Teams media, use the current "Prepare your organization's network for Teams" page for required ports and
destinations (it changes), not a copied table.

Size the range from concurrent calls, with at least an RTP and an RTCP port per media stream.

## NAT and SIP
SIP carries IP addresses and ports inside the message bodies (SDP), so behind NAT you need one of:
- An SBC at the edge (preferred for trunks).
- The PBX configured with its public address, plus port forwards for SIP and the RTP range.
- STUN/TURN/ICE for clients.

Check whether a SIP ALG on the firewall is rewriting messages; if one-way audio or registration failures appear,
test with the ALG disabled unless the vendor requires it.

## One-way audio checklist
1. Capture on both sides to see whether RTP from one side never arrives.
2. Check the SDP `c=` line: a private address there means NAT is not handled.
3. Check the firewall's UDP idle timeout against silence gaps in the media.
4. Look for asymmetric routing through a stateful firewall.

## Verify
- [ ] Test call through each trunk: two-way audio, hold/resume, and a long call (session timers, re-INVITE).

## Checked
2026-10-28. Confirmed in RFC 3261 (5060 for UDP/TCP, 5061 for TLS) and RFC 3550 (RTCP on the next higher, odd, port).
Removed as unconfirmed: per-platform RTP range table (Asterisk, FreePBX, CUCM, Teams port numbers: the fetched Teams page
did not list them), the 32-second ALG symptom, UDP timeout and call-length numbers, `external_media_address`.
Method: documentation only; no commands were run.
