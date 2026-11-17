---
id: computing-software.firmware-embedded-development.device-driver-development.modbus-rtu-framing
name: modbus-rtu-framing
category: computing-software
field: firmware-embedded-development
product: device-driver-development
tags: [modbus-rtu-framing, uart, modbus, crc16-modbus, t3-5-timeout, firmware-embedded-development]
level: practitioner
status: draft
description: "Implement Modbus RTU framing on a UART: 3.5/1.5 character silent intervals with a timer or idle-line/RTO, CRC-16 (0xA001), function codes, and exception responses."
sources:
  - https://www.modbus.org/docs/Modbus_over_serial_line_V1_02.pdf
  - https://www.modbus.org/docs/Modbus_Application_Protocol_V1_1b3.pdf
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Modbus RTU framing

## Frame
`| address (1) | function (1) | data (0..252) | CRC (2, low byte first) |`, max 256 bytes.
Frames are delimited by **silence**: at least 3.5 character times between frames (t3.5); gaps
longer than 1.5 characters (t1.5) inside a frame make it invalid.

Character time = 11 bits (start + 8 data + parity or second stop + stop). At 9600 baud:
11/9600 = 1.146 ms, so t3.5 = 4.01 ms, t1.5 = 1.72 ms. Above 19200 baud the spec fixes
**t3.5 = 1.75 ms and t1.5 = 750 us**.

## Detecting end of frame
- **Receiver timeout hardware** (best): STM32 USART `RTOR`/`RTOEN` counts bit times of idle; 3.5
  characters x 11 bits = 38.5, so set `RTO = 39` and interrupt on `RTOF`.
- **Timer restarted on each byte** (portable): RX ISR stores the byte and restarts a one-shot
  timer for t3.5; timer expiry = frame complete.
- **Idle-line detection** fires after 1 character of idle: too short for strict Modbus; acceptable
  for many masters in practice, but not compliant.

## CRC-16/MODBUS
Poly 0x8005 reflected (0xA001), init 0xFFFF, no final XOR, transmitted **low byte first**.
```c
uint16_t mb_crc(const uint8_t *p, size_t n) {
    uint16_t c = 0xFFFF;
    while (n--) { c ^= *p++; for (int i = 0; i < 8; i++) c = (c & 1) ? (c >> 1) ^ 0xA001 : c >> 1; }
    return c;
}
/* check: CRC over the whole frame including the 2 CRC bytes == 0 */
```
Test vector: `01 03 00 00 00 0A` -> CRC `C5 CD` (bytes on the wire).

## Common function codes
| Code | Function |
|---|---|
| 0x03 | Read Holding Registers (16-bit, big-endian on the wire) |
| 0x04 | Read Input Registers |
| 0x06 | Write Single Register |
| 0x10 | Write Multiple Registers |
| 0x01/0x02/0x05/0x0F | coils and discrete inputs |
Exception response: function | 0x80 plus code (01 illegal function, 02 illegal address, 03
illegal value, 04 device failure). Broadcast address 0: write-only, no response.

## Slave behaviour
- Ignore frames with bad CRC or wrong address silently (no response).
- Respond after the request's t3.5; drive RS-485 DE only while transmitting.
- 32-bit values span two registers with no standard word order: document it (many devices use
  big-endian word order, some swap).
- Libraries: libmodbus (Linux), FreeMODBUS / embedded modbus stacks for MCUs.

## Verify
- [ ] Interoperates with `mbpoll -m rtu -b 9600 -P none -a 1 -r 1 -c 10 /dev/ttyUSB0` and a commercial master.
- [ ] Back-to-back requests with minimum t3.5 gaps are all answered.
