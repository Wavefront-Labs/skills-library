---
id: computing-software.firmware-embedded-development.device-driver-development.spi-driver-and-chip-select-timing
name: spi-driver-and-chip-select-timing
category: computing-software
field: firmware-embedded-development
product: device-driver-development
tags: [spi, chip-select, cs, cpol, cpha, spi-mode, clock-polarity, clock-phase, full-duplex, half-duplex, dummy-byte, msb-first, lsb-first, daisy-chain, multi-slave, spi-dma, nss, hardware-cs-glitch, firmware-embedded-development]
level: practitioner
status: draft
description: "Write a portable SPI device driver: picking the right CPOL/CPHA mode from a datasheet timing diagram, correct chip-select assertion timing, multi-slave bus sharing, and DMA transfer pitfalls."
sources:
  - https://www.analog.com/en/analog-dialogue/articles/introduction-to-spi-interface.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# SPI driver and chip-select timing

**Goal:** write an SPI driver that reads a device's registers correctly the
first time, generalizing the datasheet-reading method in
`computing-software.firmware-embedded-development.device-driver-development.i2c-sensor-driver-from-datasheet`
to SPI's different failure modes.

## Reading the timing diagram for SPI mode
SPI has four modes from two bits:
- **CPOL** (clock polarity): idle clock level, 0 (low) or 1 (high).
- **CPHA** (clock phase): data sampled on the first clock edge (0) or second (1)
  after CS asserts.
A datasheet timing diagram shows CS falling, then SCLK, then when MOSI/MISO are
valid relative to each edge — match CPOL/CPHA to where the diagram shows data
sampled, not to a guess. Getting this wrong doesn't error cleanly; it reads
shifted/garbage data that often still "looks plausible" (off-by-one-bit framing
can produce values that are wrong but not obviously so).

## Chip-select assertion and timing
- **CS must be asserted (usually active-low) before the first SCLK edge and
  held through the whole transaction**; deasserting it mid-transaction aborts
  the command on most devices and some require CS to toggle high between
  commands (not stay low across back-to-back transfers) to latch a register
  address.
- **Hardware NSS vs GPIO-controlled CS**: many MCU SPI peripherals have a
  hardware chip-select pin, but it often toggles with timing (relative to the
  last clock edge) that doesn't match what a slow/sensitive device needs, or
  it deasserts between every single hardware "transfer" in ways a multi-byte
  command can't tolerate. Driving CS from a plain GPIO under direct code
  control is more common in practice for exactly this reason — check the
  reference manual's NSS timing against the device's datasheet before trusting
  hardware CS for anything beyond a simple single-byte-per-transaction device.
- A CS line shared incorrectly, or released a few nanoseconds early under DMA
  completion-interrupt latency, is a frequent "works on the bench at low SPI
  clock, fails at full speed" bug — verify CS-to-clock and CS-hold timing on a
  scope at the actual operating clock speed, not just logically.

## Multi-slave bus sharing
Multiple devices can share SCLK/MOSI/MISO with separate CS lines, but only one
device's CS may be asserted at a time (MISO is otherwise driven by two chips at
once). Devices with different maximum SPI clock speeds force the driver to
reclock per-device, not fix a single bus speed for all; don't assume the
fastest device's speed works for the slowest one on the same bus.

## Dummy bytes and read/write framing conventions
Full-duplex SPI shifts a byte out for every byte shifted in; a "read" command
often needs the master to clock out dummy bytes (commonly `0xFF` or `0x00` —
check the datasheet, some devices care) just to receive the response bytes
during what is logically a read-only operation from the caller's perspective.

## DMA transfer pitfalls
SPI DMA needs both TX and RX DMA channels configured for a full-duplex
transaction even if you only care about one direction — the RX FIFO can
overflow/the peripheral can stall if nothing drains RX while TX is DMA-fed. CS
must stay asserted for the DMA transfer's full duration; toggling it from the
completion callback (which fires after the last byte is *queued*, not
necessarily shifted out, on some peripherals) can deassert CS one bit-time
early — check the "transfer complete" vs "last byte transmitted" distinction
for the specific peripheral.

## Verify
- [ ] CPOL/CPHA matches the datasheet's timing diagram, confirmed by reading back a known register (WHO_AM_I-equivalent) correctly.
- [ ] CS assert-to-first-clock and last-clock-to-CS-deassert timing checked on a scope at the real operating SPI clock.
- [ ] Multi-slave bus: each device clocked at or below its own max rate; only one CS active at a time verified.
- [ ] DMA transfers: both directions configured, CS held for the true transfer duration, confirmed at full target clock speed, not just a slow bring-up clock.
