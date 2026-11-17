---
id: computing-software.systems-network-administration.coredns.coredns-loop-plugin
name: coredns-loop-plugin
category: computing-software
field: systems-network-administration
product: coredns
tags: [coredns, loop, forwarding-loop, kubernetes, troubleshooting]
level: practitioner
status: docs-checked
description: "Detect simple forwarding loops at startup and fix the usual cause, an upstream that points back at CoreDNS such as a loopback resolv.conf entry."
sources:
  - https://coredns.io/plugins/loop/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: stop CoreDNS from forwarding to itself.

The loop plugin sends a random probe query to itself and counts how many times it sees it. If seen more than twice, CoreDNS assumes a forwarding loop and halts the process. Details:
- The probe is `<random number>.<random number>.zone` with type HINFO, sent only for the first zone in the server block.
- It tries for up to 30 seconds to give CoreDNS time to start. Once a query succeeds, loop disables itself to prevent a query of death.
- Syntax is just `loop`.

Limitations: it finds only simple static loops, present at startup, and only for the HINFO type.

Log line on detection: `plugin/loop: Loop (...) detected for zone "."`. It is fatal because a real loop would consume memory and CPU until the host runs out of memory.

Usual causes: forwarding to a loopback address such as 127.0.0.1, ::1 or 127.0.0.53, including via a resolv.conf that contains one; or an upstream that forwards back to CoreDNS.

Kubernetes: the Pod enters CrashLoopBackOff. A common cause is systemd-resolved placing 127.0.0.53 in the node's resolv.conf. Fixes listed: point kubelet's `resolvConf` at the real resolv.conf, disable the local DNS cache, or (partial fix) replace `forward . /path/to/resolv.conf` with an upstream IP.

## Checked

2026-11-03. Page read: https://coredns.io/plugins/loop/ (the CoreDNS plugin page).

Confirmed: the syntax, options, defaults, limits, metric names and examples stated in this skill.

Removed or corrected: nothing.

Method: documentation only; no commands were run.
