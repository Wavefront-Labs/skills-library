---
id: computing-software.networking-hardware-and-wireless.opnsense.traffic-shaper-pipes-queues
name: traffic-shaper-pipes-queues
category: computing-software
field: networking-hardware-and-wireless
product: opnsense
tags: [traffic-shaping, dummynet, ipfw, pipes, queues]
level: practitioner
status: docs-checked
description: "OPNsense traffic shaper model: ipfw/dummynet pipes, WF2Q+ queues with weights, rules, the kern.hz tunable and the status page."
sources: ["https://docs.opnsense.org/manual/shaping.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Traffic shaper concepts

OPNsense shaping is built from pipes, queues and rules on top of IPFW and dummynet, with a low CPU footprint. Shaping rules are handled independently of firewall rules unless a pipe or queue is assigned directly in a firewall rule. Limits can depend on interface, source and destination IP, direction (in/out) and port numbers, and bandwidth can be shared evenly among all users.

Dummynet first classifies packets with ipfw-style matches and splits them into flows (a single TCP connection, a host, a subnet, a protocol and so on). A flow goes to either a pipe or a queue. A pipe emulates a link with fixed bandwidth, propagation delay, queue size and loss rate, so use pipes for hard limits. A queue implements WF2Q+ (worst-case fair weighted fair queueing) with a weight and a reference pipe; backlogged flows on the same pipe share its bandwidth in proportion to their weights. Weights are not strict priorities: a low-weight flow still receives its fraction even if a high-weight flow is permanently busy. Use queues to decide how flows share a limit.

Dummynet recommends kern.hz of at least 1000. VMs often default lower, so add the tunable in System > Settings > Tunables to improve shaper responsiveness.

Verification: Firewall > Shaper > Status lists pipes, queues and rules with traffic counts since the service last restarted (and the timestamp). Tick Show active flows to see flow details and Show rules to see per-rule ipfw counters, which exposes misconfiguration. Refresh after toggling. Use clear, searchable descriptions on every item. How-tos cover dedicated bandwidth, even sharing, per-user limits, queue prioritisation, guest networks, bufferbloat and control plane traffic.

## Checked

2026-11-03. Confirmed against the OPNsense Traffic Shaping manual page: pipes, queues, rules, IPFW and dummynet, WF2Q+ and weights, kern.hz of at least 1000, the Status page options, and the how-to list. Nothing removed.

Method: documentation only; no commands were run.
