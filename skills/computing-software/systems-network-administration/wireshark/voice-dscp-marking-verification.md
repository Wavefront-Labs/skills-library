---
id: computing-software.systems-network-administration.wireshark.voice-dscp-marking-verification
name: voice-dscp-marking-verification
category: computing-software
field: systems-network-administration
product: wireshark
tags: [wireshark, voice-dscp, dscp, dscp-ef, qos-verification, ip-dsfield, voip, cs3]
level: practitioner
status: verified
description: "Check in a capture that voice media carries DSCP EF and signalling CS3 end to end, find where markings are rewritten, and build columns and filters for it."
sources:
  - https://www.rfc-editor.org/rfc/rfc4594
  - https://www.wireshark.org/docs/dfref/i/ip.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Voice DSCP marking verification

QoS works only if packets carry the right marking at each queue. A capture proves it.

## Expected markings (RFC 4594 / common practice)
| Traffic | DSCP | Value | ToS byte |
|---|---|---|---|
| Voice RTP (telephony bearer) | EF | 46 | 0xb8 |
| Signalling, RFC 4594 | CS5 | 40 | 0xa0 |
| Signalling, common vendor practice | CS3 | 24 | 0x60 |
| Video conferencing (RFC 4594 multimedia conferencing) | AF41 | 34 | 0x88 |
RFC 4594 assigns CS5 to IP telephony signalling and CS3 to broadcast video; CS3 for SIP/SCCP is vendor practice. Use the
value in your own QoS policy and change the SIP filter below to match. ToS byte = DSCP x 4.

## Filters and columns
```
rtp && ip.dsfield.dscp != 46          # voice packets not marked EF
sip && ip.dsfield.dscp != 24          # if your policy is CS3
ipv6.tclass.dscp != 46 && rtp         # IPv6
```
Add `ip.dsfield.dscp` as a column; Statistics > Conversations or I/O graph with filter
`ip.dsfield.dscp == 46` shows how much traffic is marked.

## Find the remarking point
Capture at several points (phone access port, uplink, WAN edge, far side):
- Phone sends EF, access switch output shows 0 -> the switch port is not trusting the phone's marking (check the platform's trust settings).
- Marked across the LAN, 0 after the WAN -> provider bleaching or wrong MPLS class mapping.
- A softphone may send DSCP 0 if the operating system does not mark its traffic; verify in the capture and fix with OS policy or switch reclassification.

## Marking is not treatment
A correct EF marking means nothing if the queue is not configured. Correlate with interface
queue statistics on your platform and RTP jitter/loss.

## Verify
- [ ] Voice media EF and signalling CS3 at every capture point up to the trust boundary of the provider.

## Checked (2026-10-22)
- Built a synthetic SIP/RTP capture with scapy (RTP with IP ToS 0xb8, SIP at 0x60 and two untagged SIP packets) and ran on Wireshark 4.4.1: `ip.dsfield.dscp == 46` matched the RTP (ip.dsfield 0xb8), `rtp && ip.dsfield.dscp != 46` matched 0 packets, `sip && ip.dsfield.dscp != 24` flagged exactly the two untagged SIP packets of call3x; `ip.dsfield.dscp` and `ipv6.tclass.dscp` exist in `tshark -G fields`. ToS arithmetic: 46x4=0xb8, 24x4=0x60, 34x4=0x88, 40x4=0xa0.
- RFC 4594 (https://www.rfc-editor.org/rfc/rfc4594.txt) service class table read: Telephony EF, Signaling CS5, Multimedia Conferencing AF41/42/43, Broadcast Video CS3. The old text attributed CS3 signalling to RFC 4594; corrected.
- Removed the Cisco trust-command and `show policy-map` specifics (not verified); the softphone remark is now a conditional (check in a capture).
