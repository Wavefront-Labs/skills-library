---
id: computing-software.systems-network-administration.wireshark.tcp-keepalive-analysis
name: tcp-keepalive-analysis
category: computing-software
field: systems-network-administration
product: wireshark
tags: [wireshark, tcp-keepalive, tcp-analysis, idle-timeout, firewall-timeout]
level: practitioner
status: verified
description: "Identify TCP keep-alives and keep-alive ACKs in Wireshark, tell them from zero-window probes, and use them to diagnose idle-timeout drops by firewalls."
sources:
  - https://www.wireshark.org/docs/wsug_html_chunked/ChAdvTCPAnalysis.html
  - https://www.rfc-editor.org/rfc/rfc9293
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# TCP keep-alives

A keep-alive is a segment with sequence number one less than the next expected byte, carrying 0 or
1 byte of data, sent after an idle period to check the peer is still there.

## Filters
```
tcp.analysis.keep_alive
tcp.analysis.keep_alive_ack
tcp.analysis.keep_alive || tcp.analysis.keep_alive_ack
```
Wireshark marks them in the Info column as `[TCP Keep-Alive]` and `[TCP Keep-Alive ACK]`.
Zero-window probes are different: they follow a `[TCP ZeroWindow]` from the peer, carry 1 byte at the *next* sequence
number (a keep-alive uses next - 1), and are shown as `[TCP ZeroWindowProbe]`:
`tcp.analysis.zero_window_probe` (run in Wireshark 4.4.1 on a synthetic capture: next-1 with 1 byte was flagged
Keep-Alive, next with 1 byte after a zero window was flagged ZeroWindowProbe and the reply ZeroWindowProbeAck).

## Default timers
| OS | Idle before first probe | Interval | Probes |
|----|-------------------------|----------|--------|
| Linux | `net.ipv4.tcp_keepalive_time` 7200 s | `tcp_keepalive_intvl` 75 s | `tcp_keepalive_probes` 9 |
| Windows | `KeepAliveTime` 7,200,000 ms (2 h) | `KeepAliveInterval` 1000 ms | confirm the probe count for your Windows build |
Linux values are the documented defaults in the kernel `ip-sysctl` file; Windows values are the documented registry defaults (Winsock `SO_KEEPALIVE` page).
Applications often set their own (OpenSSH `ServerAliveInterval` in `ssh_config`, database drivers, HTTP clients).

## Diagnosing idle drops
Symptom: long-lived connections (DB pools, SSH, VPN control) die after N minutes idle.
1. Find the last packet before the failure: `frame.time_delta_displayed` on the stream.
2. If the idle gap exceeds the firewall/NAT/LB idle timeout (AWS NAT gateway 350 s and Azure Standard LB 4 min default are documented; firewall timers vary by
   device and policy, so read the device's TCP idle setting) and no keep-alive was sent in time, the middlebox dropped state.
3. Next packet from the client gets an RST from the firewall or disappears (retransmissions).

Fix: keep-alive interval below the smallest idle timeout on the path, or raise the middlebox timeout.

## Gotchas
- Keep-alives carrying 1 garbage byte are normal for some stacks (Wireshark flags both the 0-byte and 1-byte form).
- A keep-alive answered by RST means the peer has no state (rebooted or timed out).

## Verify
- [ ] After tuning, keep-alives appear at the new interval and the connection survives past the old timeout.
