---
id: computing-software.firmware-embedded-development.device-driver-development.linux-input-subsystem-driver
name: linux-input-subsystem-driver
category: computing-software
field: firmware-embedded-development
product: device-driver-development
tags: [input-driver, linux-driver-subsystem, input-event, evdev, gpio-keys, touchscreen-driver, firmware-embedded-development]
level: advanced
status: docs-checked
description: "Write a Linux input driver for buttons, encoders or touch controllers: input_allocate_device, capabilities, input_report_* + input_sync, multitouch slots, and testing with evtest."
sources:
  - https://docs.kernel.org/input/input-programming.html
  - https://docs.kernel.org/input/multi-touch-protocol.html
  - https://github.com/torvalds/linux/blob/master/Documentation/devicetree/bindings/input/gpio-keys.yaml
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Input subsystem drivers

## First check existing generic drivers
- GPIO buttons: `gpio-keys` (interrupt) / `gpio-keys-polled` with DT only.
- Rotary encoders: `rotary-encoder`; matrix keypads: `gpio-matrix-keypad`.
- ADC ladder buttons: `adc-keys`.
- Common touch controllers (Goodix, FocalTech `edt-ft5x06`) already have drivers.
```dts
gpio-keys {
    compatible = "gpio-keys";
    button-power { label = "Power"; linux,code = <KEY_POWER>; gpios = <&gpio1 5 GPIO_ACTIVE_LOW>; wakeup-source; debounce-interval = <20>; };
};
```

## Custom driver (e.g. I2C button/encoder controller)
```c
struct input_dev *in = devm_input_allocate_device(&client->dev);
in->name = "acme-keys";
in->id.bustype = BUS_I2C;
input_set_capability(in, EV_KEY, KEY_VOLUMEUP);
input_set_capability(in, EV_KEY, KEY_VOLUMEDOWN);
input_set_capability(in, EV_REL, REL_WHEEL);
ret = input_register_device(in);

static irqreturn_t acme_irq(int irq, void *p) {     /* threaded IRQ: I2C reads may sleep */
    struct acme *a = p;
    u8 st = i2c_smbus_read_byte_data(a->client, REG_STATUS);
    input_report_key(a->in, KEY_VOLUMEUP, st & BIT(0));
    input_report_rel(a->in, REL_WHEEL, (s8)i2c_smbus_read_byte_data(a->client, REG_DELTA));
    input_sync(a->in);                              /* EV_SYN: one consistent report */
    return IRQ_HANDLED;
}
devm_request_threaded_irq(dev, client->irq, NULL, acme_irq, IRQF_ONESHOT, "acme", a);
```
Report key state (1 pressed / 0 released); the input core drops duplicate states and generates
autorepeat if `EV_REP` is set.

## Touchscreens
Absolute axes with ranges: `input_set_abs_params(in, ABS_MT_POSITION_X, 0, 1023, 0, 0)`.
Multitouch type B (slots): `input_mt_init_slots(in, 10, INPUT_MT_DIRECT)`; per contact
`input_mt_slot`, `input_mt_report_slot_state`, `ABS_MT_POSITION_X/Y`; then
`input_mt_sync_frame` and `input_sync`. Use `touchscreen_parse_properties()` to honour DT
`touchscreen-size-x`, `touchscreen-inverted-x`, `touchscreen-swapped-x-y`.

## Testing
```sh
evtest                        # pick the device, see events and capabilities
libinput debug-events
cat /proc/bus/input/devices
```

## Verify
- [ ] `evtest` shows correct codes, press/release pairs and SYN_REPORT per report.
- [ ] Wakeup from suspend works for keys marked `wakeup-source` (if required).

## Checked

2026-10-26, Linux kernel documentation tree and headers (mainline, v7.3 tag, checked 2026-10-26).
Confirmed in Documentation/input/input-programming.rst: input_allocate_device, input_sync after a report, the core drops repeated same-value events, autorepeat enabled by setting EV_REP. Confirmed in include/linux/input.h: devm_input_allocate_device, input_set_capability, input_report_rel; include/linux/input/mt.h: INPUT_MT_DIRECT; include/linux/input/touchscreen.h: touchscreen_parse_properties. Confirmed in gpio-keys.yaml: gpios, linux,code, debounce-interval, wakeup-source. Confirmed present in the tree: gpio_keys.c, gpio_keys_polled.c, rotary_encoder.c, matrix_keypad.c, adc-keys.c, edt-ft5x06.c, goodix.c. The Ilitek driver name was removed as unchecked. evtest and libinput are userspace tools and were not checked.

Method: documentation only; no commands were run.
