---
id: computing-software.systems-network-administration.wireshark.rtp-dtmf-rfc4733-events
name: rtp-dtmf-rfc4733-events
category: computing-software
field: systems-network-administration
product: wireshark
tags: [wireshark, dtmf, rfc4733, rfc2833, voip, telephone-event]
level: practitioner
status: verified
description: "Find and decode DTMF in VoIP captures: RFC 4733 telephone-events, SIP INFO and in-band tones, payload type negotiation and duplicate/missing digit problems."
sources:
  - https://www.rfc-editor.org/rfc/rfc4733
  - https://www.wireshark.org/docs/dfref/r/rtpevent.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# RFC 4733 DTMF events

DTMF can travel three ways; mismatched methods between endpoints cause IVR digit failures.

| Method | How it looks in Wireshark |
|--------|---------------------------|
| RFC 4733 (formerly 2833) | RTP packets with the telephone-event payload type, protocol `RTPEvent` |
| SIP INFO | `sip.Method == "INFO"` carrying a DTMF body (the body format is vendor-specific) |
| In-band | audio tones inside G.711; only audible in RTP Player, unreliable with compressed codecs |

## Negotiation
SDP must agree on the dynamic payload type:
```
m=audio 16384 RTP/AVP 0 101
a=rtpmap:101 telephone-event/8000
a=fmtp:101 0-16
```
If one side offers 101 and the other answers 96, or omits it, events are dropped or sent as audio.
Decode As if the PT is unusual: Analyze > Decode As > `rtp.pt` value -> RTP Event (CLI `-d rtp.pt==101,rtpevent`); 4.4.1 has no RTPevent payload-type preference.

## Filters and tools
```
rtpevent
rtpevent.event_id == 5
rtpevent.end_of_event == 1
```
Telephony > RTP > RTP Streams shows event packets in the stream; Telephony > VoIP Calls > Flow
Sequence shows digits on the flow diagram.

## Reading events
Each digit sends several packets with the same RTP timestamp and growing duration, and three
redundant end packets (E bit). Count digits by unique timestamps with E bit set.

## Problems
- Double digits: endpoint sends both RFC 4733 and in-band, or the gateway converts and passes both.
- Missing digits: PT mismatch, transcoder stripping events, or SBC configured for SIP INFO.

## Verify
- [ ] Each pressed digit appears once as an RTPEvent with end_of_event set, at the negotiated PT.

## Checked (2026-10-22)
- Ran on Wireshark 4.4.1 over a scapy-built call whose SDP offers `m=audio .. RTP/AVP 0 101`, `a=rtpmap:101 telephone-event/8000`, `a=fmtp:101 0-16`, with one DTMF digit 5 sent as 6 RTP packets at PT 101 (same RTP timestamp, durations 160/320/480/640, last three with the E bit): the protocol showed as `RTP EVENT` ("DTMF Five 5"), `rtpevent.event_id == 5` and `rtpevent.end_of_event == 1` matched 6 and 3 packets, `rtpevent.duration` grew, `-d rtp.pt==0,rtpevent` reassigned a payload type (Decode As works), and `tshark -G defaultprefs` has no RTPevent PT preference (the skill's old menu path was wrong).
- RFC 4733 text: obsoletes RFC 2833, SDP example `a=fmtp:100 0-15,66,70`, the final packet SHOULD be sent three times (https://www.rfc-editor.org/rfc/rfc4733.txt). The `0-16` in the skill's fmtp line is an example event range; use the list your endpoints negotiate.
- Not tested: SIP INFO DTMF, in-band DTMF, double-digit and missing-digit causes (interpretation).
