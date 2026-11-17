---
id: computing-software.firmware-embedded-development.hardware-debugging.long-streaming-logic-capture
name: long-streaming-logic-capture
category: computing-software
field: firmware-embedded-development
product: hardware-debugging
tags: [streaming-capture, long-capture, intermittent-bug, usb-bandwidth, sigrok-streaming, trigger-and-stop, hardware-debugging, firmware-embedded-development]
level: practitioner
status: docs-checked
description: "Catch rare intermittent bus faults with hours-long logic captures: Saleae looping and trigger modes, DSLogic stream mode, sigrok-cli continuous capture and post-hoc search."
sources:
  - https://support.saleae.com/user-guide/using-logic/capture-modes
  - https://sigrok.org/wiki/Sigrok-cli
  - https://dreamsourcelab.com/product/dslogic-series/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Long streaming captures

**Use when:** a bus error happens once an hour and a single triggered capture keeps missing it.

## Streaming vs buffered
- **Streaming** captures send samples to the PC continuously; length is limited by PC RAM or
  disk and by USB throughput.
- **Buffered** captures fill onboard memory at a high rate for a short window. DSLogic documents
  both: buffer mode for high sample rate, stream mode for long sample duration. Its stream mode is
  limited by USB bandwidth (for the regular models, only 3 channels are supported under a 100 MHz
  sample rate), and the U3Pro models use USB 3.0 for a "super stream" mode with about ten times the
  bandwidth.

## Sample rate
DreamSource recommends a sample rate 10x to 100x the frequency of the signal under test; lower
rates lose pulses (2x gave wrong waveforms and pulse loss, 5x about 1/5 period deviation in their
examples). Raw data rate is sample rate x channels / 8 bytes per second, so pick the lowest rate
that still resolves the fastest edge you care about.

## Capture strategies
1. **Saleae looping mode:** records continuously into a RAM buffer whose size you set; when full,
   old data is discarded and the capture can continue indefinitely. After stopping you can trim,
   keeping the most recent data.
2. **Saleae trigger mode:** keeps recording into a RAM loop (limited by the memory buffer
   setting) until a trigger is found: rising edge, falling edge, high pulse or low pulse on one
   channel, optionally with other channels required high or low. You can set how much data to keep
   before the trigger and how long to record after it. Size the buffer so the PC does not run out
   of memory while waiting. Trigger View can also trigger on a protocol analyzer result, but only
   for analyzers that support the newer frame format.
3. **Firmware error pin:** in every error path (NACK, CRC fail, timeout) toggle a spare GPIO and
   use it as the trigger.
4. **Timed capture + search:** record for the planned duration, then search the decoded results
   (DSLogic's software supports searching and exporting decoder results) or decode a saved capture with sigrok-cli:
   `sigrok-cli -i cap.sr -P i2c:scl=D0:sda=D1 -A i2c` and search the output.
5. **Headless sigrok-cli:** `--continuous` captures until stopped, for example
   `sigrok-cli -d fx2lafw --config samplerate=4m --continuous -o cap.sr`. For very long runs the
   sigrok-cli wiki shows streaming binary output to a pipe or file
   (`--output-format binary ... --continuous`).

## Gotchas
- Sharing a USB hub with other devices can drop samples: plug the analyser in directly.
- RAM-backed captures need enough memory for the whole window.
- A "missing" event can be the threshold: DSLogic documents an adjustable threshold for 1.2 V to
  5.0 V standards, so set it to match the signal level.

## Verify
- [ ] Capture ran for the planned duration with no dropped-data warning.
- [ ] The fault event is found and the preceding traffic is intact.

## Checked
Confirmed: Saleae timer, looping and trigger modes, buffer behaviour, trim, Trigger View and its
frame-format limit (Saleae capture modes page); sigrok-cli `-d`, `--config samplerate`,
`--continuous`, `-i`, `-o`, `-P` and `-A` usage (sigrok-cli wiki); DSLogic buffer vs stream modes,
sample-rate guidance, USB limits and threshold range (DreamSource DSLogic page). Removed as
unconfirmed: the 16 channel at 20 MHz figure, USB 2 throughput numbers, Saleae transition
compression, the glitch filter claim, ground-loop advice, the grep NACK one-liner and the
automation API remark.

Method: docs-checked 2026-11-09 against the Saleae capture modes page, the sigrok-cli wiki page and the DreamSource DSLogic series page, all read in full.
