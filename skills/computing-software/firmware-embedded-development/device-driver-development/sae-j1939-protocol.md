---
id: computing-software.firmware-embedded-development.device-driver-development.sae-j1939-protocol
name: sae-j1939-protocol
category: computing-software
field: firmware-embedded-development
product: device-driver-development
tags: [j1939, can-bus, pgn, address-claim, transport-protocol, firmware-embedded-development]
level: advanced
status: gated
description: "Work with SAE J1939 on 29-bit CAN: decoding priority/PGN/source address, PDU1 vs PDU2, address claiming, BAM/RTS-CTS transport for >8 bytes, and DM1 diagnostics."
sources:
  - https://docs.kernel.org/networking/j1939.html
  - https://github.com/linux-can/can-utils
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# SAE J1939

J1939 is the CAN higher-layer protocol for trucks, buses, agricultural (ISOBUS builds on it),
marine and generators. It uses 29-bit identifiers; bit rates come from the J1939 physical layer
documents (gated: unconfirmed, source is paywalled or blocked).

## Identifier layout
```
bits 28-26  priority
bit  25     reserved (R), bit 24 data page (DP)
bits 23-16  PDU format (PF)
bits 15-8   PDU specific (PS): destination address if PF < 240, group extension if PF >= 240
bits 7-0    source address (SA)
```
```c
uint32_t pgn(uint32_t id) {
    uint32_t pf = (id >> 16) & 0xFF, dp = (id >> 24) & 0x3;
    return (pf < 240) ? (dp << 16) | (pf << 8)                 /* PDU1: PS is a destination, not part of PGN */
                      : (dp << 16) | (pf << 8) | ((id >> 8) & 0xFF);   /* PDU2: broadcast */
}
```
Example: `0x0CF00400` -> priority 3, PGN 61444 (0xF004), SA 0x00. Which parameters a PGN carries and
their scaling (for example engine speed in EEC1) come from J1939-71 and the J1939 Digital Annex (gated: unconfirmed, source is paywalled or blocked).

## Address claiming (J1939-81)
Each ECU is known by a 64-bit NAME. At power-up it sends Address Claimed (PGN 60928, 0xEE00) with its NAME
from the desired SA; on conflict the **lower NAME wins** and the loser picks another address (if
arbitrary-address-capable) or claims 254 (cannot claim). Do not transmit other messages until 250 ms
after a successful claim (gated: unconfirmed, source is paywalled or blocked).

## Transport protocol (J1939-21) for > 8 bytes
The next two bullets (control byte values, packet layout and timing) are from J1939-21 (gated: unconfirmed, source is paywalled or blocked).
- **BAM** (broadcast): TP.CM (PGN 60416, 0xEC00) control byte 32 with size, packet count and the
  wrapped PGN, then TP.DT (PGN 60160, 0xEB00) packets: byte 0 = sequence number 1..n, 7 data
  bytes each, 50-200 ms between packets.
- **RTS/CTS** (destination-specific): RTS (16), receiver replies CTS (17) with how many packets
  to send, end with End of Message Ack (19); Abort (255).
TP carries up to 1785 bytes (the Linux stack switches to ISO 11783 Extended Transport Protocol above
that, up to 111 MiB, unicast only).

## Diagnostics (J1939-73)
DM1 (PGN 65226, 0xFECA): active DTCs with lamp status bytes; each DTC = SPN (19 bits) + FMI (5)
+ occurrence count; multiple DTCs are sent via BAM (gated: unconfirmed, source is paywalled or blocked).

## Tools
Linux kernel `can-j1939` socket family (`socket(PF_CAN, SOCK_DGRAM, CAN_J1939)`) handles TP and ETP
and tracks claimed addresses and NAMEs; can-utils ships `j1939acd` (address claim daemon), `j1939cat`,
`j1939spy` and `j1939sr`; `candump -l` logs frames for offline decoding.

## Verify
- [ ] Decoded PGN/SA for logged frames match the DBC; BAM reassembly yields correct DM1 content.
- [ ] Address conflict test: two ECUs with the same preferred SA resolve per NAME priority.

## Checked

2026-10-27, Linux kernel documentation (mainline v7.3) and can-utils master.
Confirmed in Documentation/networking/j1939.rst: the identifier layout (priority 28..26, reserved 25, DP 24, PF 23..16, PS 15..8, SA 7..0), PDU1 (PF < 240, destination address not part of the PGN) versus PDU2 (PF >= 240, group extension in the PGN), PGN max 0x3ffff, 64-bit NAME, kernel tracking of claimed NAME and address, TP up to 1785 bytes, ETP above that up to 111 MiB, unicast TP needing a receiver, and socket(PF_CAN, SOCK_DGRAM, CAN_J1939). Confirmed in the can-utils file list: j1939acd, j1939cat, j1939spy, j1939sr (no tool named jcat). The example identifier decode and the PGN hex/decimal values were recomputed. Bit rates, priority defaults, parameter scaling, address-claim contention and timing rules, TP control codes and DM1 layout are marked gated because SAE J1939 documents are paywalled. Removed the DBC and SavvyCAN claim and the CSS Electronics tutorial source.

Method: documentation only; no commands were run.
