---
id: computing-software.systems-network-administration.network-design.ethtool-nic-diagnostics
name: ethtool-nic-diagnostics
category: computing-software
field: systems-network-administration
product: network-design
tags: [network-tools, ethtool, linux, nic-statistics, offloads, ring-buffers, link-negotiation]
level: practitioner
status: docs-checked
description: "Diagnose Linux NIC problems with ethtool: link speed/duplex, driver and firmware, error and drop counters, ring buffer and offload settings, and SFP module diagnostics."
sources:
  - https://man7.org/linux/man-pages/man8/ethtool.8.html
  - https://www.kernel.org/doc/html/latest/networking/statistics.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ethtool NIC diagnostics

## Link
```
ethtool eth0
#  Speed: 10000Mb/s  Duplex: Full  Auto-negotiation: on  Link detected: yes
ethtool -s eth0 speed 1000 duplex full autoneg off     # force (match the switch!)
```
Speed lower than expected (1000 on a 10G link, 100 on a gigabit port) = cable/optic or
negotiation problem; check the switch side too.

## Driver and firmware
```
ethtool -i eth0          # driver, version, firmware-version, bus-info
```
Firmware/driver mismatches cause odd drops and link flaps; compare with vendor recommended versions.

## Counters
```
ethtool -S eth0 | grep -Ei 'err|drop|miss|fifo|crc|discard' | grep -v ': 0$'
ip -s -s link show eth0
```
- `rx_crc_errors` (counted inside `rx_errors`): bad frames, usually physical layer (cable, optic).
- `rx_missed_errors`: packets the device dropped for buffer exhaustion, counted separately from
  `rx_dropped` (kernel statistics documentation); suspect a small ring or CPU/IRQ bottleneck.
- `tx_errors`: total transmit problems.
- Driver-specific counters in `ethtool -S` differ per driver; read the driver documentation.
Watch deltas: run twice with `watch -d -n1 'ethtool -S eth0 | grep -E "drop|miss"'`.

## Ring buffers
```
ethtool -g eth0                  # current vs max
ethtool -G eth0 rx 4096 tx 4096  # bigger rings absorb bursts (more memory, slight latency)
```

## Offloads
```
ethtool -k eth0 | grep -E 'segmentation|receive-offload|checksum'
ethtool -K eth0 tso off gso off gro off lro off      # for accurate packet captures or to test offload bugs
```
Offloads are good for performance; disable temporarily for diagnosis (captures showing 64 KB
packets, checksum errors in Wireshark are offload artefacts).

## Optics
```
ethtool -m eth0                  # SFP vendor, part, wavelength, DOM: Tx/Rx power, temperature
```

## Make changes persistent
Settings made with ethtool are runtime settings: persist them through your distribution's
network configuration (NetworkManager, systemd-networkd or udev rules) and check after a reboot.

## Verify
- [ ] Error/drop counters stop increasing under normal load and link speed matches design.

## Checked
2026-10-28. Confirmed against the ethtool(8) man page (`-i`, `-S`, `-g`/`-G`, `-k`/`-K` with tso, gso, gro, lro, `-s` with speed, duplex and autoneg, `-m` module info) and the kernel networking statistics documentation (`rx_errors` includes `rx_crc_errors`; `tx_errors`; `rx_missed_errors` vs `rx_dropped`; `ip -s` and `ethtool -S`). Removed: `rx_symbol_err`, `rx_no_buffer_count`, `tx_timeout` (driver-specific, not in the sources) and the NetworkManager property example.
Method: documentation only; no commands were run.
