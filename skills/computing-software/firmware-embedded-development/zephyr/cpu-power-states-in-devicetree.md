---
id: computing-software.firmware-embedded-development.zephyr.cpu-power-states-in-devicetree
name: cpu-power-states-in-devicetree
category: computing-software
field: firmware-embedded-development
product: zephyr
tags: [cpu-power-states, zephyr-power-state, min-residency-us, exit-latency-us, pm-policy-residency, zephyr, firmware-embedded-development]
level: advanced
status: docs-checked
description: "Describe SoC sleep states for Zephyr system PM in devicetree: zephyr,power-state nodes, residency and exit latency values, cpu-power-states, and locking states from code."
sources:
  - https://docs.zephyrproject.org/latest/services/pm/system.html
  - https://docs.zephyrproject.org/latest/build/dts/api/bindings/power/zephyr%2Cpower-state.html
  - https://github.com/zephyrproject-rtos/zephyr/blob/main/dts/bindings/power/zephyr%2Cpower-state.yaml
  - https://github.com/zephyrproject-rtos/zephyr/blob/main/include/zephyr/pm/policy.h
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# CPU power states in devicetree

The residency-based PM policy enters the state with the highest power savings for which
`min-residency-us + exit-latency-us` is less than or equal to the idle time the kernel has
scheduled (`time_to_next_scheduled_event >= min_residency_us + exit_latency`). Locks and latency
requests can exclude states. Those values come from devicetree.

```dts
/ {
    cpus {
        cpu0: cpu@0 {
            compatible = "arm,cortex-m4f";
            reg = <0>;
            cpu-power-states = <&stop0 &stop1 &stop2>;
        };
        power-states {
            stop0: state0 {
                compatible = "zephyr,power-state";
                power-state-name = "suspend-to-idle";
                substate-id = <1>;
                min-residency-us = <100>;
                exit-latency-us = <20>;
            };
            stop1: state1 {
                compatible = "zephyr,power-state";
                power-state-name = "suspend-to-idle";
                substate-id = <2>;
                min-residency-us = <500>;
                exit-latency-us = <80>;
            };
            stop2: state2 {
                compatible = "zephyr,power-state";
                power-state-name = "suspend-to-ram";
                min-residency-us = <2000>;
                exit-latency-us = <400>;
            };
        };
    };
};
```
- `power-state-name` (required): `active`, `runtime-idle`, `suspend-to-idle`, `standby`,
  `suspend-to-ram`, `suspend-to-disk`, `soft-off`. `substate-id` is a platform-specific integer.
  The SoC implements `pm_state_set()` to enter the state.
- `cpu-power-states` is a phandle list on the CPU node ("power management states supported by this
  cpu"). The binding also has `zephyr,pm-device-disabled` to stop system-managed device PM from
  suspending devices for a given state.
- Lower states (higher index in `enum pm_state`) offer greater savings and longer wake latencies.

## Choosing numbers
- **exit-latency-us**: worst-case latency to exit the idle state.
- **min-residency-us**: how long residency must last for entry to be worthwhile energy-wise; it
  includes the time to enter the state and is the break-even time compared with the next
  shallowest state. Measure current with a power analyser, or start from the vendor's recommended
  values.

## Locking states from code
```c
#include <zephyr/pm/policy.h>
pm_policy_state_lock_get(PM_STATE_SUSPEND_TO_RAM, PM_ALL_SUBSTATES);   /* e.g. during USB/DMA */
...
pm_policy_state_lock_put(PM_STATE_SUSPEND_TO_RAM, PM_ALL_SUBSTATES);
```
Latency constraints: `pm_policy_latency_request_add(&req, 50 /*us*/)` adds a maximum-latency
requirement (microseconds): the system will not enter a state that would exceed it, until
`pm_policy_latency_request_remove(&req)`.

## Kconfig
```
CONFIG_PM=y
CONFIG_PM_POLICY_DEFAULT=y        # default policy: CPU residency times plus driver/application constraints
```

## Verify
- [ ] `zephyr.dts` lists the intended `cpu-power-states` for cpu0.
- [ ] PM stats (or current measurement) show the deep state used during long idle.
- [ ] Measured wake-up latency stays within the declared `exit-latency-us` (a worst-case value).

## Checked

Checked 2026-10-25 against the Zephyr source (main, post-4.4; latest release v4.4.2): doc/services/pm/system.rst, dts/bindings/power/zephyr,power-state.yaml, dts/bindings/cpu/cpu.yaml, include/zephyr/pm/policy.h and subsys/pm/policy/Kconfig.
Confirmed: the `zephyr,power-state` properties and the `power-state-name` enum; `cpu-power-states` on the CPU binding; the residency expression; `pm_policy_state_lock_get`/`put` with `PM_ALL_SUBSTATES`; `pm_policy_latency_request_add` semantics; `CONFIG_PM_POLICY_DEFAULT`.

Method: documentation only; no commands were run.
