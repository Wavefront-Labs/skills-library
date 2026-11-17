---
id: computing-software.firmware-embedded-development.zephyr.gpio-api-inputs-outputs-interrupts
name: gpio-api-inputs-outputs-interrupts
category: computing-software
field: firmware-embedded-development
product: zephyr
tags: [zephyr-gpio, gpio-pin-configure-dt, gpio-pin-interrupt-configure-dt, gpio-callback, gpio-port-set-masked, zephyr, firmware-embedded-development]
level: practitioner
status: docs-checked
description: "Drive Zephyr GPIOs: configure inputs and outputs, edge and level interrupts with gpio_callback, port-wide masked writes, and wake-capable pins for low power."
sources:
  - https://github.com/zephyrproject-rtos/zephyr/blob/main/include/zephyr/drivers/gpio.h
  - https://github.com/zephyrproject-rtos/zephyr/blob/main/doc/hardware/peripherals/gpio.rst
  - https://github.com/zephyrproject-rtos/zephyr/blob/main/dts/bindings/input/gpio-keys.yaml
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# GPIO API

## Output
```c
#include <zephyr/drivers/gpio.h>
static const struct gpio_dt_spec led = GPIO_DT_SPEC_GET(DT_ALIAS(led0), gpios);

if (!gpio_is_ready_dt(&led)) return -ENODEV;
gpio_pin_configure_dt(&led, GPIO_OUTPUT_INACTIVE);
gpio_pin_set_dt(&led, 1);
gpio_pin_toggle_dt(&led);
```

## Input with interrupt
```c
static const struct gpio_dt_spec btn = GPIO_DT_SPEC_GET(DT_ALIAS(sw0), gpios);
static struct gpio_callback btn_cb;

static void btn_pressed(const struct device *port, struct gpio_callback *cb, gpio_port_pins_t pins)
{
    /* ISR context: no blocking; hand off */
    k_work_reschedule(&debounce_work, K_MSEC(20));
}

int buttons_init(void)
{
    gpio_pin_configure_dt(&btn, GPIO_INPUT);                   /* pull flags come from DT */
    gpio_pin_interrupt_configure_dt(&btn, GPIO_INT_EDGE_TO_ACTIVE);
    gpio_init_callback(&btn_cb, btn_pressed, BIT(btn.pin));
    return gpio_add_callback(btn.port, &btn_cb);
}
```
Interrupt flags:
| Flag | Meaning |
|---|---|
| `GPIO_INT_EDGE_TO_ACTIVE` / `_TO_INACTIVE` / `GPIO_INT_EDGE_BOTH` | logical edges (respect active-low) |
| `GPIO_INT_EDGE_RISING` / `_FALLING` | physical edges |
| `GPIO_INT_LEVEL_ACTIVE` / `_INACTIVE` | logical level; a level interrupt stays asserted while the pin is at that level, so disable or handle it in the callback |
| `GPIO_INT_DISABLE` | off |

One `gpio_callback` can cover several pins on the same port (`BIT(a) | BIT(b)`); check `pins` in
the handler. The callback struct must stay alive (static).

## Reading
`gpio_pin_get_dt(&btn)` returns logical level (1 = active), negative on error.
`gpio_pin_get_raw` returns the physical level.

## Port operations
```c
gpio_port_set_masked(port, 0x0F, 0x05);           /* write 4 pins in one call */
gpio_port_get(port, &val);
```
Use for parallel buses or when several pins must change in one call. These take logical levels (they honour
`GPIO_ACTIVE_LOW`); the `_raw` variants (`gpio_port_set_masked_raw()`, `gpio_port_get_raw()`) use physical levels.

## Low power and wakeup
- Wakeup: `GPIO_INT_WAKEUP` (also in the `GPIO_INT_TRIG_WAKE*` trigger values) requests that the pin trigger a
  system wakeup, where the driver supports it. `gpio_pin_interrupt_configure_dt()` adds `GPIO_INT_WAKEUP` to the
  flags you pass when it is set in the specifier's `dt_flags`.
- Disconnect unused pins: `GPIO_DISCONNECTED` disables a pin for both input and output.
- The GPIO API does not debounce; do it in deferred work, or use the input subsystem's `gpio-keys` binding,
  which has a `debounce-interval-ms` property.

## Gotchas
- Configuring interrupts before `gpio_add_callback` can miss an early edge; add the callback first
  or check state after enabling.

## Verify
- [ ] Pull-ups/downs and polarity defined in DT, not hardcoded.
- [ ] Callbacks do no blocking work; debounce handled in deferred work.

## Checked

Checked 2026-10-26 against `include/zephyr/drivers/gpio.h` and the GPIO and gpio-keys documentation/binding on Zephyr main:
`gpio_pin_configure_dt()`, `gpio_pin_interrupt_configure_dt()`, `gpio_pin_toggle_dt()`, `gpio_init_callback()`,
`gpio_add_callback()`, `gpio_port_set_masked()`, `gpio_port_get()`, `gpio_pin_get_raw()`, the `GPIO_INT_*` flag names and their
logical or physical meaning, `GPIO_INT_WAKEUP` and the `dt_flags` merge, `GPIO_DISCONNECTED`, and `debounce-interval-ms`.
Fixed the port-operation note: `gpio_port_set_masked()` and `gpio_port_get()` are logical, not raw. Removed the `GPIO_INT_DEBOUNCE` flag (not present in `gpio.h`), the DT `wakeup-source` claim and the nRF-specific
edge-emulation note.

Method: documentation only; no commands were run.
