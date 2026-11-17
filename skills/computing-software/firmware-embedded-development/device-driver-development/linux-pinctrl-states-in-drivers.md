---
id: computing-software.firmware-embedded-development.device-driver-development.linux-pinctrl-states-in-drivers
name: linux-pinctrl-states-in-drivers
category: computing-software
field: firmware-embedded-development
product: device-driver-development
tags: [linux-pinctrl, platform-driver, pinctrl-names, sleep-state, pin-muxing, firmware-embedded-development]
level: advanced
status: docs-checked
description: "Use pinctrl states in Linux device drivers: default/sleep/idle states in DT, automatic default state at probe, switching with pinctrl_pm_select_*, and debugging mux conflicts."
sources:
  - https://docs.kernel.org/driver-api/pin-control.html
  - https://github.com/torvalds/linux/blob/master/Documentation/devicetree/bindings/pinctrl/pinctrl-bindings.txt
  - https://github.com/torvalds/linux/blob/master/Documentation/devicetree/bindings/pinctrl/pincfg-node.yaml
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Pinctrl states in drivers

## Device tree
```dts
&uart4 {
    pinctrl-names = "default", "sleep";
    pinctrl-0 = <&uart4_pins_a>;           /* AF mode, pull-ups */
    pinctrl-1 = <&uart4_sleep_pins_a>;     /* analog/GPIO input to save power */
    status = "okay";
};
&pinctrl {
    uart4_pins_a: uart4-0 {
        pins1 { pinmux = <STM32_PINMUX('G', 11, AF6)>; bias-disable; drive-push-pull; slew-rate = <0>; };
        pins2 { pinmux = <STM32_PINMUX('B', 2, AF8)>; bias-pull-up; };
    };
};
```
Generic properties: `bias-pull-up/down/disable`, `drive-push-pull/open-drain`, `drive-strength`,
`slew-rate`, `input-enable`, `output-high/low` (see pincfg-node.yaml). Mux syntax (`pinmux`, `pins` + `function`,
`fsl,pins`) is SoC-specific: follow your SoC's binding.

## In the driver
The driver core applies the **"default"** state automatically before `probe()`; if both "init"
and "default" are defined, "init" is selected before probe and "default" after it. The "sleep"
and "idle" states can only be selected through the PM API. For power management:
```c
static int mydrv_suspend(struct device *dev) {
    /* stop the device first */
    return pinctrl_pm_select_sleep_state(dev);
}
static int mydrv_resume(struct device *dev) {
    pinctrl_pm_select_default_state(dev);
    /* restart the device */
    return 0;
}
```
Custom states (e.g. "gpio" for bus recovery on I2C):
```c
p = devm_pinctrl_get(dev);
st = pinctrl_lookup_state(p, "gpio");
pinctrl_select_state(p, st);         /* switch pins to GPIO to bit-bang 9 clocks, then back to "default" */
```
The I2C core implements recovery with `pinctrl-names = "default", "gpio"` plus `scl-gpios`/`sda-gpios`.

## Conflicts and debugging
```sh
cat /sys/kernel/debug/pinctrl/<controller>/pinmux-pins     # which device owns each pin
cat /sys/kernel/debug/pinctrl/<controller>/pinconf-pins
cat /sys/kernel/debug/pinctrl/pinctrl-handles
```
"pin PG11 already requested by 40010000.serial; cannot claim for 5c002000.i2c" means two enabled
nodes use the same pin: disable one or fix the overlay. GPIOs requested via `gpiod_get` and a
pinctrl mux on the same pin conflict on controllers whose pinmux ops set the `strict` flag.

## Verify
- [ ] `pinmux-pins` shows each pin owned by the intended device.
- [ ] Sleep state applied during suspend (measure current drop or read pinconf in debugfs).

## Checked

2026-10-26, Linux kernel documentation tree and headers (mainline, v7.3 tag, checked 2026-10-26).
Confirmed in Documentation/driver-api/pin-control.rst: standard state names default, init, sleep and idle; default selected before probe and init/default sequencing; sleep and idle only through the PM API; pinctrl_pm_select_default_state, _init_, _sleep_ and _idle_ helpers; devm_pinctrl_get, pinctrl_lookup_state and pinctrl_select_state; the strict flag in pinmux_ops denies simultaneous GPIO and mux use; debugfs files pinctrl-handles, pinmux-pins and pinconf-pins. Confirmed in drivers/pinctrl/pinmux.c: the message "pin %s already requested by %s; cannot claim for %s". Confirmed in drivers/i2c/i2c-core-base.c: bus recovery looks up pinctrl states "gpio" (or "recovery"). Confirmed in pincfg-node.yaml: bias-disable, bias-pull-up, bias-pull-down, drive-push-pull, drive-open-drain, drive-strength, input-enable, output-low, output-high, slew-rate. The STM32 example pin syntax is SoC specific, as the skill states.

Method: documentation only; no commands were run.
