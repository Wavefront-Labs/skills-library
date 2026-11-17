---
id: computing-software.firmware-embedded-development.bare-metal-programming.deferred-binary-logging
name: deferred-binary-logging
category: computing-software
field: firmware-embedded-development
product: bare-metal-programming
tags: [deferred-logging, binary-logging, tokenized-logging, defmt, trice, pigweed-tokenizer, rtt, log-buffer, format-string-stripping, firmware-embedded-development]
level: advanced
status: docs-checked
description: "Log from ISRs and tight loops with deferred, tokenized binary logging: strings replaced by tokens, host-side decoding, and how Pigweed, Trice, defmt and Zephyr do it."
sources:
  - https://pigweed.dev/pw_tokenizer/
  - https://github.com/rokath/trice
  - https://defmt.ferrous-systems.com/
  - https://docs.zephyrproject.org/latest/services/logging/index.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Deferred (binary) logging

**Goal:** logging whose call site is cheap and safe in ISRs, with format strings kept out of
flash and out of the transport.

## Two independent ideas
1. **Deferred**: the call site does only the time-critical part; formatting and sending happen
   later in a known context or on the host. Zephyr: deferred logging reduces the time needed to
   log a message by shifting time-consuming operations to a known context. defmt ("deferred
   formatting"): the single-byte binary value is sent to the host and formatted there.
2. **Tokenized or compressed**: the format string is replaced at build time by a token or index,
   and the host maps it back using a database or the ELF.

## Implementations (from each project's own page)
| Tool | How it works | Decoder |
|---|---|---|
| Pigweed `pw_tokenizer` | printf-style strings replaced by binary tokens during compilation (macro such as `PW_TOKENIZE_STRING`, or `pw_log_tokenized`) | Detokenization API plus a token database |
| Trice | printf-like calls with compact binary records, usable from interrupt handlers; "Bind" keeps numeric IDs out of user code | Trice host tool and ID dictionaries; keep old captures with the matching host tool and dictionaries |
| defmt (Rust) | table of string literals built at compile time; runtime sends indices; transports include defmt-rtt, defmt-itm, defmt-semihosting | defmt-decoder (used by probe-rs) or the `defmt-print` CLI; output must be an ELF |
| Zephyr logging | frontend filters and queues quickly, backends format and send later (UART, RTT, BLE); `CONFIG_LOG_MODE_DEFERRED`, `_IMMEDIATE`, `_MINIMAL` | with `CONFIG_LOG_DICTIONARY_SUPPORT`, `scripts/logging/dictionary/log_parser.py` with the generated `log_dictionary.json` |

## What the pages claim
- Pigweed example: "Battery Voltage: %d mV" is 41 bytes stored and 43 bytes on the wire untokenized
  versus a 4-byte token stored and 6 bytes on the wire (token plus a varint of the value); they report
  over 50% reduction in encoded log contents and also lower CPU use than `snprintf`.
- Trice: log C code in 3 or 7 assembler instructions (under about 16 clocks) per call, in an
  optimised configuration, transmission handled separately. Its advice for interrupts: send raw
  hardware counter stamps and let the host reconstruct wraps and convert units.
- defmt: a single global logger instance, custom linker script required, compile-time level filtering.
- Zephyr: messages go into a circular packet buffer. Without overflow mode the new message is
  dropped if space cannot be allocated; `CONFIG_LOG_MODE_OVERFLOW` instead discards the oldest
  pending messages, which Zephyr notes degrades performance, so size the buffer and enabled logs to limit
  dropping. Backends can be told how many messages were dropped. In an error condition where the scheduler
  cannot be relied on, call `log_panic()` to switch to synchronous processing.

## Design rules
- The dictionary or database only works for the build that produced it (Zephyr states the
  `log_dictionary.json` works only with the same build). Archive it with each release artefact.
- Count and report dropped records; do not let loss be silent.
- Timestamp from a free-running source on the device; Zephyr performs no conversion between
  timestamp sources of different domains.
- Prefer logging integers over pointers to data that may change before it is decoded (a design
  rule of this skill, not stated by the pages).

## Verify
- [ ] The decoder output matches the source format strings for the build that is running.
- [ ] Logging from a fast ISR does not change timing of the time-critical code (measure on target).
- [ ] The dropped-message count is visible in the output.

## Checked
Method: docs-only read of cited pages, 2026-11-08
Confirmed on the Pigweed, Trice, defmt and Zephyr pages: tokenizing and deferred-formatting principles, the byte-count example, Trice cycle claim, defmt transports and limits, Zephyr deferred, overflow and dictionary options and parser.
Removed because the pages do not state them: the hand-rolled ring-buffer code using DWT, the 5 to 10 times bandwidth figure, trice command lines, python module names for pw_tokenizer, and the SEGGER SystemView row.
