---
id: computing-software.firmware-embedded-development.device-driver-development.uart-protocol-framing-and-checksums
name: uart-protocol-framing-and-checksums
category: computing-software
field: firmware-embedded-development
product: device-driver-development
tags: [uart, framing, byte-stuffing, cobs, start-byte, delimiter, length-prefix, crc16, crc8, checksum, parser-state-machine, partial-frame, resync, baud-rate-mismatch, framing-error, firmware-embedded-development]
level: practitioner
status: draft
description: "Design a robust UART packet protocol: framing with delimiters vs length-prefixing, CRC vs checksum choice, a byte-at-a-time parser state machine, and resync after a dropped or corrupted byte."
sources:
  - https://www.slideshare.net/jamesjaringan/cobs-consistent-overhead-byte-stuffing
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# UART protocol framing and checksums

**Goal:** turn a raw UART byte stream — which has no concept of "packet", just
bytes — into reliably delimited, verified frames that resynchronize after noise
or a dropped byte, instead of a parser that locks up after the first bit error.

## Why UART needs an application-layer framing scheme
UART guarantees (approximately) start/stop bit framing of individual bytes, not
message boundaries. A noisy line, a momentarily disconnected cable, or a
receiver that starts listening mid-transmission all produce a byte stream with
no inherent structure — your protocol must define where a message starts,
how long it is, and whether it arrived intact.

## Framing strategies
1. **Delimiter-based** (e.g. a reserved start byte `0x7E`, end byte, or
   newline for text protocols): simple, but needs **byte stuffing** (escaping)
   if the delimiter value can appear in payload data — otherwise payload bytes
   that happen to match the delimiter desync the parser. **COBS** (Consistent
   Overhead Byte Stuffing) is the standard answer: guarantees zero bytes only
   ever appear as the frame delimiter, with bounded, predictable overhead
   (unlike naive escape-byte stuffing, whose worst case doubles frame size).
2. **Length-prefixed**: `[length][payload][checksum]`. No escaping needed, but
   a corrupted length byte makes the parser wait for (or misinterpret) the
   wrong number of following bytes — must pair with a timeout (abandon a
   partial frame if the next expected byte doesn't arrive within N ms) or the
   parser can wait forever after one flipped bit.
3. **Fixed-length**: simplest, only viable when every message is genuinely
   the same size; still needs a start marker to find frame boundaries in a
   stream that might start mid-frame on connect.

## Checksum/CRC choice
- A simple additive checksum or XOR catches many but not all single/double-bit
  errors and misses some common error patterns (e.g. byte reordering, certain
  burst errors) — fine for a low-noise, short-range wired link where
  "good enough" is actually fine.
- **CRC-16** (e.g. CRC-16/CCITT or /MODBUS depending on existing convention)
  catches a much larger class of burst errors with a 2-byte cost; CRC-8 is a
  reasonable middle ground for short frames where 2 bytes of overhead matters.
  Match whatever polynomial/initial-value convention the other end (if not
  your own design) already uses — "CRC-16" alone is not one algorithm, several
  common variants exist and silently disagree on the same input.

## Parser state machine, not blocking reads
Receive one byte at a time (interrupt or DMA-idle-callback driven — see
`computing-software.firmware-embedded-development.stm32.cubemx-hal-project-setup`
for the DMA idle-line pattern) into a state machine: `WAIT_START` →
`READ_LENGTH` → `READ_PAYLOAD` → `READ_CHECKSUM` → validate → dispatch, back to
`WAIT_START`. Never block waiting for a full frame to arrive in one read —
partial frames, inter-byte delays, and USB-serial bridges that can deliver
bytes in odd-sized chunks are normal, not exceptional.

## Resync after corruption
If a frame fails its checksum, discard it and scan forward for the *next*
start marker rather than assuming "length" was correct — a corrupted length
byte otherwise causes the parser to skip the wrong number of bytes and
misinterpret real data as length/checksum of a bogus "next frame", producing a
cascading desync that persists until something resets it. A timeout-based
fallback to `WAIT_START` after inactivity is cheap insurance against a parser
stuck mid-frame forever.

## Verify
- [ ] Payload bytes that happen to equal the delimiter/start value don't desync the parser (tested with fuzzed/adversarial payload content, not just happy-path data).
- [ ] A corrupted byte mid-stream is detected (checksum fails) and the parser resynchronizes on the next valid frame within a bounded number of bytes.
- [ ] A dropped byte (simulate by removing one byte from a captured stream) doesn't permanently wedge the state machine — a timeout returns it to `WAIT_START`.
- [ ] CRC/checksum algorithm and parameters match the other end's implementation exactly, verified against a known test vector.
