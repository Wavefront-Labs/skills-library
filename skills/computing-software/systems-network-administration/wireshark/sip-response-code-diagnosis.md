---
id: computing-software.systems-network-administration.wireshark.sip-response-code-diagnosis
name: sip-response-code-diagnosis
category: computing-software
field: systems-network-administration
product: wireshark
tags: [wireshark, sip, sip-response-codes, voip, registration, sip-trunk, codec-negotiation, sdp]
level: practitioner
status: verified
description: "Diagnose failed VoIP calls and registrations from SIP response codes: 401/407 challenges, 403/404/408/480/486/488/503, SDP codec mismatches, and NAT-related one-way audio clues."
sources:
  - https://www.rfc-editor.org/rfc/rfc3261#section-21
  - https://www.rfc-editor.org/rfc/rfc4566
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# SIP response code diagnosis

## Find the failures
```
sip.Status-Code >= 400
sip.Method == "REGISTER"
sip.Call-ID == "a84b4c76e66710"
```
`tshark -q -z sip,stat` (GUI: Telephony > SIP Statistics) counts responses by code; Telephony > VoIP Calls > Flow Sequence shows a
ladder per call.

## What the codes usually mean
| Code | Meaning in practice |
|---|---|
| 100/180/183 | trying / ringing / session progress (183 often carries early media SDP) |
| 401 / 407 | authentication challenge; normal once, then the request repeats with credentials. Repeated 401 = wrong password or realm |
| 403 Forbidden | credentials OK but not allowed: IP not whitelisted on the trunk, number not permitted, account suspended |
| 404 Not Found | dialled number/user unknown at the target (dial plan, number format E.164 vs national) |
| 408 Request Timeout | no final response: far end unreachable, firewall dropping |
| 480 Temporarily Unavailable | user not registered/DND |
| 486 Busy Here | busy |
| 487 Request Terminated | caller cancelled (CANCEL sent), normal |
| 488 Not Acceptable Here | no common codec or SDP problem |
| 500 / 503 | server error / overloaded or trunk down; 503 from a carrier often means routing failure |
| 603 Decline | callee rejected |

## SDP and 488
Compare `m=audio` lines and `a=rtpmap` in the INVITE's SDP with what the far end accepts.
```
sdp.media.format
sdp.connection_info
```
Codec lists with no overlap (G.729 only vs G.711 only) or SRTP required on one side (`RTP/SAVP`)
versus plain RTP give 488.

## NAT clues (registrations drop, one-way audio)
- `c=IN IP4 192.168.1.20` in SDP sent to the internet: private address leaked; media goes nowhere.
- `Via` received/rport parameters differ from the sent address: NAT in path.
- Registrations expiring because NAT pinholes time out before re-REGISTER (a long `Expires` against a shorter UDP NAT
  mapping timeout; check your NAT's value). Shorten expiry or enable keepalives.
- SIP ALG on the firewall rewriting headers inconsistently: disable it as a first test.

## Verify
- [ ] For each failed call: Call-ID, request, final code, which hop sent it (Via/Server/User-Agent),
  and the SDP offer/answer.

## Checked (2026-10-22)
- Ran the three filters from the skill on a synthetic scapy SIP capture with Wireshark 4.4.1: `sip.Status-Code >= 400` returned 407, 488 and 404 with their Call-IDs, `sip.Method == "REGISTER"` returned the REGISTER, `sip.Call-ID == "call1abc"` returned that dialog's 7 messages; `sdp.media.format`, `sdp.connection_info` exist and returned values (`ITU-T G.711 PCMU,DynamicRTP-Type-101,0,101,101` and `IN IP4 192.168.1.20` for the leaked address); `tshark -z sip,stat` produced the per-code counts.
- All code names in the table (100/180/183, 401, 403, 404, 407, 408, 480, 486, 487, 488, 503, 603) matched the IANA SIP parameters registry https://www.iana.org/assignments/sip-parameters/ ; `RTP/SAVP` is the SRTP SDP profile name (RFC 3711). The 500 row is the generic server-error class. The practical-cause column and NAT remarks are interpretation, not captured.
