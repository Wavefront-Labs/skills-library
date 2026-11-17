---
id: computing-software.qa-testing-engineering.performance-testing.network-latency-emulation
name: network-latency-emulation
category: computing-software
field: qa-testing-engineering
product: performance-testing
tags: [latency-emulation, tc-netem, toxiproxy-latency, wan-emulation, bandwidth-limits]
level: practitioner
status: draft
description: "Emulate WAN latency, jitter, packet loss and bandwidth limits in performance tests with tc netem, Toxiproxy and browser throttling, and know what each affects."
sources:
  - https://man7.org/linux/man-pages/man8/tc-netem.8.html
  - https://github.com/Shopify/toxiproxy
  - https://developer.chrome.com/docs/devtools/settings/throttling
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Network latency and bandwidth emulation

**Why:** test labs have sub-millisecond networks. Real users and cross-region dependencies add 20-300 ms RTT, jitter and loss, which changes connection counts, timeouts and chatty-protocol performance.

## Linux tc netem (on the generator or a router)
```bash
# add 80ms delay ±10ms jitter, 0.5% loss on egress
sudo tc qdisc add dev eth0 root netem delay 80ms 10ms distribution normal loss 0.5%
# bandwidth cap (tbf) under netem
sudo tc qdisc add dev eth0 root handle 1: netem delay 80ms
sudo tc qdisc add dev eth0 parent 1: handle 2: tbf rate 10mbit burst 32kbit latency 400ms
tc qdisc show dev eth0
sudo tc qdisc del dev eth0 root      # remove
```
netem shapes **egress**; for ingress use an `ifb` device or shape on both ends.

## Toxiproxy (per dependency)
```bash
toxiproxy-cli create -l 0.0.0.0:15432 -u db:5432 pg
toxiproxy-cli toxic add -t latency -a latency=50 -a jitter=10 pg
toxiproxy-cli toxic add -t bandwidth -a rate=1000 pg    # KB/s
```
Point the app at the proxy to simulate a remote DB or third-party API without touching host networking.

## Browser level
Chrome DevTools / Playwright CDP `Network.emulateNetworkConditions` for front-end tests (e.g. "Slow 4G"). Lighthouse uses simulated throttling by default.

## What changes under latency
- More concurrent connections needed for the same throughput (Little's Law).
- Chatty APIs (N+1 calls) degrade linearly with RTT.
- TLS handshakes and connection setup costs rise: keep-alive and connection pooling matter.
- Timeouts tuned in the lab start firing.

## Gotchas
- Shaping the generator's interface also delays its metrics exports and SSH; use a dedicated interface or shape only the target port (`tc filter` with `u32 match ip dport`).
- netem rules persist until removed: always clean up in teardown.

## Verify
`ping`/`curl -w '%{time_connect}'` through the shaped path shows the configured delay before starting the test.
