---
id: computing-software.firmware-embedded-development.esp-idf.heap-corruption-detection
name: heap-corruption-detection
category: computing-software
field: firmware-embedded-development
product: esp-idf
tags: [esp-debug, heap-corruption, heap-poisoning, heap-caps-check-integrity, use-after-free, esp-idf, firmware-embedded-development]
level: advanced
status: docs-checked
description: "Find ESP-IDF heap corruption (buffer overruns, use-after-free, double free) with heap poisoning levels, heap_caps_check_integrity calls and bisecting the corrupting code."
sources:
  - https://github.com/espressif/esp-idf/blob/master/docs/en/api-reference/system/heap_debug.rst
  - https://github.com/espressif/esp-idf/blob/master/components/heap/include/esp_heap_caps.h
  - https://github.com/espressif/esp-idf/blob/master/components/heap/Kconfig
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Heap corruption detection

## Symptoms
- `CORRUPT HEAP: Bad head at 0x3ffb...` / `assert failed: multi_heap_free`
- Crashes in `malloc`/`free` or in unrelated code far from the bug.
- `LoadProhibited` with addresses or values like `0xFEFEFEFE` (freed-memory pattern in Comprehensive mode).

## Poisoning levels
```
CONFIG_HEAP_POISONING_DISABLED / _LIGHT / _COMPREHENSIVE
```
- **Light**: head and tail canary bytes on every block; integrity checks fail if they are
  overwritten. Catches overruns.
- **Comprehensive**: also fills freshly allocated memory with `0xCE` and freed memory with
  `0xFE`, and checks both patterns on later allocations and integrity checks. Catches
  use-after-free (reads return 0xFEFEFEFE) and uninitialised use. Substantial runtime cost.
Use comprehensive while hunting, light (or off) in production.

## Narrow it down
Sprinkle integrity checks to bisect where corruption first appears:
```c
#define HEAP_CHECK() assert(heap_caps_check_integrity_all(true))
HEAP_CHECK(); step_a(); HEAP_CHECK(); step_b(); HEAP_CHECK();
```
The first failing check after a passing one brackets the corrupting code. Also check from a
periodic task to catch timing-dependent corruption.

`heap_caps_check_integrity_addr(addr, true)` checks the heap containing an address and returns false if the address belongs to no heap region.

## Find the owner of a smashed block
- With Light or Comprehensive poisoning the error message includes the first corrupt address.
- Heap tracing (`CONFIG_HEAP_TRACING_STANDALONE`, see heap-tracing) shows which call site
  allocated a block when its address is in the records.
- `CONFIG_HEAP_TASK_TRACKING` tracks the task responsible for each allocation.

## Common causes
- `strcpy`/`sprintf` into undersized buffers (use `snprintf`).
- Off-by-one on string NUL (`malloc(strlen(s))`).
- DMA into a heap buffer longer than allocated (SPI RX length > buffer).
- Freed buffer still referenced by a callback or queue item.
- Freeing memory that did not come from the heap (static or stack memory).

## Verify
- [ ] Repro with comprehensive poisoning crashes at (or near) the faulty access.
- [ ] After fix, integrity check in a periodic task stays clean for 24 h.

## Checked
2026-10-26. ESP-IDF master docs, latest release v6.1 (repository head 2026-10-23). Confirmed in the heap debugging page: Basic/Light/Comprehensive levels, head/tail canary bytes, 0xCE (fresh) and 0xFE (freed) patterns, 0xFEFEFEFE crash meaning, heap_caps_check_integrity_all/addr semantics, HEAP_TASK_TRACKING, HEAP_TRACING_STANDALONE, "CORRUPT HEAP" message. Removed unconfirmed claims: 0xcececece as a crash address, canaries checked on free, tracing neighbour-block technique and allocator-mixing remark.
Method: documentation only; no commands were run.
