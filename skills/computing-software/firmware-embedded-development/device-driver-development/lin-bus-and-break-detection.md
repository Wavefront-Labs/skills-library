---
id: computing-software.firmware-embedded-development.device-driver-development.lin-bus-and-break-detection
name: lin-bus-and-break-detection
category: computing-software
field: firmware-embedded-development
product: device-driver-development
tags: [lin-bus, uart, lin-break, protected-identifier, lin-checksum, firmware-embedded-development]
level: advanced
status: draft
description: "Implement LIN 2.x on a UART: break generation and detection, sync byte, protected identifier parity, classic vs enhanced checksum, and slave response timing."
sources:
  - https://www.iso.org/standard/61222.html
  - https://www.st.com/resource/en/application_note/an1229-lin-bus-introduction-stmicroelectronics.pdf
  - https://www.st.com/resource/en/reference_manual/rm0351-stm32l47xxx-stm32l48xxx-stm32l49xxx-and-stm32l4axxx-advanced-armbased-32bit-mcus-stmicroelectronics.pdf
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# LIN and break detection

LIN (ISO 17987, formerly LIN 2.x) is a single-wire 12 V master/slave bus up to 20 kbit/s used for
body electronics. The MCU side is a UART plus a LIN transceiver (TJA1021, TLE7259).

## Frame
```
| break (>=13 dominant bits) | delimiter | sync 0x55 | PID | data 1..8 | checksum |
  <------------- header (master) ------------------>   <--- response (master or slave) --->
```
- **Break**: at least 13 bit times low. Normal UART framing error detection doesn't distinguish it
  reliably; LIN-capable USARTs have break detection (`LBDL` 10 or 11 bits, `LBDF` flag) and send
  breaks with `SBKRQ`.
- **Sync 0x55**: lets slaves measure the master's bit rate (combine with auto-baud for slaves
  without crystals, LIN allows +-14% slave clock deviation before sync).
- **PID**: 6-bit ID + 2 parity bits:
```c
uint8_t lin_pid(uint8_t id) {
    uint8_t p0 =  ((id >> 0) ^ (id >> 1) ^ (id >> 2) ^ (id >> 4)) & 1;
    uint8_t p1 = ~((id >> 1) ^ (id >> 3) ^ (id >> 4) ^ (id >> 5)) & 1;
    return (uint8_t)((id & 0x3F) | (p0 << 6) | (p1 << 7));
}
```
- **Checksum**: inverted 8-bit sum with carry wrap-around. *Classic* (LIN 1.3) covers data only;
  *enhanced* (LIN 2.x) covers PID + data. IDs 0x3C/0x3D (diagnostics) always use classic.
```c
uint8_t lin_checksum(uint8_t pid, const uint8_t *d, int n, bool enhanced) {
    uint16_t s = enhanced ? pid : 0;
    for (int i = 0; i < n; i++) { s += d[i]; if (s > 0xFF) s -= 0xFF; }
    return (uint8_t)~s;
}
```

## STM32 USART in LIN mode
`CR2.LINEN = 1`, `CR2.LBDL = 1` (11-bit break detection), `CR2.LBDIE`; master sends a break with
`USART_RQR_SBKRQ` then writes 0x55 and the PID. Single-wire transceiver echoes everything sent:
read back each transmitted byte and compare (bit error detection).

## Slave timing
After the PID, a publishing slave must start its response within the response space; the whole
frame must fit in `T_frame_max = 1.4 x T_frame_nominal`. Prepare response data before the header
arrives; look up the PID in the ISR, not in the main loop.

## Higher layers
Schedule tables (master), LDF files describe signals and frames, node configuration and
diagnostics (ISO 17987-3, transport over 0x3C/0x3D). Use a LIN stack for production.

## Verify
- [ ] Bus analyser (PLIN, Vector, or logic analyser LIN decoder) shows correct PID parity and checksum type per ID.
- [ ] Slave responds within the frame time budget at 19.2 kbit/s under full ISR load.
