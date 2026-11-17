---
id: computing-software.systems-network-administration.network-design.bufferbloat-and-bandwidth-delay-product
name: bufferbloat-and-bandwidth-delay-product
category: computing-software
field: systems-network-administration
product: network-design
tags: [network-design, network-performance, bufferbloat, congestion, bandwidth-delay-product, latency-under-load, fq-codel, cake, sqm, tcp-window-scaling, long-fat-network, bbr, tcp-window-tuning]
level: advanced
status: verified
description: "Diagnose two classic performance limits: bufferbloat (latency under load, fixed with fq_codel/CAKE shaping) and bandwidth-delay product limits on long fat networks (windows, BBR)."
sources:
  - https://www.bufferbloat.net/projects/bloat/wiki/Introduction/
  - https://datatracker.ietf.org/doc/html/rfc8290
  - https://fasterdata.es.net/host-tuning/
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Bufferbloat and the bandwidth-delay product

## Bufferbloat: latency under load
Oversized buffers at a bottleneck (usually the WAN edge or a home router/modem) fill during
uploads/downloads; every packet then waits behind them. Idle ping 15 ms, during a big upload
400+ ms: video calls freeze, gaming lags, DNS slows, while throughput looks fine.

Test:
```
ping -i 0.2 8.8.8.8            # in one terminal
iperf3 -c <server> -t 30       # load the link (also with -R)
```
or the Waveform/"Bufferbloat test" web tests. A latency increase of tens of milliseconds or more under load is the usual sign (rule of thumb, no standard threshold).

Fix: shape slightly below the bottleneck rate so the queue forms where you control it, with a
smart queue discipline:
```
# Linux edge router, CAKE on egress
tc qdisc replace dev wan0 root cake bandwidth 95mbit diffserv4 nat
# ingress via ifb or let OpenWrt SQM handle both directions
```
- fq_codel (RFC 8290) / CAKE keep queues short and isolate flows. The tc-cake man page lists the `bandwidth`, `diffserv4` and `nat` keywords used above.
- Enterprise routers: shape to the CIR with fair-queue in class-default (see qos-policing-and-shaping).
- Cost: whatever headroom you shave off (95mbit on a 100 Mbit/s link gives up 5%).

## Bandwidth-delay product (BDP)
Max single-flow TCP throughput ~ window / RTT. To fill a path you need window >= bandwidth x RTT (table recomputed in Python):
| Path | BDP |
|---|---|
| 1 Gb/s x 10 ms | 1.25 MB |
| 1 Gb/s x 80 ms (transatlantic) | 10 MB |
| 10 Gb/s x 150 ms | 187 MB |
Symptom: one transfer stuck well below link speed on high-RTT paths; parallel streams go faster
(see iperf3-throughput-testing). In Wireshark, bytes in flight plateau at the window size.

Fixes:
- Window scaling on (default) and large auto-tuning limits: Linux `net.ipv4.tcp_rmem/tcp_wmem`
  max and `net.core.rmem_max/wmem_max` to 64-256 MB on transfer hosts.
- Middleboxes that strip window scaling (old firewalls) cap windows at 64 KB: check the SYN options
  on both sides of the box.
- Congestion control: loss limits a single flow. The Mathis model (rate ~ MSS/RTT x 1.22/sqrt(p)) gives
  about 3.0 Mbit/s at 0.1% loss and 150 ms RTT with a 1460-byte MSS (9.5 Mbit/s at 0.01%), far below any
  fast link; that is for Reno-style loss response, so measure CUBIC and BBR
  (`net.ipv4.tcp_congestion_control=bbr`, needs the module) on your own path.
- Use tools built for it (parallel streams: rclone, GridFTP; or UDP-based transfer).

## Verify
- [ ] Latency under load close to idle latency after shaping (re-run the ping-under-iperf3 test).
- [ ] Single-stream throughput on the long path near the expected BDP-limited value after tuning.
