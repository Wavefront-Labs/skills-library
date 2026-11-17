---
id: computing-software.systems-network-administration.wireshark.tcp-protocol-preferences-relative-sequence
name: tcp-protocol-preferences-relative-sequence
category: computing-software
field: systems-network-administration
product: wireshark
tags: [wireshark, tcp-analysis, relative-sequence-numbers, tcp-preferences, reassembly]
level: practitioner
status: verified
description: "Set the Wireshark TCP preferences that change analysis: relative sequence numbers, reassembly, timestamps, window scaling guess and checksums."
sources:
  - https://www.wireshark.org/docs/wsug_html_chunked/ChAdvTCPAnalysis.html
  - https://www.wireshark.org/docs/dfref/t/tcp.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# TCP protocol preferences

Edit > Preferences > Protocols > TCP (or right-click the TCP layer > Protocol Preferences).

| Preference | Default | When to change |
|------------|---------|----------------|
| Relative sequence numbers (`tcp.relative_sequence_numbers`; also needs Analyze TCP sequence numbers on) | on | off when comparing seq numbers with a capture from the other side of a firewall that randomises ISNs, or with logs that show absolute numbers |
| Analyze TCP sequence numbers (`tcp.analyze_sequence_numbers`) | on | off only for speed on huge files; disables retransmission/dup ACK flags |
| Allow subdissector to reassemble TCP streams (`tcp.desegment_tcp_streams`) | on | off to see per-segment timing of HTTP/TLS records |
| Calculate conversation timestamps (`tcp.calculate_timestamps`) | on (TRUE in `tshark -G currentprefs`, 4.4.1) | off only to save work; on gives `tcp.time_relative` and `tcp.time_delta` (with FALSE `tcp.time_delta` was empty) |
| Scaling factor to use when not available from capture (`tcp.default_window_scaling`) | Not known | set the shift count, e.g. `-o tcp.default_window_scaling:7` (multiply by 128), when the handshake is missing so window sizes are not understated; `:128` is not a valid value |
| Validate the TCP checksum | off | on only for SPAN/tap captures; host captures show offload errors |
| Try heuristic sub-dissectors first | off | on when proprietary protocols use well-known ports |
| Do not call subdissectors for error packets (`tcp.no_subdissector_on_error`) | on (TRUE in 4.4.1) | off to see application decodes of retransmitted/out-of-order segments |

## tshark
```
tshark -r in.pcapng -o tcp.relative_sequence_numbers:FALSE -T fields -e tcp.seq_raw -e tcp.seq
tshark -r in.pcapng -o tcp.calculate_timestamps:TRUE -Y "tcp.time_delta > 0.5"
```
`tcp.seq_raw` and `tcp.ack_raw` always hold absolute values regardless of the preference (run: with relative numbers off
`tcp.seq` equalled `tcp.seq_raw`; with them on, a SYN with raw sequence 1 showed `tcp.seq` 0).
Defaults above were read from `tshark -G currentprefs` and the `-o` forms were run; with `tcp.analyze_sequence_numbers:FALSE`
the count of `tcp.analysis.flags` packets dropped from 18 to 0 on a test capture.

## Gotchas
- Captures without the SYN: the window scale factor shows as -1 (unknown) and `tcp.window_size` is the unscaled value;
  with `tcp.default_window_scaling:7` the same packets showed factor 128 and a scaled window (8192 became 1048576).
- Different preferences between analysts produce different tcp.analysis results; state them in reports.

## Verify
- [ ] Sequence numbers in both side captures line up (using `tcp.seq_raw` offset by the firewall ISN delta).
