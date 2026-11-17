---
id: computing-software.systems-network-administration.wireshark.tcp-sack-analysis
name: tcp-sack-analysis
category: computing-software
field: systems-network-administration
product: wireshark
tags: [wireshark, tcp-analysis, sack, selective-acknowledgment, tcp-options, packet-loss, middlebox]
level: practitioner
status: verified
description: "Read TCP SACK in captures: SACK-permitted negotiation, SACK blocks in duplicate ACKs, calculating what was lost, and middleboxes that strip or break SACK."
sources:
  - https://www.rfc-editor.org/rfc/rfc2018
  - https://www.wireshark.org/docs/dfref/t/tcp.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# TCP SACK analysis

Selective acknowledgment (RFC 2018) lets the receiver tell the sender exactly which byte ranges
arrived after a gap, so only missing segments are retransmitted.

## Negotiation
Both SYN and SYN/ACK must carry `SACK permitted`:
```
tcp.flags.syn == 1 && tcp.options.sack_perm
tcp.flags.syn == 1 && !tcp.options.sack_perm      # one side does not offer it
```
If only one side offers it, SACK is off for the connection.

## SACK blocks
During loss, duplicate ACKs carry `SLE` (left edge) and `SRE` (right edge) values:
```
Acknowledgment number: 10001
SACK: 11461-17301
```
Meaning: received everything up to 10000 and 11461-17300; bytes 10001-11460 (one 1460-byte segment)
are missing. Wireshark shows relative numbers and sets `tcp.options.sack.dsack` for duplicate SACKs
(D-SACK, RFC 2883: the receiver got something twice, a spurious retransmission).
```
tcp.options.sack_le
tcp.options.sack.count > 1          # multiple holes: burst loss
tcp.options.sack.dsack_le
```
Add a column for `tcp.options.sack_le` and `tcp.options.sack_re` to read loss patterns quickly. All these
filters were run in Wireshark 4.4.1; `tcp.options.sack_perm` is accepted as a filter (its `.present`/`.absent`
subfields are the listed fields). A D-SACK in the test showed as a Dup ACK whose first block lies below the ACK number.

## Interpreting
- One hole, quick retransmit: random loss, recovered efficiently.
- Many holes growing over a window: burst loss (queue overflow, policing).
- D-SACK frequent: retransmission timer too aggressive or reordering, not loss.

## Middlebox problems
- A device that rewrites sequence numbers (randomisation) must also rewrite SACK edges; if it does not, the
  sender sees SACK blocks outside its window and transfers stall. Compare SACK values with sequence numbers on
  both sides of the device (a hypothesis to test, not a named product bug).
- Devices stripping TCP options remove SACK-permitted (and window scaling), cutting throughput.

## Verify
- [ ] SYN/SYN-ACK both show SACK permitted, and during loss the retransmitted segment matches the
  hole in the SACK block.
