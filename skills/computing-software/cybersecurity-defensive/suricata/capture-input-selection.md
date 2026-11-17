---
id: computing-software.cybersecurity-defensive.suricata.capture-input-selection
name: capture-input-selection
category: computing-software
field: cybersecurity-defensive
product: suricata
tags: [capture-modes, interface, af-packet-option, nfqueue-option]
level: practitioner
status: docs-checked
description: "Pick a packet source on the Suricata command line: -i, --af-packet, --pcap, --netmap, --pfring, --af-xdp, -q for NFQUEUE, -d divert, --dag and --napatech."
sources: ["https://docs.suricata.io/en/latest/command-line-options.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Selecting the capture source

- `-i <interface>`: best available method; repeatable for several interfaces.
- `--af-packet[=<device>]`: Linux AF_PACKET. Without a device, uses the `af-packet` section.
- `--af-xdp[=<device>]`: Linux AF_XDP, using the `af-xdp` section if no device.
- `--pcap[=<device>]`: libpcap, using the `pcap` section if no device.
- `--netmap[=<device>]`: FreeBSD or Linux.
- `--pfring[=<device>]`, with `--pfring-cluster-id` and `--pfring-cluster-type` (`cluster_round_robin` or `cluster_flow`).
- `-q <queue id>`: inline on an NFQUEUE queue (repeatable).
- `-d <divert-port>`: IPFW divert inline mode.
- `--dag <device>` (for example `dag0:4` selects a stream) and `--napatech`.
- `--simulate-ips`: behave as IPS while in a non-IPS mode.
- `--runmode <runmode>`: workers, autofp or single, overriding YAML.
- `-k all|none`: force or disable all checksum validation.
- `-F <file>`: read a BPF filter from a file.
- `--reject-dev=<device>`: send RST or ICMP errors for `reject` via this device.

## Checked

2026-11-04. Every option above confirmed against the Suricata Command Line Options page.

Method: documentation only; no commands were run.
