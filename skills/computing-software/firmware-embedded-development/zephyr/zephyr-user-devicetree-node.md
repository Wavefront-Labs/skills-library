---
id: computing-software.firmware-embedded-development.zephyr.zephyr-user-devicetree-node
name: zephyr-user-devicetree-node
category: computing-software
field: firmware-embedded-development
product: zephyr
tags: [zephyr-user, dt-path-zephyr-user, app-devicetree-properties, binding-free-properties, zephyr, firmware-embedded-development]
level: practitioner
status: docs-checked
description: "Give an application board-specific GPIOs, ADC channels or values without writing a binding, using the zephyr,user devicetree node and its implicit binding."
sources:
  - https://github.com/zephyrproject-rtos/zephyr/blob/main/doc/build/dts/zephyr-user-node.rst
  - https://github.com/zephyrproject-rtos/zephyr/blob/main/include/zephyr/devicetree.h
  - https://github.com/zephyrproject-rtos/zephyr/blob/main/include/zephyr/drivers/adc.h
  - https://github.com/zephyrproject-rtos/zephyr/blob/main/include/zephyr/drivers/gpio.h
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# The zephyr,user node

Writing a binding for "the GPIO my app toggles" is overkill. The devicetree scripts treat the `/zephyr,user` node as a
special case: it accepts arbitrary properties and infers their types, so application code gets DT macros for them.
The guide says it is meant for sample code and user applications, not for drivers or subsystems in upstream Zephyr.

## Overlay
```dts
/ {
    zephyr,user {
        signal-gpios = <&gpio0 12 GPIO_ACTIVE_HIGH>;
        io-channels  = <&adc 0>, <&adc 3>;
        boot-delay-ms = <250>;
        product-name  = "widget-a";
    };
};
```

## Code
```c
#include <zephyr/devicetree.h>
#include <zephyr/drivers/gpio.h>
#include <zephyr/drivers/adc.h>

#define ZEPHYR_USER DT_PATH(zephyr_user)

static const struct gpio_dt_spec sig = GPIO_DT_SPEC_GET(ZEPHYR_USER, signal_gpios);
/* DT_FOREACH_PROP_ELEM_SEP calls fn(node_id, prop, idx); ADC_DT_SPEC_GET_BY_IDX takes (node_id, idx), so wrap it */
#define ADC_SPEC_BY_IDX(node_id, prop, idx) ADC_DT_SPEC_GET_BY_IDX(node_id, idx)
static const struct adc_dt_spec chans[] = {
    DT_FOREACH_PROP_ELEM_SEP(ZEPHYR_USER, io_channels, ADC_SPEC_BY_IDX, (,))
};
#define BOOT_DELAY DT_PROP(ZEPHYR_USER, boot_delay_ms)
static const char product[] = DT_PROP(ZEPHYR_USER, product_name);
```
Different boards provide different overlays; the app code is unchanged.

## Type inference
Inferred from the value syntax. The guide shows: no value is a boolean, `[81 82 83]` bytes, `<23>` a number,
`<1>, <2>, <3>` a numbers array, `"text"` a string, `"a", "b", "c"` a string array, and a single phandle `<&gpio0>`
a phandle (use `DEVICE_DT_GET(DT_PROP(node, handle))`). Any property whose value contains at least one phandle and a
number (for example `<&adc0 1>`) is inferred as a phandle-array. When inference does not fit or you need
validation/defaults, write a real binding for a proper node.

## Making it optional
```c
#if DT_NODE_HAS_PROP(ZEPHYR_USER, signal_gpios)
   ...
#endif
```
Or `GPIO_DT_SPEC_GET_OR(ZEPHYR_USER, signal_gpios, {0})`, which expands to the given default when the property is missing,
so boards without it still build.

## When not to use it
- A reusable driver or library: give it a proper node with a compatible and a binding.
- Many related settings: a dedicated node keeps things grouped and documented.

## Verify
- [ ] `zephyr.dts` contains the `zephyr,user` node with all properties for each target board.
- [ ] Builds for boards lacking a property still compile (guarded access).

## Checked

Checked 2026-10-26 against the Zephyr `/zephyr,user` guide (doc/build/dts/zephyr-user-node.rst), `devicetree.h`, `adc.h` and `gpio.h`
on main: node purpose and the note that it is not for upstream drivers, inferred types and the phandle-array rule, `DT_PATH(zephyr_user)`,
`DT_PROP`, `DEVICE_DT_GET(DT_PROP(...))`, `GPIO_DT_SPEC_GET`, `GPIO_DT_SPEC_GET_OR`, `DT_FOREACH_PROP_ELEM_SEP`. Removed the `pwms` example line, which no checked source covers. Fixed: `DT_FOREACH_PROP_ELEM_SEP` passes
`(node_id, prop, idx)` to the macro, so `ADC_DT_SPEC_GET_BY_IDX(node_id, idx)` needs a wrapper (the example would not have compiled).

Method: documentation only; no commands were run.
