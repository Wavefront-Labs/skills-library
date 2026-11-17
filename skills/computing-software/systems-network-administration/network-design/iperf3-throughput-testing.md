---
id: computing-software.systems-network-administration.network-design.iperf3-throughput-testing
name: iperf3-throughput-testing
category: computing-software
field: systems-network-administration
product: network-design
tags: [network-design, network-performance, iperf3, throughput-testing, bandwidth-test, parallel-streams, udp-jitter-test, reverse-mode, bandwidth-delay-product, tcp-window, link-acceptance-test]
level: practitioner
status: docs-checked
description: "Measure real throughput with iperf3: single vs parallel TCP streams, reverse and bidir, UDP loss/jitter at a target rate, windows for high-RTT links, honest reporting."
sources:
  - https://software.es.net/iperf/invoking.html
  - https://fasterdata.es.net/performance-testing/network-troubleshooting-tools/iperf/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Throughput testing with iperf3

## Basics
```
server$ iperf3 -s                         # TCP/UDP 5201
client$ iperf3 -c <server> -t 30          # 30 s TCP upload client->server
client$ iperf3 -c <server> -t 30 -R       # reverse: server->client (download)
client$ iperf3 -c <server> -t 30 --bidir  # both directions at once
client$ iperf3 -c <server> -P 8           # 8 parallel streams
client$ iperf3 -c <server> -J > run.json  # JSON for records
```
Interpretation:
- Single stream much lower than parallel = per-flow limit: window/RTT (BDP), a policer, or ECMP
  /EtherChannel hashing all of it onto one path.
- Retr column (retransmits) > 0 in steady state = loss on path or a policer; correlate with
  interface drops.
- Run each direction separately: asymmetric results reveal duplex/shaping/one-way problems.

## UDP: loss and jitter at a target rate
```
iperf3 -c <server> -u -b 50M -t 30 -l 1200
```
Reports jitter (ms) and lost/total datagrams on the receiver. Use to validate voice/video paths and
policer/shaper rates. UDP without `-b` defaults to 1 Mbit/sec.

## High-latency links (bandwidth-delay product)
BDP = bandwidth x RTT. 1 Gb/s x 80 ms = 10 MB must be in flight to fill the pipe. Use `-w` to set
the socket buffer/window size on the test, and check the OS limits on the test hosts.

## Testing hygiene
- Test hosts must be capable: CPU (before iperf3 3.16 all streams share one thread; from 3.16 each
  `-P` stream gets its own thread), NIC speed, disk not involved.
- Test across the segment under suspicion, then halve the path to localise.
- Don't run iperf across production WAN links at peak without approval: it competes with users.
- Public iperf servers are often busy/limited; use your own endpoints.
- Wi-Fi results vary with position, airtime; run several and report medians.

## Verify
- [ ] Results recorded with direction, streams, duration, RTT and retransmits.
- [ ] Single-stream and multi-stream numbers explained (BDP or per-flow limits).
- [ ] Link acceptance: agreed share of the contracted rate reached with low retransmits.

## Checked
2026-10-28. Confirmed against the iperf3 invoking page and ESnet fasterdata: default server port 5201, `-R`, `--bidir`, `-P`, `-J`, `-u -b` (default 1 Mbit/sec for UDP), `-l`, `-w`, per-stream threads from 3.16. The BDP figure is arithmetic (1 Gb/s x 80 ms = 10 MB). Removed: the 3.7 version gate, the 64 MB buffer example, the Windows auto-tuning check and the 90-95% acceptance figure.
Method: documentation only; no commands were run.
