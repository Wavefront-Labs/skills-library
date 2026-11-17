---
id: computing-software.firmware-embedded-development.hardware-debugging.runtime-deadline-monitoring
name: runtime-deadline-monitoring
category: computing-software
field: firmware-embedded-development
product: hardware-debugging
tags: [deadline-monitoring, deadline-miss, runtime-monitoring, control-loop-timing, overrun-detection, zephyr-timing, hardware-debugging, firmware-embedded-development]
level: advanced
status: docs-checked
description: "Detect missed deadlines in shipping firmware: cycle-counter timestamps, absolute schedules without drift, overrun counters, and Zephyr timing APIs."
sources:
  - https://docs.zephyrproject.org/latest/kernel/services/timing/clocks.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Runtime deadline monitoring

Lab timing measurements prove the design; runtime monitors show the shipped device keeps meeting it
under real inputs and firmware updates. The measurement design below is general practice; the API
facts are from the Zephyr kernel timing page.

## Zephyr timing facts to build on
- `k_cycle_get_32()` and `k_cycle_get_64()` return the fastest cycle counter the OS can present
  (for example a CPU cycle counter), and the read is intended to be very fast. Its frequency is
  `sys_clock_hw_cycles_per_sec()`. On platforms where the system timer frequency can change, that
  function returns a runtime value, so do not assume a fixed frequency.
- Convert with the kernel conversion family, for example `k_cyc_to_us_floor64()`. Units are ms, us,
  tick and cyc, with floor, ceil and near rounding at 32 or 64 bit precision.
- `k_uptime_get()` is milliseconds since boot; `k_uptime_ticks()` gives the 64-bit tick count;
  `k_uptime_delta()` returns elapsed time since a reference and updates the reference.
- A relative timeout scheduled from inside a timeout callback (a `k_timer` expiry function or a
  delayable work handler) is measured from the time the firing timeout was originally scheduled, so
  periodic work can fire at regular intervals without systematic drift. Relative timeouts from
  application context start from `k_uptime_ticks()` at the time the kernel receives them.
- Absolute timeouts exist (`K_TIMEOUT_ABS_MS` and variants for ns, us, cycles and ticks).
- 32-bit timeout values in non-tick units have complicated rollover semantics on long uptimes;
  timing sensitive applications with long uptimes should use the 64-bit timeout type.

## Instrument the periodic job
Timestamp release and completion with the cycle counter, using wrap-safe unsigned subtraction:
- lateness = start - scheduled release (release jitter); keep the maximum;
- execution time = end - start; keep the maximum;
- overrun = execution time above its budget; miss = completion after the next release.
Advance the scheduled time by the period each cycle (an absolute schedule) so lateness does not
accumulate as drift.

## Alarms for deadlines that matter
Arm a timer at release for the deadline and cancel it on completion; if it fires, the deadline was
missed, so enter a safe state and log. A watchdog only catches total hangs.

## Reporting
- Keep counters and maxima in RAM and expose them through a shell command or telemetry; reset the
  maxima only on request.
- Never print from the monitored path; let a background task read the counters.
- Compare execution-time maxima per firmware build to catch regressions after an update.

## Verify
- [ ] A busy-wait longer than the period increments the miss counter and trips the alarm.
- [ ] The monitor's own overhead is measured and small against the job budget.

## Checked
Confirmed from the Zephyr Kernel Timing page: cycle counter and frequency APIs, conversions, uptime
APIs, drift-free relative scheduling from callbacks, absolute timeouts and 64-bit timeout advice.
Removed as unconfirmed: the ISO 26262-related source, the FreeRTOS vTaskDelayUntil source and its
return value claim, the `k_timer_status_get` claim, DWT CYCCNT details, histogram bucket counts and
the overhead figure. The monitoring pattern itself is general practice, not a sourced claim.

Method: docs-checked 2026-11-09 against the Zephyr Kernel Timing documentation page.
