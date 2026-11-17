---
id: computing-software.networking-hardware-and-wireless.kea.client-classification-overview-and-steps
name: client-classification-overview-and-steps
category: computing-software
field: networking-hardware-and-wireless
product: kea
tags: [networking-hardware-and-wireless, kea, client-classes, classification, known, unknown, drop]
level: practitioner
status: docs-checked
description: "How Kea client classification works: how a packet joins a class, what classes change, and the ordered steps with KNOWN, UNKNOWN and DROP."
sources:
  - https://kea.readthedocs.io/en/latest/arm/classify.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# client classification overview and steps
A packet joins a class implicitly (vendor class option or other built-in condition), through an expression that evaluates true, through static host reservations, shared network or subnet, or via a hook. Classes can drop queries, steer subnet and pool selection, apply lease or rate limits, tune DDNS, define DHCPv4 private (224-254) and code 43 options, assign options, and set TFTP address and boot file for cable modems.

Order of steps:
1. The ALL class is attached.
2. Vendor class options are processed.
3. Classes with expressions, not marked for later evaluation, run in configuration order.
4. A subnet is chosen: the first with no class guard or one matching a packet class (subnet4_select/subnet6_select callouts run).
5. Host reservations are searched. A match adds KNOWN and the reservation classes; no match adds UNKNOWN. In a shared network the reservation classes are assigned after lease allocation.
6. Classes depending on KNOWN or UNKNOWN are evaluated. Because reservations are looked up after subnet selection, UNKNOWN cannot select a subnet or shared network; KNOWN can only if global reservations are used with `early-global-reservations-lookup` true.
7. A packet in class DROP is dropped and logged (it may depend on KNOWN/UNKNOWN since 1.9.8).
8. Pool addresses or prefixes are assigned, then `evaluate-additional-classes` run (pool, subnet, shared network), then options.

## Checked

2026-11-08. Read the Client Classification chapter in full, in particular sections 15.1 and 15.1.1: the ways a packet joins a class, the nine mechanisms, and the ordered classification steps including KNOWN and UNKNOWN timing, early-global-reservations-lookup, DROP and evaluate-additional-classes. The early global lookup step is summarised rather than listed separately. All claims confirmed; nothing removed.

Method: documentation only; no commands were run.
