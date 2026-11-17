---
id: computing-software.firmware-embedded-development.device-driver-development.devm-managed-resources
name: devm-managed-resources
category: computing-software
field: firmware-embedded-development
product: device-driver-development
tags: [platform-driver, devm-managed-resources, devm-kzalloc, devm-platform-ioremap-resource, devm-clk-get-enabled, devm-add-action-or-reset, probe-error-paths, firmware-embedded-development]
level: practitioner
status: docs-checked
description: "Use devm_* managed resources in Linux drivers so probe error paths and remove() need no manual cleanup, and know the ordering pitfalls with IRQs and workqueues."
sources:
  - https://docs.kernel.org/driver-api/driver-model/devres.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# devm managed resources

**Goal:** a probe function with no goto-cleanup ladder and a near-empty remove, without
use-after-free at unbind.

## Typical probe
```c
static int acme_probe(struct platform_device *pdev) {
    struct device *dev = &pdev->dev;
    struct acme *a = devm_kzalloc(dev, sizeof(*a), GFP_KERNEL);
    if (!a) return -ENOMEM;

    a->base = devm_platform_ioremap_resource(pdev, 0);
    if (IS_ERR(a->base)) return PTR_ERR(a->base);

    a->clk = devm_clk_get_enabled(dev, NULL);           /* get + prepare_enable, auto disable on unbind */
    if (IS_ERR(a->clk)) return dev_err_probe(dev, PTR_ERR(a->clk), "no clock\n");

    a->reset = devm_gpiod_get_optional(dev, "reset", GPIOD_OUT_HIGH);
    if (IS_ERR(a->reset)) return PTR_ERR(a->reset);

    int ret = devm_regulator_get_enable(dev, "vdd");
    if (ret) return dev_err_probe(dev, ret, "vdd\n");

    ret = devm_add_action_or_reset(dev, acme_hw_shutdown, a);   /* custom teardown */
    if (ret) return ret;

    platform_set_drvdata(pdev, a);
    return devm_iio_device_register(dev, a->indio);     /* registration last */
}
```
Devres entries are released when probe fails or the device is unbound, in reverse order of
registration (the devres core walks its list backwards).

## Ordering pitfalls
- **IRQ vs data it uses:** `devm_request_irq` registered early is freed late (after resources
  acquired later). If the handler uses something freed earlier during teardown (a workqueue, a
  buffer from non-devm allocation), the IRQ can fire on freed data. Request the IRQ after
  everything it uses, and make the hardware quiet in a devm action registered after the IRQ.
- **Mixing devm and manual**: a manual `kfree`/`clk_disable` in remove() for something also
  devm-managed double-frees. Either all devm for an object, or none.
- **Lifetime longer than the device binding** (objects user space can still hold, e.g. char
  device open files): devm memory is freed at unbind, while the file is open. Use reference
  counting for such objects; devm is for binding-scoped resources.
- `devm_kzalloc` in non-probe paths (e.g. per-open allocations) leaks until unbind.

## Useful helpers
`devm_platform_get_and_ioremap_resource`, `devm_clk_bulk_get_all_enabled`,
`devm_pinctrl_get_select`, `devm_mutex_init`, `devm_work_autocancel`,
`devm_pm_runtime_enable`, `devm_regmap_init_i2c`.

## Verify
- [ ] Inject failures at each step (fault injection or `return -EPROBE_DEFER` hacks): no leaks
      in `kmemleak`, no warnings.
- [ ] `echo <dev> > /sys/bus/platform/drivers/acme/unbind` and rebind 100 times cleanly.

## Checked

2026-10-26, Linux kernel documentation tree and headers (mainline, v7.3 tag, checked 2026-10-26).
Confirmed in Documentation/driver-api/driver-model/devres.rst: all devres entries are released on driver detach; devm_platform_ioremap_resource, devm_platform_get_and_ioremap_resource, devm_pinctrl_get_select, devm_regulator_get_enable, devm_gpiod_get_optional, devm_iio_device_register, devm_request_irq are listed. Confirmed in headers: devm_clk_get_enabled and devm_clk_bulk_get_all_enabled (include/linux/clk.h), devm_add_action_or_reset (device/devres.h), devm_mutex_init (mutex.h), devm_work_autocancel (devm-helpers.h), devm_pm_runtime_enable (pm_runtime.h), devm_regmap_init_i2c (regmap.h), dev_err_probe (dev_printk.h). Reverse release order confirmed in drivers/base/devres.c (list_for_each_entry_safe_reverse).

Method: documentation only; no commands were run.
