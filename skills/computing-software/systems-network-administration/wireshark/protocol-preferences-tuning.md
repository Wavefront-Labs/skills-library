---
id: computing-software.systems-network-administration.wireshark.protocol-preferences-tuning
name: protocol-preferences-tuning
category: computing-software
field: systems-network-administration
product: wireshark
tags: [wireshark, protocol-preferences, preferences, dissector-settings, tshark-o]
level: practitioner
status: verified
description: "Find and set Wireshark protocol preferences (ports, reassembly, decoding options) in the GUI, preferences file and tshark -o to fix misleading dissection."
sources:
  - https://www.wireshark.org/docs/wsug_html_chunked/ChCustPreferencesSection.html
  - https://www.wireshark.org/docs/man-pages/tshark.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Protocol preferences

Many "Wireshark is wrong" moments are a protocol preference: wrong port, reassembly off, a
heuristic disabled.

## Finding them
- Right-click a protocol in the details pane > Protocol Preferences: shows that protocol's options
  inline (fastest path).
- Edit > Preferences > Protocols > <name> for the full list; Advanced lists every pref with its
  internal name and whether it is changed from default (bold).

## Common settings worth knowing
| Pref | Effect |
|------|--------|
| `tcp.desegment_tcp_streams` | reassemble PDUs spanning segments (on by default) |
| `tcp.analyze_sequence_numbers` | enables tcp.analysis.* flags |
| `tcp.calculate_timestamps` | adds tcp.time_delta / time_relative |
| `http.tls.port` | extra TLS ports for HTTP (default 443; `http.ssl.port` is rejected as obsolete) |
| `http.tcp.port` | still accepted by `-o` for extra HTTP ports but not listed by `-G currentprefs`; use Decode As (`-d tcp.port==8888,http`) |
| `tls.keylog_file` | TLS decryption key log |
| `sip.display_raw_text` | show raw SIP text |
| `ip.check_checksum` | off by default; enable only on mirrored traffic |
| `rtp.heuristic_rtp` | legacy name still accepted by `-o`; it turns on the `rtp_udp` heuristic (prefer `--enable-heuristic rtp_udp`) |

## tshark and files
```
tshark -o tcp.desegment_tcp_streams:FALSE -o "http.tcp.port:80,8080,8888" -r in.pcapng
tshark -G currentprefs | grep '^#*http'
```
`-G currentprefs` prints every preference as `#name: value` (commented while at its default) with the help text
above it. An unknown `-o` name fails with `specifies unknown preference`; a removed one with `specifies obsolete
preference`.
Preferences are saved in the profile's `preferences` file as `name: value` lines; only changed
values are uncommented. Port-style options now live in Decode As and the heuristic list rather than in
Preferences.

## Gotchas
- Changes are per profile; a teammate using another profile sees different results.
- Disabling reassembly makes HTTP/TLS look broken; enabling it hides individual segment timing.
  Know which view you need.

## Verify
- [ ] After changing a pref, the details pane shows the expected decode and `tshark -G currentprefs` reflects it.

## Checked
Run with TShark 4.4.1: defaults read from `tshark -G currentprefs` (`tcp.desegment_tcp_streams` TRUE,
`tcp.analyze_sequence_numbers` TRUE, `tcp.calculate_timestamps` TRUE, `ip.check_checksum` FALSE, `sip.display_raw_text`
FALSE, `http.tls.port` 443, `tls.keylog_file` empty). With `--disable-heuristic http_tcp`, `-o http.tcp.port:8888` and
`-d tcp.port==8888,http` both decoded HTTP on a synthetic port-8888 stream while the default run showed plain TCP;
`-o http.ssl.port:443` printed "specifies obsolete preference"; `-o rtp.heuristic_rtp:TRUE` made 5 RTP packets appear
(same result as `--enable-heuristic rtp_udp`) although the name is absent from `-G currentprefs`;
`-o tcp.desegment_tcp_streams:FALSE` accepted. Right-click "Protocol Preferences" is in the User's Guide (802.11 chapter).
