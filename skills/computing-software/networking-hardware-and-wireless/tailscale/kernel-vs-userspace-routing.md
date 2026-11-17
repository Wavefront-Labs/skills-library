---
id: computing-software.networking-hardware-and-wireless.tailscale.kernel-vs-userspace-routing
name: kernel-vs-userspace-routing
category: computing-software
field: networking-hardware-and-wireless
product: tailscale
tags: [netstack, userspace-networking, kernel-mode]
level: advanced
status: docs-checked
description: "Understand how kernel mode and netstack mode differ for subnet routers and exit nodes."
sources: ["https://tailscale.com/kb/1177"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Kernel vs netstack routing

Goal: pick the right forwarding mode for subnet routers and exit nodes.

**Kernel mode**

- Default on Linux and the first mode Tailscale supported.
- The kernel forwards packets and Tailscale decrypts them; packets are not rewritten.
- TCP streams are end to end through the router, and all IP protocols are supported.

**Userspace (netstack) mode**

- Used when `tailscaled` runs with `--tun=userspace-networking` (typical for a regular non-root user) or on operating systems other than Linux such as FreeBSD, macOS or Windows. On those it is the only way to run subnet routers and exit nodes.
- Uses the gVisor netstack library.
- Tailscale terminates TCP and UDP from the origin peer and makes a new outbound connection to the target, stitching them together.
- ICMP ping is relayed by issuing its own ping to the target, which can add apparent latency. Other ICMP is not relayed.
- Protocols other than TCP and UDP, such as SCTP, are unsupported.

**Performance.** Use kernel mode (Linux) for heavily used routers, where heavy means some combination of users, flows and bandwidth. Userspace is sufficient for few users or low bandwidth.

**Checklist**

1. Linux and busy: kernel mode.
2. Non-Linux or unprivileged: userspace.
3. Need SCTP: kernel mode.

## Checked

Confirmed against Tailscale kb/1177 (Kernel vs. netstack subnet routing and exit nodes), read in full: kernel default on Linux, no packet rewriting, all IP protocols, userspace triggers, gVisor netstack, TCP/UDP termination, ICMP ping relaying, SCTP unsupported, and the performance guidance. Nothing was removed.

Method: docs-checked 2026-11-09 against https://tailscale.com/kb/1177
