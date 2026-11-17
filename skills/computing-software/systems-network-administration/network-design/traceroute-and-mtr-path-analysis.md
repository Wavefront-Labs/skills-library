---
id: computing-software.systems-network-administration.network-design.traceroute-and-mtr-path-analysis
name: traceroute-and-mtr-path-analysis
category: computing-software
field: systems-network-administration
product: network-design
tags: [network-design, network-tools, network-performance, traceroute, tracert, tcptraceroute, mtr, pathping, latency, packet-loss, icmp-rate-limiting, asymmetric-path, paris-traceroute]
level: practitioner
status: docs-checked
description: "Read traceroute and mtr output correctly: how TTL probes work, ICMP/UDP/TCP modes, why mid-path loss is often fake, spotting real loss and latency, and what to send an ISP."
sources:
  - https://www.bitwizard.nl/mtr/
  - https://datatracker.ietf.org/doc/html/rfc1393
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Traceroute and mtr path analysis

## How it works
Probes are sent with TTL 1, 2, 3, ...; each router that expires the TTL returns an ICMP error, revealing itself
(RFC 1393 describes the method: first hop with TTL 1, then TTL 2, and so on). MTR combines traceroute and ping: it sends
a sequence of ICMP echo requests to each hop to measure link quality. Probe type and options differ per tool and
operating system: read your tool's man page for how to select ICMP, UDP or TCP probes.

## mtr usage
Use report mode with a few hundred cycles for a ticket-worthy sample, and a TCP probe to the application port when
ICMP results disagree with application behaviour (see `mtr --help` or the man page for your version's flags).
Columns include loss percentage, packets sent, last, average, best, worst and standard deviation.

## Reading it correctly
- Loss at an intermediate hop that does not continue to later hops is usually not real loss: routers often deprioritise
  generating ICMP replies. Loss that persists to the final hop matters.
- A latency jump that persists to the destination is real; a single slow hop that later hops do not show is usually
  slow replies from that router, not slow forwarding.
- `* * *` hops: the router does not reply or filters; fine if later hops answer.
- The return path may differ (asymmetric routing), so the latency includes a reverse path you cannot see. Run mtr from
  both ends if you can.
- Load balancing across equal-cost paths can make hops alternate between routers.

## Evidence for an ISP ticket
Both directions of mtr (report mode, many cycles, with timestamps and your public IP), a baseline from a good time,
and the specific symptom (loss at the final hop, latency increase).

## Verify
- [ ] Loss/latency conclusion based on the final hop and persistent changes, not mid-path artefacts.
- [ ] A TCP probe used when ICMP or UDP results conflict with application behaviour.

## Checked
2026-10-28. Confirmed in RFC 1393 (TTL-based method with ICMP errors) and the MTR project page (traceroute plus ping,
ICMP echo requests per hop). Removed as unconfirmed: the per-tool default-probe table, mtr flags (`-rwzbc`, `-T -P`),
pathping 100 s figure, tcptraceroute and Paris-traceroute claims, MPLS TTL note. The interpretation bullets are
operational judgement, not sourced figures.
Method: documentation only; no commands were run.
