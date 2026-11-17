---
id: computing-software.firmware-embedded-development.device-driver-development.canopen-basics
name: canopen-basics
category: computing-software
field: firmware-embedded-development
product: device-driver-development
tags: [canopen, can-bus, object-dictionary, sdo-pdo, nmt-heartbeat, firmware-embedded-development]
level: advanced
status: draft
description: "Implement or integrate a CANopen node (CiA 301): COB-IDs, object dictionary and EDS, NMT state machine, heartbeat, SDO expedited/segmented transfers, PDO mapping."
sources:
  - https://www.can-cia.org/can-knowledge/canopen/
  - https://github.com/CANopenNode/CANopenNode
  - https://www.can-cia.org/groups/specifications/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# CANopen

CANopen (CiA 301) defines how nodes are addressed, configured and exchange process data on
classical CAN. Used in industrial automation, motion control (CiA 402 drives), medical and marine.

## Predefined connection set (11-bit COB-IDs, node ID 1-127)
| Object | COB-ID |
|---|---|
| NMT command | 0x000 |
| SYNC | 0x080 |
| EMCY | 0x080 + node |
| TPDO1..4 | 0x180 / 0x280 / 0x380 / 0x480 + node |
| RPDO1..4 | 0x200 / 0x300 / 0x400 / 0x500 + node |
| SDO server TX / RX | 0x580 / 0x600 + node |
| Heartbeat / boot-up | 0x700 + node |

## Object dictionary (OD)
Every parameter lives at index:subindex. Key entries: 0x1000 device type, 0x1001 error register,
0x1017 producer heartbeat time (ms), 0x1018 identity (vendor ID, product code, revision, serial),
0x1400-0x15FF RPDO comm/mapping, 0x1800-0x1BFF TPDO comm/mapping, 0x6000+ device profile area.
The OD is described in an **EDS** file (INI format) or XDD (XML) that configuration tools read.
Generate both the C OD and EDS from one source (CANopenEditor for CANopenNode).

## NMT state machine
Initialisation -> (boot-up message 0x700+id, data 0x00) -> **Pre-operational** (SDO allowed, no
PDO) -> **Operational** (PDOs active) / **Stopped**. NMT master commands: `01` start, `02` stop,
`80` pre-op, `81` reset node, `82` reset communication; byte 2 = node ID (0 = all).

## SDO
Confirmed access to any OD entry. Expedited (<= 4 bytes in one frame):
`0x600+id: 40 18 10 02 00 00 00 00` = upload (read) 0x1018 sub 2 -> response
`43 18 10 02 xx xx xx xx`. Segmented and block transfers for larger data (firmware download via
0x1F50). Abort codes (e.g. 0x06020000 object does not exist, 0x06090011 subindex does not exist).

## PDO
Unconfirmed, up to 8 bytes, mapping configured in OD (each mapping entry = index, subindex, bit
length). Transmission type: 0xFF/0xFE event-driven (with inhibit and event timer), 1-240 = every
N SYNC. Mapping changes follow a sequence: disable PDO (COB-ID bit 31), set mapping count 0,
write entries, set count, re-enable.

## Implementation
Use a stack: CANopenNode (open source, Apache-2.0), CANfestival, or commercial stacks. Port by
providing the CAN driver (send, receive callback, filters for your COB-IDs), a 1 ms timer
process call, and non-volatile storage for OD parameters (0x1010 store/0x1011 restore).

## Verify
- [ ] Node sends boot-up then heartbeat at the 0x1017 period.
- [ ] `cansend can0 600#4018100200000000` (from Linux SocketCAN) returns the vendor ID; mapping changes take effect.
- [ ] Conformance test (CiA CANopen conformance tool) passes before certification.
