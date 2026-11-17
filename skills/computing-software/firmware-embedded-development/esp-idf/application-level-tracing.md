---
id: computing-software.firmware-embedded-development.esp-idf.application-level-tracing
name: application-level-tracing
category: computing-software
field: firmware-embedded-development
product: esp-idf
tags: [idf-monitor, esp-app-trace, apptrace, sysview-tracing, jtag-trace, logging-over-jtag, esp-idf, firmware-embedded-development]
level: advanced
status: docs-checked
description: "Stream high-rate data, logs and SystemView RTOS traces from ESP32 to the host over JTAG with ESP-IDF application level tracing (apptrace) and OpenOCD."
sources:
  - https://github.com/espressif/esp-idf/blob/master/docs/en/api-guides/tracing/transports.rst
  - https://github.com/espressif/esp-idf/blob/master/docs/en/api-guides/tracing/sysview.rst
  - https://github.com/espressif/esp-idf/blob/master/docs/en/api-guides/jtag-debugging/index.rst
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Application level tracing

apptrace moves data from target to host through the JTAG interface at far higher rates than a
UART and with very little CPU time, while the target keeps running. Uses: logging without
disturbing timing, raw sensor/ADC streams, SystemView RTOS traces, and gcov data.

## Enable
In current ESP-IDF (v6.x) apptrace is a transport of the `esp_trace` component:
```
CONFIG_ESP_TRACE_ENABLE=y
CONFIG_ESP_TRACE_LIB_NONE=y
CONFIG_ESP_TRACE_TRANSPORT_APPTRACE=y
CONFIG_APPTRACE_DEST_JTAG=y            # a UART destination also exists
```
JTAG needs a probe (external or built-in USB-JTAG) with OpenOCD running on the host. ESP-IDF v5.x used `CONFIG_APPTRACE_ENABLE` and passed a destination argument (`ESP_APPTRACE_DEST_JTAG`) to the write and flush calls; check the v5.x guide if you are on that release.

## Raw data from the app
```c
#include "esp_app_trace.h"
esp_err_t r = esp_apptrace_write(samples, sizeof(samples),
                                 ESP_APPTRACE_TMO_INFINITE);   /* or a timeout in us */
```
Zero-copy variant: `esp_apptrace_buffer_get(size, tmo)` / `esp_apptrace_buffer_put(ptr, tmo)`.

Host side, in the OpenOCD telnet/GDB console:
```
esp apptrace start file://trace.bin 1 2048 5 0 0
#               outfile          poll_period trace_size stop_tmo wait4halt skip_size
esp apptrace stop
```
With a finite timeout, writes return an error instead of blocking when the host is not reading; use finite timeouts so the app does not stall when no debugger is attached.

## Logs over JTAG
```c
esp_log_set_vprintf(esp_apptrace_vprintf);   /* ESP_LOGx now goes to apptrace */
```
Decode on the host with `$IDF_PATH/tools/esp_app_trace/logtrace_proc.py <trace_file> <elf_file>`
(the function does not fully parse the format string on target, so logging is cheap).

## SystemView RTOS tracing
In v6.x SystemView support is the external `espressif/esp_sysview` managed component: add it to `idf_component.yml` and enable `CONFIG_ESP_TRACE_LIB_EXTERNAL`.
```
esp sysview start file://cpu0.svdat file://cpu1.svdat
esp sysview stop
```
Open the `.svdat` files in SEGGER SystemView. Shows task switches, ISRs, and API calls with timestamps: the tool for "why did this task miss
its deadline". For SystemView 3.60 and later, `esp sysview_mcore start file://trace.SVDat` writes a single multi-core file; earlier SystemView versions need one file per core. ESP-IDF uses its own FreeRTOS event ID mapping, so replace SystemView's `SYSVIEW_FreeRTOS.txt` with the copy under `$IDF_PATH/tools/esp_app_trace` as the guide describes.

## Also via apptrace
- Heap tracing to host, see heap-tracing.
- Gcov coverage dumps through the `espressif/esp_gcov` managed component, either dumped from the application over apptrace or on demand from OpenOCD with `esp gcov` (JTAG only); see that component's README.

## Verify
- [ ] Sustained throughput measured for your data rate (check for dropped data/timeouts).
- [ ] App runs normally with no debugger attached (finite write timeouts).
- [ ] SystemView capture opens with correct task names and timestamps.

## Checked

2026-10-25, against the ESP-IDF documentation source (espressif/esp-idf docs/en, master, v6.1 release period). Confirmed against the v6.x tracing guides: esp_trace plus apptrace Kconfig names, esp_apptrace_write and buffer_get/put signatures, OpenOCD esp apptrace/esp sysview/esp sysview_mcore syntax, esp_apptrace_vprintf with logtrace_proc.py, esp_sysview and esp_gcov components. Wrong for v6.x: CONFIG_APPTRACE_ENABLE, CONFIG_APPTRACE_SV_ENABLE, CONFIG_APPTRACE_GCOV_ENABLE and the destination argument on write/flush (v5.x forms). Removed the unconfirmed sysviewtrace_proc summary command, esp_apptrace_flush call and heap tracing option name.
Method: documentation only; no commands were run.
