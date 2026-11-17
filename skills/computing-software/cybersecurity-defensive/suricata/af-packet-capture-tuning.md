---
id: computing-software.cybersecurity-defensive.suricata.af-packet-capture-tuning
name: af-packet-capture-tuning
category: computing-software
field: cybersecurity-defensive
product: suricata
tags: [af-packet, ring-size, tpacket-v3, cluster-type]
level: practitioner
status: docs-checked
description: "Configure AF_PACKET capture: interface, cluster-id, cluster-type, tpacket-v3 versus v2, ring-size memory sizing, hardware timestamps."
sources: ["https://docs.suricata.io/en/latest/capture-hardware/af-packet.html", "https://docs.suricata.io/en/latest/performance/tuning-considerations.html", "https://docs.suricata.io/en/latest/performance/packet-capture.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# AF_PACKET

Linux capture default. Sample: `interface: eth0`, `cluster-id: 99`, `cluster-type: cluster_flow`.

- `cluster_flow` hashes the 5-tuple symmetrically so both directions reach one thread.
- `cluster_qm` can bind Suricata to RSS queues when RSS is symmetric.
- `tpacket-v3: yes` is recommended for IDS/NSM; tpacket-v2 for IPS.
- `ring-size` is per thread: memory is threads x ring-size x (default-packet-size + roughly 750 bytes). Rising drop counters in stats mean buffers are filling.
- `enable-hwtimestamp` (default off) can desynchronise NIC and kernel clocks.
- Review with `suricata --dump-config | grep af-packet`.

Sizing also applies to `max-pending-packets`: suggested minimum 10000, roughly 65000 max, per thread.

## Checked

2026-11-04. Confirmed against the AF_PACKET page (enable-hwtimestamp, sample `cluster-id: 99`, `cluster-type: cluster_flow`), Tuning Considerations (tpacket-v3/v2 advice, ring-size, memory formula, max-pending-packets) and Packet Capture (symmetric cluster_flow hash, cluster_qm with symmetric RSS).

Method: documentation only; no commands were run.
