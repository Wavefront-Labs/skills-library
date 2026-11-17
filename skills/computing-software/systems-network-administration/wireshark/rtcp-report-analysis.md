---
id: computing-software.systems-network-administration.wireshark.rtcp-report-analysis
name: rtcp-report-analysis
category: computing-software
field: systems-network-administration
product: wireshark
tags: [voip, rtcp, rtp, jitter, packet-loss, sender-report, receiver-report, call-quality]
level: practitioner
status: verified
description: "Read RTCP sender and receiver reports for the far end view of call quality: fraction lost, cumulative loss, jitter, round-trip time from LSR/DLSR, and XR metrics."
sources:
  - https://www.rfc-editor.org/rfc/rfc3550#section-6.4
  - https://www.rfc-editor.org/rfc/rfc3611
  - https://www.wireshark.org/docs/dfref/r/rtcp.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# RTCP report analysis

RTP carries the audio; RTCP (normally RTP port + 1, or multiplexed on the same port with rtcp-mux)
carries quality reports roughly every 5 seconds. Your capture sees the RTP you receive, but RTCP
receiver reports tell you what the other side received: the only way to see loss in the direction
you cannot capture.

## Decode
If RTCP is not recognised: check Analyze > Enabled Protocols > `rtcp_udp` heuristic (on by default in 4.4.1), or Decode As
UDP port -> RTCP. SIP/SDP in the capture lets Wireshark set up conversations automatically.
```
rtcp
rtcp.pt == 200        # Sender Report
rtcp.pt == 201        # Receiver Report
rtcp.pt == 207        # Extended Report (XR)
```

## Report blocks (in SR and RR)
| Field | Meaning |
|---|---|
| `rtcp.ssrc.fraction` | fraction lost since last report, /256 (e.g. 13 = 5 %) |
| `rtcp.ssrc.cum_nr` | cumulative packets lost |
| `rtcp.ssrc.jitter` | interarrival jitter in RTP timestamp units (divide by clock rate: 8000 for G.711 -> seconds) |
| `rtcp.ssrc.lsr` / `rtcp.ssrc.dlsr` | last SR timestamp / delay since it; with arrival time gives RTT |
Wireshark computes `rtcp.roundtrip-delay` when it sees the matching SR and RR (enable "Show
roundtrip calculation" in RTCP preferences, `-o rtcp.show_roundtrip_calculation:TRUE`; off by default).

## Interpreting
- Compare fraction lost and jitter with your vendor/SLA targets; sustained non-zero loss is worth chasing.
- Loss reported by the far end but your outbound RTP looks perfect in the capture: loss after your
  capture point (WAN, provider, far LAN).
- Round-trip time: ITU-T G.114 treats one-way delay under about 150 ms as essentially transparent and 400 ms as the planning upper limit.
- RTCP XR VoIP metrics block (RFC 3611) adds burst/gap density, R-factor and MOS estimates on
  phones that send it.

## Gotchas
- Some devices never send RTCP or send it on unexpected ports (check SDP `a=rtcp:`).
- SRTP deployments use SRTCP: encrypted, reports unreadable without keys.
- Telephony > RTP > RTP Streams analyses received RTP; combine both views.

## Verify
- [ ] For a bad call, both directions' loss and jitter are known: local from RTP stream analysis,
  remote from RTCP receiver reports.

## Checked (2026-10-22)
- Ran on Wireshark 4.4.1 on a scapy-built RTP/RTCP exchange (SR with sender info plus a report block, RR with fraction 13, cumulative lost 10, jitter 80, LSR 0x8000, DLSR 3277): `rtcp.pt == 200` and `== 201` each matched one packet; the fields `rtcp.ssrc.fraction` (5 in the SR block, 13 in the RR), `rtcp.ssrc.cum_nr`, `rtcp.ssrc.jitter`, `rtcp.ssrc.lsr`, `rtcp.ssrc.dlsr` decoded as injected; 13/256 = 5.1 %, jitter 80 / 8000 = 10 ms. `rtcp.roundtrip-delay` stays empty until `rtcp.show_roundtrip_calculation` is TRUE (default FALSE), after which a value appears (my synthetic timing makes it meaningless: -49).
- `tshark -G heuristic-decodes`: `rtcp_udp` T T by default. RFC 3550: RTCP on the next higher (odd) port, 5 s recommended minimum report interval (https://www.rfc-editor.org/rfc/rfc3550.txt); RFC 5761 `a=rtcp-mux`; IANA RTCP packet types 200 SR, 201 RR, 207 XR; RFC 3611 VoIP Metrics block contains R factor, MOS-LQ and MOS-CQ. G.114 figures from the ITU PDF.
- Not tested: SRTCP, devices omitting RTCP (advice), RTCP XR packets in a capture.
