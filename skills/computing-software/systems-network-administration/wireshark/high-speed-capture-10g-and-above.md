---
id: computing-software.systems-network-administration.wireshark.high-speed-capture-10g-and-above
name: high-speed-capture-10g-and-above
category: computing-software
field: systems-network-administration
product: wireshark
tags: [wireshark, high-speed-capture, 10g, packet-loss, af-packet, capture-performance]
level: practitioner
status: docs-checked
description: "Capture at 10/25/100 Gb/s without loss: dumpcap limits, kernel buffers, snaplen, AF_PACKET fanout, PF_RING/DPDK tools, NVMe write speed and verification."
sources:
  - https://www.wireshark.org/docs/man-pages/dumpcap.html
  - https://www.kernel.org/doc/html/latest/networking/packet_mmap.html
  - https://www.ntop.org/products/packet-capture/pf_ring/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Capturing at 10G and above

At high line rates a single general-purpose capture process may drop packets, so plan the capture.

## Budget
10 Gb/s = 1.25 GB/s to disk; 1 minute = 75 GB (arithmetic). Small packets (64 B plus 20 B of preamble and gap = 672 bits on the wire) at line rate = 14.88 Mpps.

## Tuning dumpcap
```
dumpcap -i ens1f0 -B 1024 -s 128 -f "host 10.1.1.5" -w /nvme/cap.pcapng -b filesize:2000000
```
- `-B` sets the capture buffer size in MiB (default 2 MiB); the dumpcap man page says to increase it if you see packet drops, and notes the system or interface may limit what it can set.
- `-s` sets the snapshot length: no more than that many bytes of each packet are read into memory or saved to disk (0 means 262144, the default). A short snaplen suits header-only analysis and reduces disk bandwidth.
- `-f` is a capture filter; keep it as tight as possible.
- `-b filesize:value` switches to the next file after value kB (maximum 2 TB).
- Write to fast storage (NVMe); confirm sustained write speed against the budget above.
- NIC ring size, offload settings and NUMA pinning: see the `ethtool` and `numactl` man pages and your NIC vendor's tuning guide (not covered by this skill's sources).

## Beyond libpcap
| Approach | Source says |
|------|----------|
| AF_PACKET with TPACKET_V3 and fanout | Linux packet_mmap documents TPACKET_V3 and an AF_PACKET fanout mode that load-balances reception among processes |
| PF_RING ZC (ntop) | zero-copy capture on Intel, NVIDIA/Mellanox and FPGA adapters including Napatech and Silicom/Fiberblaze; PF_RING module can read n2disk dump sets |
| Other tools (DPDK-based capture, hardware capture cards) | evaluate from the vendor's own documentation; not covered here |

## Detect loss
- Increase the buffer if dumpcap or the kernel reports drops; the kernel's packet_mmap interface exposes drop statistics (`TP_STATUS_LOSING`, `PACKET_STATISTICS`).
- Check NIC counters with the NIC driver's `ethtool -S` output (names vary by driver).

## Verify
- [ ] A controlled test at expected peak rate shows zero kernel and NIC drops for the capture duration.

## Checked
Date: 2026-11-02. Confirmed against the dumpcap man page (-B MiB and default 2, -s semantics and 262144, -f, -b filesize in kB with 2 TB max), the kernel packet_mmap document (TPACKET_V3, AF_PACKET fanout, TP_STATUS_LOSING, PACKET_STATISTICS) and the ntop PF_RING page (ZC adapters, Napatech, n2disk). Rates are arithmetic. Removed: "a few Gb/s" figure, 10x disk saving, BPF-in-kernel claim, ethtool/taskset/numactl specifics, netsniff-ng, dpdk-pdump, Arkime, Endace, Wireshark lost_segment, dumpcap summary wording.
Method: documentation only; no commands were run.
