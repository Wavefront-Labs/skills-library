---
id: computing-software.firmware-embedded-development.device-driver-development.linux-clock-and-reset-consumers
name: linux-clock-and-reset-consumers
category: computing-software
field: firmware-embedded-development
product: device-driver-development
tags: [clk-api, platform-driver, reset-controller, devm-clk-get-enabled, clock-names, firmware-embedded-development]
level: advanced
status: docs-checked
description: "Consume clocks and resets in Linux platform drivers: devm_clk_get_enabled, clk_set_rate and prepare/enable rules, reset_control_get and deassert sequencing, and DT clock-names."
sources:
  - https://docs.kernel.org/driver-api/clk.html
  - https://docs.kernel.org/driver-api/reset.html
  - https://github.com/devicetree-org/dt-schema/blob/main/dtschema/schemas/clock/clock.yaml
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Clock and reset consumers

## Device tree
```dts
adc@40012000 {
    compatible = "acme,adc";
    reg = <0x40012000 0x400>;
    clocks = <&rcc ADC_CK>, <&rcc ADC_BUS>;
    clock-names = "kernel", "bus";
    resets = <&rcc ADC_R>;
};
```

## Clocks in probe
```c
struct clk *kclk = devm_clk_get_enabled(&pdev->dev, "kernel");   /* get + prepare + enable, auto-disable on unbind */
if (IS_ERR(kclk))
    return dev_err_probe(&pdev->dev, PTR_ERR(kclk), "kernel clock\n");   /* handles -EPROBE_DEFER quietly */
struct clk *bclk = devm_clk_get_optional_enabled(&pdev->dev, "bus");    /* NULL if absent: calls become no-ops */

ret = clk_set_rate(kclk, 48000000);
rate = clk_get_rate(kclk);           /* the rate you actually got, may differ */
```
- `clk_prepare()` may sleep and must not be called from atomic context; `clk_enable()` may be
  called from atomic context: in IRQ context only enable/disable already-prepared clocks. `clk_prepare_enable` combines both for process context.
- Enable counts are reference counted: every enable needs a matching disable or the clock stays on
  (power) or is switched off under another user (crash).
- `devm_clk_bulk_get_all_enabled` for drivers with many clocks.
- Rate changes may propagate to parents and affect other devices; use `clk_round_rate` first and
  `assigned-clocks`/`assigned-clock-rates` in DT for fixed setups.

## Resets
```c
struct reset_control *rst = devm_reset_control_get_exclusive(&pdev->dev, NULL);
if (IS_ERR(rst)) return dev_err_probe(dev, PTR_ERR(rst), "reset\n");
reset_control_assert(rst);
usleep_range(10, 20);                 /* datasheet minimum reset pulse */
reset_control_deassert(rst);
```
`_shared` variants for resets used by several devices (reference counted deassert; exclusive
resets give direct control);
`_optional_` returns NULL if the DT has no `resets`. Order matters on many SoCs: enable the
bus clock before deasserting reset, or register accesses hang the bus.

## Debugging
```sh
cat /sys/kernel/debug/clk/clk_summary        # tree, enable/prepare counts, rates
cat /sys/kernel/debug/clk/<name>/clk_enable_count
```
`clk_ignore_unused` kernel parameter keeps bootloader-enabled but unclaimed clocks on (the kernel
otherwise disables them at late init): a quick test when a device dies after boot finishes.

## Verify
- [ ] `clk_summary` shows the expected rate and enable counts return to zero after unbind.
- [ ] Probe defers cleanly when the clock provider loads later.

## Checked

2026-10-26, Linux kernel documentation tree and headers (mainline, v7.3 tag, checked 2026-10-26).
Confirmed in include/linux/clk.h: devm_clk_get_enabled, devm_clk_get_optional_enabled, devm_clk_bulk_get_all_enabled. Confirmed in Documentation/driver-api/clk.rst: enable/disable operations are not allowed to sleep and may be used in atomic context, prepare operations may sleep and are not allowed in atomic context. Confirmed in Documentation/driver-api/reset.rst: shared resets use reference-counted deassertion, exclusive resets give direct control; include/linux/reset.h has devm_reset_control_get_exclusive and _shared. Confirmed in drivers/clk/clk.c: debugfs files clk_summary and clk_enable_count, and the clk_ignore_unused boot parameter (also in admin-guide/kernel-parameters.txt). Removed the unconfirmed "5.19+" version gate. The DT clock binding link now points to the dt-schema file the old kernel text file redirects to.

Method: documentation only; no commands were run.
