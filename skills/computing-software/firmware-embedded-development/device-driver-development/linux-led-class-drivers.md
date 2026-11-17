---
id: computing-software.firmware-embedded-development.device-driver-development.linux-led-class-drivers
name: linux-led-class-drivers
category: computing-software
field: firmware-embedded-development
product: device-driver-development
tags: [led-class, linux-driver-subsystem, led-triggers, gpio-leds, multicolor-led, firmware-embedded-development]
level: practitioner
status: docs-checked
description: "Expose LEDs through the Linux LED class: gpio-leds/pwm-leds in DT, a custom led_classdev with brightness_set_blocking, triggers (heartbeat, netdev, timer), and multicolour LEDs."
sources:
  - https://docs.kernel.org/leds/leds-class.html
  - https://github.com/torvalds/linux/blob/master/Documentation/devicetree/bindings/leds/common.yaml
  - https://docs.kernel.org/leds/leds-class-multicolor.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# LED class drivers

## DT-only for GPIO and PWM LEDs
```dts
leds {
    compatible = "gpio-leds";
    led-status {
        color = <LED_COLOR_ID_GREEN>;
        function = LED_FUNCTION_STATUS;
        gpios = <&gpio2 7 GPIO_ACTIVE_HIGH>;
        linux,default-trigger = "heartbeat";
        default-state = "off";
    };
};
```
`color` + `function` generate a `color:function` name such as `green:status` (sysfs
`/sys/class/leds/green:status`). `pwm-leds` gives brightness levels; `max-brightness` sets the scale.

## Custom LED controller driver (I2C LED driver chip)
```c
static int acme_led_set(struct led_classdev *cdev, enum led_brightness b) {   /* may sleep */
    struct acme_led *l = container_of(cdev, struct acme_led, cdev);
    return regmap_write(l->chip->regmap, REG_PWM(l->idx), b);
}
l->cdev.max_brightness = 255;
l->cdev.brightness_set_blocking = acme_led_set;      /* use brightness_set only if it never sleeps */
struct led_init_data init = { .fwnode = child_fwnode, .devicename = "acme" };
ret = devm_led_classdev_register_ext(dev, &l->cdev, &init);   /* parses color/function/label from DT */
```
Hardware blink offload: implement `blink_set` so the timer trigger uses the chip's blink engine
instead of software timers.

## Triggers
```sh
cat /sys/class/leds/green:status/trigger          # [none] heartbeat timer netdev mmc0 disk-activity ...
echo timer > /sys/class/leds/green:status/trigger; echo 100 > delay_on; echo 900 > delay_off
echo netdev > trigger; echo eth0 > device_name; echo 1 > link; echo 1 > rx
```
Triggers need their Kconfig options (for example the heartbeat, timer and netdev triggers).

## Multicolour (RGB) LEDs
`led_classdev_mc` with `multi_intensity` per colour channel; DT node `color = <LED_COLOR_ID_RGB>`
with subnodes per channel. Userspace writes `multi_intensity` (e.g. `255 0 128`) and `brightness`.

## Verify
- [ ] LED named per the color:function convention; brightness writes take effect; default trigger active at boot.
- [ ] Triggers that may run in atomic context work with your brightness op (blocking ops are deferred by the core).

## Checked

2026-10-26, Linux kernel documentation tree and headers (mainline, v7.3 tag, checked 2026-10-26).
Confirmed in include/linux/leds.h: brightness_set_blocking (brightness_set must not sleep), blink_set, struct led_init_data, devm_led_classdev_register_ext. Confirmed in Documentation/leds/leds-class.rst: triggers chosen via /sys/class/leds/<device>/trigger, trigger parameters appear once selected, the timer trigger. Confirmed in Documentation/leds/leds-class-multicolor.rst: multi_intensity and multi_index files. Confirmed in leds/common.yaml: function, color, label, default-state, linux,default-trigger, max-brightness, trigger names heartbeat, timer and netdev. Confirmed present: leds-gpio.c, leds-pwm.c, ledtrig-netdev.c, ledtrig-heartbeat.c, ledtrig-timer.c. Confirmed in Documentation/ABI/testing/sysfs-class-led-trigger-netdev: device_name, link, tx and rx attributes. Removed the exact CONFIG_LEDS_TRIGGER_* symbol names (not checked in Kconfig).

Method: documentation only; no commands were run.
