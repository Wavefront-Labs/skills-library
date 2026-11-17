---
id: computing-software.systems-network-administration.wireshark.rtp-stream-analysis-and-player
name: rtp-stream-analysis-and-player
category: computing-software
field: systems-network-administration
product: wireshark
tags: [wireshark, rtp-player, rtp, rtp-stream-analysis, jitter, packet-loss, voip, decode-as-rtp]
level: practitioner
status: verified
description: "Analyse and listen to RTP audio in Wireshark: enable RTP decoding, RTP Streams statistics for loss, jitter and sequence errors, and the RTP Player with jitter buffer."
sources:
  - https://www.rfc-editor.org/rfc/rfc3550
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# RTP stream analysis and player

## Make Wireshark see RTP
RTP is found automatically only when the SIP/SDP setting up the call is in the capture.
Otherwise: Analyze > Enabled Protocols > `rtp_udp` heuristic on (it is off by default and ignores well-known ports), or Decode As UDP port -> RTP.

## RTP Streams
Telephony > RTP > **RTP Streams**: per SSRC: payload (PCMU/G.711, G.729, Opus), packets,
lost (%), max delta, max/mean jitter.
Targets for loss and jitter come from your vendor or SLA; one-way delay under about 150 ms is the ITU-T G.114 planning figure.

Select a stream > **Analyze**: per packet delta, jitter, sequence errors, graph. Analyse
both directions (select the reverse stream too).

## RTP Player
Telephony > RTP > **RTP Player** (or from VoIP Calls > Play Streams):
- Plays any codec with an installed codec plugin; the official 4.4.1 Windows build has g711, g722, g726, g729, ilbc, l16mono, opus and sbc (`tshark -G plugins`; Help > About > Plugins > codec in the GUI).
- **Jitter buffer** setting simulates the phone: packets later than the buffer are dropped
  and shown as such. Compare "Uninterrupted" vs jitter buffer to separate network jitter from
  real loss.
- Export audio (the dialog writes .au data) or payload to a file for a ticket.
Privacy: you are listening to a real conversation; follow your organisation's lawful
intercept and privacy rules.

## Reading problems
- Loss bursts on one direction only -> a congested link or queue on that path.
- Sequence errors with no loss -> reordering (multipath, ECMP per-packet).
- Mark (M) bit and timestamp jumps -> silence suppression or PBX transcoding, not loss.

## Verify
- [ ] Each direction's loss and jitter measured; audible issues correlated with the stream graph.

## Checked (2026-10-22)
- Ran on Wireshark 4.4.1 against a synthetic scapy SIP+RTP capture (150 PCMU packets each way, 10 packets removed in one direction, a DTMF event burst): `tshark -z rtp,streams` listed per-SSRC payload (g711U, g711U + telephone-event), packets, lost (10 = 6.4%), min/mean/max delta and jitter, and flagged the lossy stream with `X`; RTP was recognised from SDP alone (no heuristic needed), and `tshark -G heuristic-decodes` shows `rtp_udp` default off. Decode As `rtp.pt` is listed in `tshark -G decodes`.
- Codec plugin list from `tshark -G plugins`; the Wireshark User's Guide section 9.2.4 (https://www.wireshark.org/docs/wsug_html_chunked/ChTelPlayingCalls.html) confirms SDP-based recognition, Decode As, and the `rtp_udp` heuristic caveat for well-known ports. Jitter Buffer, RTP Timestamp and Uninterrupted timing modes read in ui/qt/rtp_player_dialog.ui (tag wireshark-4.4.1); the .au export header is written in rtp_player_dialog.cpp. G.114 figure from the ITU-T PDF.
- Not tested: the GUI windows themselves (RTP Streams, Analyze, Player) and the "Reading problems" bullets (interpretation).
