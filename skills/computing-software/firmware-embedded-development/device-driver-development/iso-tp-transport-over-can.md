---
id: computing-software.firmware-embedded-development.device-driver-development.iso-tp-transport-over-can
name: iso-tp-transport-over-can
category: computing-software
field: firmware-embedded-development
product: device-driver-development
tags: [can-bus, iso-tp, iso-15765-2, single-frame, first-frame, consecutive-frame, flow-control, block-size, stmin, uds, firmware-embedded-development]
level: advanced
status: gated
description: "Implement ISO-TP (ISO 15765-2) segmentation over CAN for messages longer than 8 bytes: SF/FF/CF/FC frames, block size, STmin and timeout handling."
sources:
  - https://docs.kernel.org/networking/iso15765-2.html
  - https://github.com/torvalds/linux/blob/master/net/can/isotp.c
  - https://github.com/torvalds/linux/blob/master/include/uapi/linux/can/isotp.h
  - https://github.com/linux-can/can-utils
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ISO-TP transport over CAN

**Goal:** send and receive messages longer than one CAN frame (up to 4095 bytes, and since ISO 15765-2:2016
up to 4 GB, per the Linux isotp source) over
8-byte CAN frames, as UDS diagnostics and many bootloaders require.

## Frame types (first nibble of byte 0 = PCI type)
| PCI | Frame | Layout (classic CAN) |
|---|---|---|
| 0 | Single Frame | `0L dd dd ...` L = length 1..7 |
| 1 | First Frame | `1L LL dd x6` 12-bit total length |
| 2 | Consecutive Frame | `2N dd x7` N = sequence 1..15, then 0, 1, ... |
| 3 | Flow Control | `3S BS ST` S: 0 continue, 1 wait, 2 overflow |
The frame layouts, flow-control codes and STmin encoding in this table and in the sequence below come from
ISO 15765-2 (gated: unconfirmed, source is paywalled or blocked); Linux confirms the roles of SF, FF, CF, FC, `blocksize` and `stmin`.
Padding unused bytes is required by many OEM specs: make it configurable (Linux: `CAN_ISOTP_TX_PADDING`
and `txpad_content`).

## Sequence
1. Sender: First Frame with total length and first 6 bytes.
2. Receiver: Flow Control `30 BS STmin` within the N_Bs timeout (typically 1000 ms (gated: unconfirmed, source is paywalled or blocked)).
3. Sender: BS consecutive frames (BS = 0 means all remaining without further FC), each at
   least STmin apart. STmin 0x00..0x7F = ms, 0xF1..0xF9 = 100..900 us.
4. Receiver checks the sequence number; a gap aborts the transfer.

## Implementation notes
- Two independent state machines (TX and RX) per address pair; tick them from a timer to
  enforce the N_As/N_Bs/N_Cr timeouts (take the values from the standard or OEM spec).
- **Respect STmin from the receiver**, not your own preference. Sending faster than the
  receiver's STmin is the most common interop failure with ECUs.
- Sender must handle FC.WAIT (re-arm N_Bs) and FC.OVFLW (abort).
- On the receive side, handle a new First Frame that arrives while a reception is in progress as
  the spec or OEM document says.
- Addressing: normal (CAN ID per direction), extended (first data byte is
  target address, so 6 bytes per CF) and mixed (same extra byte for both addresses). Pick per the
  vehicle/OEM spec.
- CAN FD ISO-TP uses a longer single frame with an escape length byte (gated: unconfirmed, source is paywalled or blocked); data length must
  follow the CAN FD DLC table.

## Linux reference implementation
```
modprobe can-isotp
isotpsend -s 7E0 -d 7E8 can0 <<< "22 F1 90"
isotprecv -s 7E0 -d 7E8 -l can0
```
Useful as a known-good peer when developing the MCU side.

## Verify
- [ ] 7-byte (SF), 8-byte (FF+1 CF) and 4095-byte transfers succeed against `isotprecv`.
- [ ] STmin and BS from the peer are honoured (check timestamps in `candump -td`).
- [ ] Dropping one CF produces a clean abort and the next transfer works.

## Checked

2026-10-27, Linux kernel documentation and source (mainline v7.3) and can-utils master.
Confirmed in Documentation/networking/iso15765-2.rst: the SF/FF/FC/CF flow with blocksize and stmin, the normal/extended/mixed addressing formats, PF_CAN SOCK_DGRAM CAN_ISOTP sockets, use on classic CAN and CAN FD. Confirmed in net/can/isotp.c and isotp.h: the 4095 byte limit before ISO 15765-2:2016 and 32-bit FF_DL (4 Gbyte) since, TX/RX padding options with txpad_content, module can-isotp (CONFIG_CAN_ISOTP). Confirmed in can-utils: isotpsend and isotprecv exist with -s, -d, -l and -p options. The PCI byte layouts, flow-control status codes, STmin encoding, timeout values and the FD escape length byte are marked gated because ISO 15765-2 is paywalled. Removed the 1000 ms defaults, the padding byte values, the example CAN IDs and the new-FF rule.

Method: documentation only; no commands were run.
