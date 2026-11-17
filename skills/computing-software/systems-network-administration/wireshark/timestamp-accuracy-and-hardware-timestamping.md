---
id: computing-software.systems-network-administration.wireshark.timestamp-accuracy-and-hardware-timestamping
name: timestamp-accuracy-and-hardware-timestamping
category: computing-software
field: systems-network-administration
product: wireshark
tags: [wireshark, timestamp-accuracy, hardware-timestamping, time-precision, capture-setup]
level: practitioner
status: verified
description: "Understand capture timestamp accuracy (software vs hardware, nanosecond precision, clock sync) and enable hardware timestamps with dumpcap and ethtool."
sources:
  - https://www.wireshark.org/docs/man-pages/dumpcap.html
  - https://www.tcpdump.org/manpages/pcap-tstamp.7.html
  - https://www.kernel.org/doc/html/latest/networking/timestamping.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Timestamp accuracy and hardware timestamping

Software timestamps are taken when the kernel processes a packet: interrupt coalescing, NAPI
polling and CPU load add jitter. Fine for most troubleshooting;
wrong for microburst, latency SLA and trading analysis.

## Check what the NIC supports
```
ethtool -T ens1f0                 # show the device's time stamping capabilities (ethtool(8))
tcpdump -J -i ens1f0              # list timestamp types (tcpdump -J / --list-time-stamp-types)
dumpcap -i ens1f0 --list-time-stamp-types
```
On the Npcap loopback adapter of a Windows host, dumpcap 4.4.1 listed only `host`, `host_hiprec_unsynced`,
`host_lowprec` and `host_hiprec`; the NIC-clock types `adapter` and `adapter_unsynced` depend on the driver.

## Capture with hardware timestamps
```
dumpcap -i ens1f0 --time-stamp-type adapter_unsynced -w hw.pcapng
tcpdump -i ens1f0 -j adapter_unsynced --time-stamp-precision=nano -w hw.pcap
```
- `--time-stamp-precision` is a tcpdump option (`--micro`/`--nano` shorthands); dumpcap 4.4.1 rejects it
  (`unrecognized option: time-stamp-precision`), and a dumpcap file captured with `--time-stamp-type host_hiprec` was
  still written with microsecond precision (`capinfos` reports it).
- `adapter`: per pcap-tstamp(7), a high-precision NIC time stamp synchronised with the host clock (`phc2sys` synchronises two or more
  clocks in the system, `ptp4l` implements IEEE 1588 PTP; linuxptp manual pages).
- `adapter_unsynced`: a high-precision NIC time stamp not synchronised with the host clock, so deltas are accurate but
  absolute time may be off.

## Clock sync across capture points
Correlating two captures needs both clocks synced: PTP (`ptp4l`, `phc2sys`) or NTP; the achievable accuracy depends
on hardware and network. Without sync, align on a shared packet and apply `editcap -t <seconds>` (checked:
`editcap -t 1.5` moved the first packet from epoch 1057.806185 to 1059.306185).

## Verify
- [ ] Back-to-back packets at line rate show inter-arrival deltas consistent with serialisation time (e.g. 1500 B x 8 / 10 Gb/s = 1.2 us, ignoring preamble and inter-frame gap).

## Checked
Run on Windows with Wireshark 4.4.1: `dumpcap --list-time-stamp-types -i <loopback>` printed the four host types;
`dumpcap ... --time-stamp-precision nano` failed with "unrecognized option"; `--time-stamp-type host_hiprec` worked and
`capinfos` showed microseconds; `editcap -t 1.5` shifted epoch times by +1.5 s; 1500 x 8 / 10e9 = 1.2e-6 s computed.
tcpdump `-J`, `-j`, `--time-stamp-precision`, `--micro`, `--nano` and the pcap-tstamp(7) meanings of `adapter` and
`adapter_unsynced` read from the tcpdump.org manual pages. ethtool(8) `-T` and the linuxptp `phc2sys`/`ptp4l` descriptions were read from the Debian manual pages; accuracy figures, VM and capture-card remarks were removed.
