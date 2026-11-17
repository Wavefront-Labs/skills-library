---
id: computing-software.software-engineering.c.binary-io-and-endianness
name: binary-io-and-endianness
category: computing-software
field: software-engineering
product: c
tags: [c, endianness, byte-order, htonl, fwrite-struct, serialization]
level: advanced
status: docs-checked
description: "Read and write binary data portably with explicit byte order instead of fwrite of structs."
sources: ["https://man7.org/linux/man-pages/man3/byteorder.3.html", "https://man7.org/linux/man-pages/man3/endian.3.html", "https://en.cppreference.com/w/c/99"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Binary io and endianness

Goal: files and packets that read back identically on any CPU.

- Define the format in bytes: field widths, byte order, no padding. Serialise manually: `buf[0] = v >> 24; buf[1] = v >> 16; buf[2] = v >> 8; buf[3] = v;` (big-endian). Deserialise with explicit shifts using unsigned types (cast bytes to `uint32_t` before shifting).
- POSIX `htonl`/`ntohl`/`htons`/`ntohs` (`<arpa/inet.h>`) convert to network (big-endian) order; 64-bit has `htobe64`/`be64toh` (`<endian.h>` on Linux/BSD, non-standard).
- Detect host endianness only if you must: `uint16_t x = 1; *(unsigned char *)&x == 1` means little-endian; better to avoid.
- Never `fwrite(&struct, ...)` for interchange: padding, size of `long`, and byte order vary.
- Floating point: IEEE 754 is typical but not guaranteed by ISO C (check `__STDC_IEC_559__`); transmit as `uint32_t`/`uint64_t` bits via `memcpy`.
- Validate lengths read from files before allocating.

Verify: round-trip test comparing against hexdump of known vectors, and run once on a big-endian target or emulator (for example qemu) if available.

## Checked

- Date: 2026-11-02
- Confirmed in man7: `htonl`/`htons`/`ntohl`/`ntohs` (byteorder(3)); `htobe64`/`be64toh` declared in `<endian.h>` (endian(3)). cppreference C99 page: `__STDC_IEC_559__` indicates IEEE-754 support, so it is optional. The rest is design advice with no numeric or named claims.
Method: documentation only; no commands were run.
