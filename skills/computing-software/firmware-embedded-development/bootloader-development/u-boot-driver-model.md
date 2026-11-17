---
id: computing-software.firmware-embedded-development.bootloader-development.u-boot-driver-model
name: u-boot-driver-model
category: computing-software
field: firmware-embedded-development
product: bootloader-development
tags: [u-boot-dm, u-boot, driver-model, uclass, bootph-pre-ram, firmware-embedded-development]
level: advanced
status: docs-checked
description: "Write and debug U-Boot driver model drivers: U_BOOT_DRIVER, uclasses, of_match, probe and priv data, bootph tags for SPL, and the dm tree/uclass commands."
sources:
  - https://docs.u-boot.org/en/latest/develop/driver-model/index.html
  - https://docs.u-boot.org/en/latest/develop/driver-model/design.html
  - https://docs.u-boot.org/en/latest/develop/spl.html
  - https://docs.u-boot.org/en/latest/usage/cmd/dm.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# U-Boot driver model

## Structure
- **uclass**: a class of devices with a common API (`UCLASS_I2C`, `UCLASS_GPIO`, `UCLASS_MMC`,
  `UCLASS_REGULATOR`, `UCLASS_MISC`...). Consumers call uclass functions (`dm_i2c_read`,
  `dm_gpio_set_value`).
- **driver**: implements a uclass's ops for specific hardware, bound to DT nodes by compatible.
- **device**: an instance; bound at startup (cheap), probed (hardware init) only on first use.

## Minimal driver
```c
struct acme_led_priv { struct gpio_desc gpio; };

static int acme_led_probe(struct udevice *dev) {
    struct acme_led_priv *priv = dev_get_priv(dev);
    return gpio_request_by_name(dev, "led-gpios", 0, &priv->gpio, GPIOD_IS_OUT);
}
static int acme_led_set_state(struct udevice *dev, enum led_state_t st) {
    struct acme_led_priv *priv = dev_get_priv(dev);
    return dm_gpio_set_value(&priv->gpio, st == LEDST_ON);
}
static const struct led_ops acme_led_ops = { .set_state = acme_led_set_state };
static const struct udevice_id acme_led_ids[] = { { .compatible = "acme,led" }, { } };

U_BOOT_DRIVER(acme_led) = {
    .name = "acme_led",
    .id = UCLASS_LED,
    .of_match = acme_led_ids,
    .probe = acme_led_probe,
    .ops = &acme_led_ops,
    .priv_auto = sizeof(struct acme_led_priv),
};
```
Read DT properties with `dev_read_u32`, `dev_read_addr`, `dev_read_string`. Add a Kconfig symbol
and a Makefile entry for the driver, and make sure the uclass's own option is enabled.

## SPL and pre-relocation
Before relocation only drivers flagged `DM_FLAG_PRE_RELOC` or DT nodes with a `bootph-` property
are bound, and SPL/TPL device trees keep only nodes with such properties:
```dts
&uart2 { bootph-all; };            /* bind in all phases */
&i2c1  { bootph-pre-ram; };        /* SPL, before DRAM */
```
`bootph-pre-sram` (TPL) and `bootph-some-ram` (U-Boot proper, pre-relocation only) also exist. Put
these in the board's `-u-boot.dtsi` so the shared Linux DTS stays clean. Enable driver model in SPL
with `CONFIG_SPL_DM`.

## Debugging
```
=> dm tree            # all devices, uclass, driver, probed status
=> dm uclass          # devices per uclass with sequence numbers
=> dm drivers
=> dm compat          # driver compatible strings
```
A device listed but not probed is normal until used. A node missing from `dm tree` means no
driver matched its compatible, or it isn't tagged for this phase.

## Verify
- [ ] `dm tree` shows the device bound and probed after first use; the uclass's command (e.g. `led`) works.
- [ ] Device available in SPL when required (bootph tags), not bound when not needed (size).

## Checked
2026-10-31. Confirmed against the U-Boot driver model design page (bind then probe separated, of_match, priv_auto, bootph-all/pre-ram/pre-sram/some-ram, CONFIG_SPL_DM), the dm command page, the SPL page and include/led.h and gpio.h (led_ops.set_state, led_state_t). Removed the old `u-boot,dm-*` property names, `CONFIG_SPL_OF_CONTROL`, `OF_PLATDATA` and the `status = "disabled"` remark, which the fetched pages do not state.
Method: documentation only; no commands were run.
