---
id: computing-software.firmware-embedded-development.zephyr.gpio-dt-spec-and-specifiers
name: gpio-dt-spec-and-specifiers
category: computing-software
field: firmware-embedded-development
product: zephyr
tags: [gpio-dt-spec, gpio-dt-spec-get-or, phandle-array, gpio-active-low, specifier-cells, zephyr, firmware-embedded-development]
level: practitioner
status: docs-checked
description: "Describe GPIOs in Zephyr devicetree with phandle-array specifiers and use them via gpio_dt_spec: active-low flags, multiple pins, optional pins, and logical vs physical levels."
sources:
  - https://github.com/zephyrproject-rtos/zephyr/blob/main/include/zephyr/drivers/gpio.h
  - https://github.com/zephyrproject-rtos/zephyr/blob/main/doc/build/dts/phandles.rst
  - https://github.com/zephyrproject-rtos/zephyr/blob/main/doc/hardware/peripherals/gpio.rst
  - https://github.com/zephyrproject-rtos/zephyr/blob/main/include/zephyr/dt-bindings/gpio/gpio.h
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# gpio_dt_spec and specifiers

## Devicetree side
```dts
/ {
    leds {
        compatible = "gpio-leds";
        status_led: led_0 {
            gpios = <&gpio0 13 GPIO_ACTIVE_LOW>;   /* controller, pin, flags */
        };
    };
    my_device {
        compatible = "acme,widget";
        reset-gpios = <&gpio1 4 GPIO_ACTIVE_LOW>;
        irq-gpios   = <&gpio1 5 (GPIO_ACTIVE_HIGH | GPIO_PULL_DOWN)>;
    };
};
```
`gpios` is a **phandle-array**: each entry is `<&controller cell...>`, and the number/meaning of
cells comes from the controller's `#gpio-cells` (`pin`, `flags` by the usual convention; the Zephyr devicetree
guide describes `<&gpioX pin flags>`). Property names ending in `-gpios` are the convention, and `flags` is a bit
mask such as `(GPIO_ACTIVE_LOW | GPIO_PULL_UP)` from `dt-bindings/gpio/gpio.h`.

## C side
```c
#include <zephyr/drivers/gpio.h>

static const struct gpio_dt_spec led = GPIO_DT_SPEC_GET(DT_NODELABEL(status_led), gpios);
static const struct gpio_dt_spec rst = GPIO_DT_SPEC_GET(DT_PATH(my_device), reset_gpios);
/* optional pin: zeroed spec if property missing */
static const struct gpio_dt_spec en  = GPIO_DT_SPEC_GET_OR(DT_PATH(my_device), enable_gpios, {0});
/* second entry of a multi-pin property */
static const struct gpio_dt_spec d1  = GPIO_DT_SPEC_GET_BY_IDX(DT_PATH(my_device), data_gpios, 1);

int init(void) {
    if (!gpio_is_ready_dt(&led)) return -ENODEV;
    gpio_pin_configure_dt(&led, GPIO_OUTPUT_INACTIVE);
    gpio_pin_set_dt(&led, 1);        /* logical 1 = active = LOW on the wire here */
    if (en.port) gpio_pin_configure_dt(&en, GPIO_OUTPUT_ACTIVE);
    return 0;
}
```
`gpio_pin_configure_dt()` configures with `spec->dt_flags | extra_flags`, so the DT flags (active-low, pulls) are
merged with the flags you pass. `gpio_pin_interrupt_configure_dt()` only merges the `GPIO_INT_WAKEUP` flag from `dt_flags`.

## Logical vs physical
- `gpio_pin_set_dt(spec, 1)` sets the **logical** active state, honouring `GPIO_ACTIVE_LOW`.
- `gpio_pin_set_raw(port, pin, 1)` drives the physical level, ignoring polarity.
- Configure with `GPIO_OUTPUT_ACTIVE`/`GPIO_OUTPUT_INACTIVE` (logical), not `GPIO_OUTPUT_HIGH/LOW`
  (physical), so board polarity lives in DT only.

## Gotchas
- Property name in C uses underscores: `reset-gpios` -> `reset_gpios`.
- A driver binding must declare the property (`type: phandle-array`) or no macros are generated.
- Pin numbers are per-controller (port-relative), not global SoC pin numbers.
- Leaving pull flags out of DT and adding them in code works but splits the hardware description;
  keep pulls in DT.

## Verify
- [ ] Polarity only in DT; code uses logical levels throughout.
- [ ] Optional pins guarded with `GPIO_DT_SPEC_GET_OR` and a `.port` check.
- [ ] Scope/LED confirms active state on a board with active-low wiring.

## Checked

Checked 2026-10-26 against `include/zephyr/drivers/gpio.h`, `include/zephyr/dt-bindings/gpio/gpio.h`, the devicetree
phandle guide and the GPIO controller binding on Zephyr main: `GPIO_DT_SPEC_GET`, `_GET_OR`, `_GET_BY_IDX`,
`gpio_is_ready_dt()`, `gpio_pin_set_dt()`, `gpio_pin_set_raw()`, `GPIO_OUTPUT_ACTIVE`/`INACTIVE`, how `gpio_pin_configure_dt()`
merges `dt_flags`, `#gpio-cells`, the `<&gpioX pin flags>` form and pull/active flags in devicetree, and the phandle-array
property type. Removed the nRF pin-number example. The statement that a binding must declare the property for macros to
exist follows from the devicetree phandle-array guide.

Method: documentation only; no commands were run.
