---
id: computing-software.firmware-embedded-development.hardware-debugging.logic-analyzer-protocol-capture-workflow
name: logic-analyzer-protocol-capture-workflow
category: computing-software
field: firmware-embedded-development
product: hardware-debugging
tags: [logic-analyzer, saleae, sigrok, pulseview, i2c-decode, spi-decode, uart-decode, sample-rate, nyquist, glitch-filter, trigger-setup, ground-loop, probe-loading, bus-decoder, protocol-analyzer, firmware-embedded-development]
level: practitioner
status: draft
description: "Capture and decode I2C/SPI/UART with a logic analyzer: sample-rate vs clock speed, trigger setup for an intermittent bug, and probe-loading effects that corrupt the signal being measured."
sources:
  - https://support.saleae.com/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Logic analyzer protocol capture workflow

**Goal:** capture a real bus transaction cleanly enough to decode it, and
actually catch the one-in-a-thousand intermittent failure instead of filling
the buffer with uneventful idle time.

## Sample rate vs bus clock — the number that's usually wrong
Decoding requires sampling fast enough to resolve the fastest edge, not just
the nominal clock: Nyquist says 2× the clock frequency is the theoretical
floor, but reliable decode in practice wants 10-20× the bus clock to resolve
edge timing and glitches, not just toggle state. A 400kHz I2C bus wants at
least a few MHz of sample rate; sampling at 1MHz "because that's fast" on a
1MHz SPI bus will alias and misdecode. Check the analyzer software's own
decoder requirements — most state a minimum oversampling ratio.

## Trigger setup for an intermittent bug
Capturing continuously and scrolling through minutes of idle bus traffic to
find one glitch wastes the exercise. Use:
- **Edge/pattern triggers** on a specific signal transition (e.g. a NACK bit,
  a specific SPI CS edge) to start capture only around the event of interest.
- **Pre-trigger buffer** (captures some time *before* the trigger fires) so
  you see what led up to the fault, not just the fault itself.
- For a rare intermittent issue, a longer total capture window at the minimum
  adequate sample rate (trading resolution for duration) beats maximum sample
  rate for a short window that misses the event entirely — decide which
  matters more before starting the capture, not after missing it twice.

## Decoding I2C/SPI/UART in software
Nearly every modern logic analyzer tool (Saleae Logic software, PulseView/
sigrok) has built-in protocol decoders that turn raw sampled edges into
labeled transactions (address, R/W bit, ACK/NACK for I2C; byte values aligned
to CS for SPI; framed bytes with parity/framing-error flags for UART) —
decode in software rather than reading raw timing diagrams by eye once a
decoder exists for the protocol; manual bit-counting on a timing diagram is
slow and error-prone by comparison. Confirm decoder settings (bit order,
CPOL/CPHA for SPI, baud rate for UART) match the actual bus configuration, or
the decoder silently produces wrong values that look plausible.

## Probe loading: the analyzer that changes what it measures
Logic analyzer inputs have input capacitance and (for some analyzers)
non-trivial impedance; clipping a probe onto a fast, weakly-driven, or
marginal signal (a long I2C bus already near its capacitance limit, a
high-impedance sensor output) can itself slow edges enough to change bus
behavior — a signal that "fails intermittently" only while being probed, and
works once unplugged, points at loading, not a logic bug. Prefer probing as
close to the source as possible, use the shortest ground lead available (a
long ground wire adds inductance that rings on fast edges and can look like
noise that isn't really on the bus), and cross-check with a scope's higher
bandwidth/lower capacitance input if a logic analyzer capture looks
suspiciously different from expected timing.

## Verify
- [ ] Sample rate is at least ~10× the bus clock, confirmed against the specific decoder's documented minimum.
- [ ] Trigger condition and pre-trigger buffer were tested to actually catch the target event before relying on them for the real intermittent capture.
- [ ] Decoder settings (bit order, polarity, baud) were cross-checked against the known bus configuration, not left at tool defaults.
- [ ] If a captured anomaly only appears while probed, probe loading was ruled out (shorter ground lead, different probe point, or a scope cross-check) before concluding it's a firmware bug.
