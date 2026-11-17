---
id: computing-software.firmware-embedded-development.hardware-debugging.oscilloscope-serial-decode
name: oscilloscope-serial-decode
category: computing-software
field: firmware-embedded-development
product: hardware-debugging
tags: [scope-serial-decode, protocol-decode, i2c-trigger, spi-decode, uart-decode, can-decode, oscilloscope, hardware-debugging, firmware-embedded-development]
level: practitioner
status: draft
description: "Use scope serial decode and protocol triggers for I2C/SPI/UART/CAN: thresholds, memory depth, triggering on an address or error frame, and when to use an LA."
sources:
  - https://www.tek.com/en/documents/primer/oscilloscope-basics
  - https://www.keysight.com/us/en/assets/7018-02904/application-notes/5990-5158.pdf
  - https://www.rigolna.com/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Serial decode on the oscilloscope

The scope's advantage over a logic analyser: you see the analog waveform *under* each decoded
bit, so you can tell a protocol bug from a signal-integrity bug.

## Setup checklist
1. Channel assignment: I2C SCL/SDA, SPI SCK/MOSI/MISO/CS, UART TX (and RX), CAN H (or a
   differential probe across H-L, or CAN_RX logic pin).
2. Thresholds per channel at mid-level (1.65 V for 3.3 V logic). Auto threshold misjudges slow I2C
   edges; set it manually.
3. Protocol parameters: SPI CPOL/CPHA, bit order, word size, CS polarity; UART baud, bits, parity,
   idle level; CAN bit rate and sample point.
4. Memory depth: decode only covers what is in acquisition memory. A 1 Mpts scope at 100 MS/s has
   10 ms. Lower the sample rate (still >=4x bit rate) or use segmented memory.

## Protocol triggers
- I2C: trigger on START + address 0x48 + R/W, on NACK, or on a data byte.
- SPI: trigger on CS active + MOSI pattern.
- UART: trigger on a specific byte or parity/framing error.
- CAN: trigger on ID, error frame, or ACK error.
Triggering on errors captures the one bad frame among millions.

## Segmented memory
Each trigger fills a short segment; the scope stores thousands of them with timestamps. Ideal for
bursty buses: capture every transaction to a sensor for an hour without the idle time between.

## Reading the result
- NACK with a clean waveform: firmware problem (address, device busy, wrong sequence).
- Decode errors with a sagging or ringing edge: hardware problem (pull-ups too weak, too much
  capacitance, reflections). Measure rise time against the spec (I2C Fm: 300 ns max).
- Glitch on SCK causing an extra bit in SPI: ground bounce or crosstalk; zoom on the edge.

## When to switch tools
Long captures, more than 4 channels, or analysing thousands of transactions statistically:
logic analyser. Edge quality, analog levels, noise: scope. Often both, cross-triggered.

## Verify
- [ ] Decoded bytes match firmware logs for a known transaction.
- [ ] Error trigger fires on an injected fault (wrong address).
