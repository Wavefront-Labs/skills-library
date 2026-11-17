---
id: computing-software.cybersecurity-defensive.palo-alto-pan-os.pan-os-packet-flow-and-capture-troubleshooting
name: pan-os-packet-flow-and-capture-troubleshooting
category: computing-software
field: cybersecurity-defensive
product: palo-alto-pan-os
tags: [packet-flow-debug, pan-os, packet-diag, packet-capture, global-counters, drop-stage, flow-basic]
level: practitioner
status: draft
description: "Troubleshoot PAN-OS traffic with global counters, packet-diag filters and stage captures to find where packets drop."
sources: ["https://docs.paloaltonetworks.com/pan-os/11-1/pan-os-admin/monitoring/take-packet-captures/take-a-custom-packet-capture"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
Goal: find the stage (receive, firewall, transmit, drop) where a flow dies.

Capture on the dataplane:
```
debug dataplane packet-diag clear all
debug dataplane packet-diag set filter index 1 match source 10.1.1.5 destination 198.51.100.7 destination-port 443 protocol 6
debug dataplane packet-diag set filter on
debug dataplane packet-diag set capture stage receive file rx.pcap
debug dataplane packet-diag set capture stage firewall file fw.pcap
debug dataplane packet-diag set capture stage transmit file tx.pcap
debug dataplane packet-diag set capture stage drop file drop.pcap
debug dataplane packet-diag set capture on
```
Reproduce the traffic, then:
```
debug dataplane packet-diag set capture off
debug dataplane packet-diag set filter off
view-pcap filter-pcap drop.pcap
debug dataplane packet-diag clear all
```
Counters with the same filter:
```
show counter global filter packet-filter yes delta yes
```
Drop counters tell you the reason (route lookup failure, policy deny, session setup failure, zone protection, etc.).

Gotchas
- Leaving the filter or capture on after finishing impacts performance and can fill disk.
- The firewall stage capture shows post-NAT packets; compare with receive to see translation.
- Traffic offloaded to hardware may not appear in later captures; use `set session offload no` for troubleshooting only (confirm).

## Verify
You find a specific counter incrementing, for example a policy deny or no route, matching the flow; fix and confirm the counter stops.
