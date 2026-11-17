---
id: computing-software.networking-hardware-and-wireless.f5-big-ip.tcp-profile
name: tcp-profile
category: computing-software
field: networking-hardware-and-wireless
product: f5-big-ip
tags: [networking-hardware-and-wireless, f5-big-ip, tcp-profile, tcp-optimization, idle-timeout]
level: practitioner
status: draft
description: "Tune BIG-IP client-side and server-side TCP profiles (idle timeout, Nagle, buffers, congestion) for WAN and LAN."
sources:
  - https://www.f5.com/pdf/certification/exams/blueprint-tmos-administration.pdf
  - https://techdocs.f5.com/en-us/bigip-15-1-0/big-ip-local-traffic-manager-implementations.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# TCP profiles and tuning

```
tmsh create ltm profile tcp tcp_wan defaults-from tcp-wan-optimized idle-timeout 600
tmsh create ltm profile tcp tcp_lan defaults-from tcp-lan-optimized
tmsh modify ltm virtual vs_web profiles replace-all-with { tcp_wan { context clientside } tcp_lan { context serverside } http clientssl }
tmsh list ltm profile tcp tcp_wan idle-timeout nagle congestion-control
```
- Using two profiles lets the BIG-IP speak WAN-friendly TCP to clients (`tcp-wan-optimized`: larger windows, selective ACK) and LAN-friendly TCP to servers (`tcp-lan-optimized`).
- `idle-timeout` is seconds before an idle flow is purged (default 300). Long-lived apps (databases, SSH via VS) need a larger value, or enable keep-alives (`keep-alive-interval`).
- `nagle`, `proxy-buffer-high/low`, `send-buffer-size` and `receive-window-size` bound memory per connection; huge buffers multiply with the connection count.
- `tcp-progressive` / `tcp-cmetrics-enable` settings cache per-destination metrics; the `ip-tos-to-client` fields mark QoS.
- `time-wait-recycle` and `reset-on-timeout` affect how quickly state clears and whether clients get a RST at idle expiry.
- Gotcha: if the VS uses a `fastL4` profile, TCP profile options do not apply, only the fastL4 idle timeout does.

Verify: `tmsh show ltm profile tcp tcp_wan` for retransmit counts and `tmsh show sys connection cs-server-addr 10.1.10.100` for flows and timeouts; `curl -w "%{time_total}"` before and after change.
