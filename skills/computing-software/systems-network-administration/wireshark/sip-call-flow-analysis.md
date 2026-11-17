---
id: computing-software.systems-network-administration.wireshark.sip-call-flow-analysis
name: sip-call-flow-analysis
category: computing-software
field: systems-network-administration
product: wireshark
tags: [wireshark, sip-flows, voip-calls, sip, sdp, flow-sequence, voip, telephony]
level: practitioner
status: verified
description: "Reconstruct VoIP calls in Wireshark with Telephony > VoIP Calls and SIP Flows: call ladders, SDP media negotiation, failure response codes and one-way audio clues."
sources:
  - https://www.wireshark.org/docs/wsug_html_chunked/ChTelVoipCalls.html
  - https://www.rfc-editor.org/rfc/rfc3261
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# SIP call flow analysis

## Find the calls
Telephony > **VoIP Calls**: one row per call with From/To, state (CALL SETUP, RINGING, IN CALL, CANCELLED,
COMPLETED, REJECTED, UNKNOWN in the 4.4.1 source), duration. Select a call > **Flow Sequence** for a ladder diagram of
SIP and the RTP streams. Telephony > **SIP Flows** lists SIP dialogs only.
SIP on a non-standard port: Decode As SIP (CLI `-d udp.port==5070,sip`), or enable "Try heuristic sub-dissectors".

## Normal call
INVITE (with SDP offer) -> 100 Trying -> 180 Ringing / 183 Session Progress (early media) ->
200 OK (SDP answer) -> ACK -> RTP both ways -> BYE -> 200 OK.

## Failure codes
| Code | Usually |
|---|---|
| 401/407 | auth challenge (normal once, a loop = wrong credentials) |
| 403 | forbidden: dial plan, trunk not allowed |
| 404 | number unknown |
| 408 | timeout to next hop |
| 480/486 | unavailable/busy |
| 488 | codec mismatch (no common codec in SDP) |
| 503 | trunk or server down/overloaded |

## SDP and one-way audio
Check `c=` (connection IP) and `m=audio <port>` in INVITE and 200 OK:
- A private IP in SDP sent to a public peer = NAT problem (missing SBC/ALG handling); the far
  end sends RTP to an unroutable address -> one-way audio.
- Filter `sdp` and add `sdp.connection_info.address`, `sdp.media.port` columns.
- No RTP in one direction in the Flow Sequence = firewall/NAT, not the codec.
- SIP ALG rewriting badly: compare SDP before and after the firewall (two capture points).

## Encrypted signalling
SIP over TLS (default port 5061, `sip.tls.port`) needs keys; SRTP media cannot be played without the SDES/DTLS keys.

## Verify
- [ ] Failing call located, the failing message and side identified, SDP addresses/codecs checked.

## Checked (2026-10-22)
- Built a synthetic SIP/SDP/RTP capture with scapy (one completed call with 150 RTP packets per direction, a 407-then-488 call whose SDP leaks 192.168.1.20, a 404 call) and ran on Wireshark 4.4.1: RTP/RTCP/RTPEvent were decoded with no heuristics (rtp_udp default off in `tshark -G heuristic-decodes`), proving the SDP-driven setup; `sdp.connection_info.address` and `sdp.media.port` columns returned 10.0.0.1:16384, 10.0.0.2:20000 and the leaked private 192.168.1.20:16400; `tshark -z sip,stat` counted the 407/488/404/200/180/100 replies and the INVITE/ACK/BYE/REGISTER methods; `-z rtp,streams` listed both directions.
- VoIP Calls state names read in ui/voip_calls.c (tag wireshark-4.4.1); the Wireshark User's Guide (https://www.wireshark.org/docs/wsug_html_chunked/ChTelVoipCalls.html) states that SIP Flows shows SIP only while VoIP Calls shows all protocols, and that Flow Sequence and Play Streams are available from both. SIP status code names (401, 403, 404, 407, 408, 480, 486, 488, 503, 603) checked against the IANA SIP parameters registry.
- The "usually" meanings in the failure table are interpretation of those standard code names, not tested against live gear.
