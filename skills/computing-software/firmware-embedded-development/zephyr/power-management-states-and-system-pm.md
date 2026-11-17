---
id: computing-software.firmware-embedded-development.zephyr.power-management-states-and-system-pm
name: power-management-states-and-system-pm
category: computing-software
field: firmware-embedded-development
product: zephyr
tags: [zephyr, power-management, system-pm, pm-state, pm-device-runtime, residency, idle-thread, pm-policy, wakeup-source, pm-device-busy, cpu-idle, firmware-embedded-development]
level: advanced
status: docs-checked
description: "Configure Zephyr's system PM: PM states and residency requirements, the default idle policy, device busy marking so sleep doesn't cut off an in-flight transfer, wakeup sources."
sources:
  - https://docs.zephyrproject.org/latest/services/pm/system.html
  - https://docs.zephyrproject.org/latest/services/pm/device.html
  - https://docs.zephyrproject.org/latest/services/pm/device_runtime.html
  - https://github.com/zephyrproject-rtos/zephyr/blob/main/dts/bindings/power/zephyr,power-state.yaml
  - https://github.com/zephyrproject-rtos/zephyr/blob/main/include/zephyr/pm/policy.h
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Zephyr power management states and system PM

**Goal:** let Zephyr's PM subsystem pick sleep depth automatically based on
how long the system is actually idle, instead of hand-coding sleep-entry
logic per board — the Zephyr-native equivalent of the bare-metal tradeoffs in
`computing-software.firmware-embedded-development.low-power-design.clock-gating-and-peripheral-sleep-modes`,
and complements this field's device-PM-hook mention in
`computing-software.firmware-embedded-development.zephyr.driver-model-and-device-api`.

## PM states and residency
`CONFIG_PM` enables the subsystem; boards declare which power states they
support (CPU nodes list them in `cpu-power-states`, each a `zephyr,power-state` node with
`power-state-name` such as `suspend-to-idle`, `standby` or `suspend-to-ram`, plus
`min-residency-us` and `exit-latency-us`). Under the default residency policy the kernel asks
how long it would like to sleep and the system enters the state with the highest power savings
whose minimum residency plus exit latency is less than or equal to the scheduled idle time — conceptually the same "how long until something
needs me" calculation underlying FreeRTOS tickless idle in
`computing-software.firmware-embedded-development.freertos.software-timers-and-tickless-idle`,
but Zephyr formalizes it as pluggable states with declared residency rather
than a single tickless/non-tickless toggle.

## Device busy marking prevents sleep mid-transfer
A driver mid-DMA-transfer or mid-I2C-transaction should call
`pm_device_busy_set(dev)` before the operation and `pm_device_busy_clear(dev)`
after. The PM documentation says a busy device is not suspended by device power management,
because suspending a device in the middle of a hardware transaction (for example a flash write)
may lead to undefined behaviour. For the busy flag to also keep the whole system out of low-power
states, enable `CONFIG_PM_NEED_ALL_DEVICES_IDLE` (it depends on `PM_DEVICE` and `!SMP`); that
option makes the PM subsystem check that no devices are busy before entering a system low-power mode.

## Custom PM policy
The default policy (`CONFIG_PM_POLICY_DEFAULT`, the residency policy) picks a state purely from
timing. `pm_policy_state_lock_get(state, substate_id)` (released with the matching `_put`) lets
software block a state at runtime, and `CONFIG_PM_POLICY_CUSTOM` lets you supply your own policy
(`pm_policy_next_state()`); the first lets application code constrain which states are allowed (e.g.
"never go below Suspend-to-RAM while a firmware update is downloading, even
if timing alone would allow deeper sleep") — reach for this only when the
default timing-based policy genuinely conflicts with a correctness
requirement, not as a default override; the built-in policy already does the
packing-tightest-sleep-into-idle-time calculation correctly for the common
case.

## Wakeup sources
A state is only useful if something can actually wake the system out of it. The PM
documentation says it is the application's responsibility to set up a wake-up event (typically
an interrupt from a SysTick, RTC, counter or GPIO), and not every source is usable in every
power mode, so declare wakeup-capable sources explicitly; a deep sleep state entered with no configured wakeup
source for the event the application actually needs (e.g. a button press)
leaves the device asleep until the next unrelated wake, which looks like a
responsiveness bug rather than a missing wakeup-source declaration.

## `pm_device_runtime` vs system-wide PM
Beyond whole-system sleep, `CONFIG_PM_DEVICE_RUNTIME` lets individual devices
suspend themselves when unused and the rest of the system stays active
(e.g. a sensor powered down between polls while the CPU keeps running other
tasks) — a different, finer-grained lever than system sleep states; the two
compose (a runtime-suspended device plus a deep system sleep state both
contribute to the total current draw) but solve different timescales of
idleness.

## Verify
- [ ] Board's declared PM states and residency values were checked against the datasheet's actual wake-latency numbers, not left at a template default.
- [ ] Every driver performing async hardware operations (DMA, bus transactions) calls `pm_device_busy_set`/`clear` around them, tested by forcing sleep during an in-flight transfer.
- [ ] At least one real wakeup source was tested end to end from the deepest state the application relies on.
- [ ] Measured current during idle periods confirms the expected PM state is actually being entered, not just configured (cross-check against a current profiler, not log output alone).

## Checked

Zephyr v4.4.2 documentation and source (latest release on 2026-10-27), read from the zephyr repository.
Confirmed: CONFIG_PM and the residency policy rule (minimum residency plus exit latency must not exceed the scheduled idle time), `cpu-power-states` on CPU nodes, the `zephyr,power-state` binding (power-state-name values, min-residency-us, exit-latency-us); `pm_device_busy_set`/`pm_device_busy_clear` and the busy-status section of the device PM doc; CONFIG_PM_NEED_ALL_DEVICES_IDLE (depends on PM_DEVICE && !SMP); `pm_policy_state_lock_get(enum pm_state, uint8_t substate_id)`, `pm_policy_next_state()`, CONFIG_PM_POLICY_DEFAULT and CONFIG_PM_POLICY_CUSTOM; CONFIG_PM_DEVICE_RUNTIME; the wake-up responsibility statement.
Wrong or overstated claims fixed: the residency threshold includes exit latency, and the default policy chooses the highest-savings state meeting it; busy marking guards a device from suspension and blocks system low-power entry only when CONFIG_PM_NEED_ALL_DEVICES_IDLE is on.

Method: documentation only; no commands were run.
