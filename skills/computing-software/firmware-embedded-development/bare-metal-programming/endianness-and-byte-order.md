---
id: computing-software.firmware-embedded-development.bare-metal-programming.endianness-and-byte-order
name: endianness-and-byte-order
category: computing-software
field: firmware-embedded-development
product: bare-metal-programming
tags: [endian-conversion, embedded-c-coding-standard, byte-order, rev-instruction, big-endian-sensor, firmware-embedded-development]
level: practitioner
status: docs-checked
description: "Convert between little-endian Cortex-M and big-endian sensors, network protocols and file formats using shifts, __REV/__builtin_bswap, and clear naming of wire byte order."
sources:
  - https://gcc.gnu.org/onlinedocs/gcc-14.2.0/gcc/Other-Builtins.html
  - https://arm-software.github.io/CMSIS_6/latest/Core/group__intrinsic__CPU__gr.html
  - https://gcc.gnu.org/onlinedocs/gcc-14.2.0/cpp/Common-Predefined-Macros.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Endianness and byte-order serialisation

Most Cortex-M MCUs run little-endian. Sensors, network protocols and file formats each fix their
own byte order, and the datasheet or protocol spec decides: never assume a global rule.

## Portable: shifts (endianness-independent code)
```c
/* sensor sends temperature as MSB, LSB */
int16_t raw = (int16_t)(((uint16_t)buf[0] << 8) | buf[1]);
/* 24-bit signed (MSB first), sign-extend */
int32_t v = (int32_t)(((uint32_t)buf[0] << 24) | ((uint32_t)buf[1] << 16) | ((uint32_t)buf[2] << 8)) >> 8;
```
This code is correct on any host because it describes the *wire* order, not the CPU order.
Cast to an unsigned type before shifting so the shift is done on unsigned values.

## Fast: byte-swap intrinsics
```c
uint32_t be = __builtin_bswap32(le);       /* GCC built-in, 32-bit byte swap */
uint16_t s  = __builtin_bswap16(x);        /* 16-bit byte swap */
uint32_t r  = __REV(x); int16_t h = __REVSH(x);   /* CMSIS intrinsics */
```
GCC documents `__builtin_bswap16/32/64` (and 128 where 128-bit types exist); CMSIS-Core provides
`__REV`, `__REV16`, `__REVSH` and `__RBIT`. Use `memcpy` to load unaligned data:
`uint32_t w; memcpy(&w, p, 4); w = __builtin_bswap32(w);`.

## Naming and APIs
- Name conversion helpers by wire order: `get_be16`, `put_le32`. Document byte order in every
  protocol struct comment or register-map table.
- GCC predefines `__BYTE_ORDER__` and `__ORDER_LITTLE_ENDIAN__`, so
  `#if __BYTE_ORDER__ == __ORDER_LITTLE_ENDIAN__` (or a static assert) can guard assumptions.

## Common traps
- **Multi-byte register addresses and auto-increment order**: the part's datasheet decides
  whether the low or high byte comes first; manual buffers often get it backwards.
- **Floats on the wire**: `memcpy` into `uint32_t`, swap, `memcpy` into `float`; never cast pointers.
- **Bit order within bytes** (LSB-first peripherals) is a separate issue from byte order; `__RBIT`
  reverses the bits of a word.

## Verify
- [ ] Unit test with a known frame from the datasheet example decodes correctly.
- [ ] Swap helpers produce the expected bytes on a known value.

## Checked
2026-10-31. Confirmed in the GCC 14.2 manual: `__builtin_bswap16/32/64/128`; in the CMSIS-Core 6
page: `__REV`, `__REV16`, `__REVSH`, `__RBIT`; in the GCC preprocessor manual: `__BYTE_ORDER__`,
`__ORDER_LITTLE_ENDIAN__`.
Removed: BE8 and per-protocol endianness claims (USB, BLE, CAN-open, network order), ST MEMS and EEPROM examples,
`I2C_MEMADD_SIZE_16BIT`, `SPI_CR1.LSBFIRST`, lwIP `lwip_htons`, the claim that swaps compile to REV/REV16, the
undefined-behaviour assertion about shifting, the example temperature value.
Method: documentation only; no commands were run.
