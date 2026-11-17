---
id: computing-software.firmware-embedded-development.esp-idf.heap-tracing
name: heap-tracing
category: computing-software
field: firmware-embedded-development
product: esp-idf
tags: [idf-monitor, esp-heap-trace, heap-trace-start, memory-leak-detection, heap-poisoning, heap-tracing-tohost, esp-idf, firmware-embedded-development]
level: advanced
status: docs-checked
description: "Find memory leaks on ESP32 with ESP-IDF heap tracing: standalone leak mode around a suspect operation, host-based tracing, reading the dump, and separating real leaks from caches."
sources:
  - https://github.com/espressif/esp-idf/blob/master/docs/en/api-reference/system/heap_debug.rst
  - https://github.com/espressif/esp-idf/blob/master/components/heap/include/esp_heap_trace.h
  - https://github.com/espressif/esp-idf/blob/master/components/heap/Kconfig
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Heap tracing

## Is there a leak?
Before tracing, confirm: log `heap_caps_get_free_size(MALLOC_CAP_DEFAULT)` and
`heap_caps_get_minimum_free_size(MALLOC_CAP_DEFAULT)` after each repetition of an operation (connect/disconnect,
HTTP request, OTA check). A real leak shows a steady downward trend after the first few
iterations; one-time drops are caches and lazy init.

## Standalone leak tracing
```
CONFIG_HEAP_TRACING_STANDALONE=y
CONFIG_HEAP_TRACING_STACK_DEPTH=4     # caller frames recorded per allocation
```
```c
#include "esp_heap_trace.h"
#define NUM_RECORDS 200
static heap_trace_record_t records[NUM_RECORDS];   /* must be in internal RAM */

void app_main(void)
{
    ESP_ERROR_CHECK(heap_trace_init_standalone(records, NUM_RECORDS));
    do_operation();                                  /* warm-up: fills caches */

    ESP_ERROR_CHECK(heap_trace_start(HEAP_TRACE_LEAKS));
    for (int i = 0; i < 5; i++) do_operation();
    ESP_ERROR_CHECK(heap_trace_stop());
    heap_trace_dump();
}
```
`HEAP_TRACE_LEAKS` keeps only allocations not freed by the time of the dump. Output lists
size, address, memory type, CPU and the call stack, in this format:
```
3 bytes (@ 0x3fcb26f8, Internal) allocated CPU 0 ccount 0x1e7af728 freed
```
An allocation that appears **5 times** (once per iteration) is your leak. Allocations appearing
once are usually lazily created state.

`HEAP_TRACE_ALL` records every malloc/free (needs many records); useful to understand churn.

## Host-based tracing
```
CONFIG_HEAP_TRACING_TOHOST=y
```
Streams events over JTAG via apptrace (see application-level-tracing), so there is no record
limit. Per the heap debugging page: set `CONFIG_APPTRACE_DESTINATION` to JTAG, add the
`espressif/esp_sysview` managed component, enable `CONFIG_ESP_TRACE_LIB_EXTERNAL`, call
`heap_trace_init_tohost()` early and `heap_trace_start()` / `heap_trace_stop()` around the code.
On the host, run GDB with a gdbinit that issues `mon esp sysview start file://<path>.svdat` at
`heap_trace_start` and `mon esp sysview stop` at `heap_trace_stop`, then process the file with
`$IDF_PATH/tools/esp_app_trace/sysviewtrace_proc.py -p -b <app.elf> <file>.svdat`.

## Overhead and accuracy
- Tracing adds per-allocation cost and records consume RAM; it shifts timing.
- If the record buffer fills, later allocations are not recorded; size `NUM_RECORDS` generously.
- If the recorded stack ends inside a generic wrapper, increase `CONFIG_HEAP_TRACING_STACK_DEPTH`
  to see the real caller.

## Corruption is a different tool
Overwrites and double frees: `CONFIG_HEAP_POISONING_COMPREHENSIVE=y` plus
`heap_caps_check_integrity_all(true)` calls narrowing down where corruption first appears.
`CONFIG_HEAP_TASK_TRACKING=y` attributes heap usage to tasks.

## Verify
- [ ] Leak suspect reproduced over N iterations and the repeating record identified with a decoded stack.
- [ ] After the fix, free heap is flat over 1000 iterations.
- [ ] Tracing disabled in release builds.

## Checked
2026-10-26. ESP-IDF master docs, latest release v6.1 (repository head 2026-10-23). Confirmed: heap_trace_init_standalone, heap_trace_start(HEAP_TRACE_LEAKS | HEAP_TRACE_ALL), heap_trace_stop, heap_trace_dump, record buffer must be in internal RAM, CONFIG_HEAP_TRACING_STANDALONE / TOHOST, CONFIG_HEAP_TRACING_STACK_DEPTH, dump line format, host-based setup (APPTRACE_DESTINATION JTAG, esp_sysview component, gdbinit commands, sysviewtrace_proc.py), HEAP_TASK_TRACKING. Wrong: the host-based sequence (`esp sysview start` is issued from a GDB script, not typed separately) and the dump line format (older format shown). Removed unconfirmed claims about "PC decoded by idf.py monitor" and which subsystems create one-off allocations.
Method: documentation only; no commands were run.
