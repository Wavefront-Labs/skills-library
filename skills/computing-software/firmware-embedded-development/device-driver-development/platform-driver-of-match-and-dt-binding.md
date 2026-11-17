---
id: computing-software.firmware-embedded-development.device-driver-development.platform-driver-of-match-and-dt-binding
name: platform-driver-of-match-and-dt-binding
category: computing-software
field: firmware-embedded-development
product: device-driver-development
tags: [platform-driver, of-match-table, compatible-string, dt-binding-yaml, of-property-read, module-device-table, dt-schema, firmware-embedded-development]
level: advanced
status: docs-checked
description: "Bind a Linux platform driver to devicetree nodes: compatible strings, of_match_table, reading properties, MODULE_DEVICE_TABLE autoload and writing a dt-schema YAML binding."
sources:
  - https://docs.kernel.org/driver-api/driver-model/platform.html
  - https://docs.kernel.org/devicetree/bindings/writing-schema.html
  - https://docs.kernel.org/devicetree/bindings/writing-bindings.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Platform driver: OF match and DT binding

**Goal:** a driver that probes automatically for every matching devicetree node, reads its
configuration from DT, and has a binding that `dtbs_check` validates.

## Driver skeleton
```c
static const struct of_device_id acme_adc_of_match[] = {
    { .compatible = "acme,adc100", .data = &adc100_info },
    { .compatible = "acme,adc200", .data = &adc200_info },
    { }
};
MODULE_DEVICE_TABLE(of, acme_adc_of_match);    /* modalias -> udev autoloads the module */

static int acme_adc_probe(struct platform_device *pdev) {
    struct device *dev = &pdev->dev;
    const struct acme_info *info = device_get_match_data(dev);
    u32 rate;
    if (device_property_read_u32(dev, "acme,sample-rate-hz", &rate))
        rate = 1000;                              /* optional property default */
    ...
}
static struct platform_driver acme_adc_driver = {
    .probe = acme_adc_probe,
    .driver = { .name = "acme-adc", .of_match_table = acme_adc_of_match },
};
module_platform_driver(acme_adc_driver);
```
Use the generic `device_property_*` API (works for DT and ACPI) or `of_property_read_*`.

## DT node
```dts
adc@40012000 {
    compatible = "acme,adc200", "acme,adc100";   /* specific compatible first, then fallback */
    reg = <0x40012000 0x400>;
    interrupts = <GIC_SPI 18 IRQ_TYPE_LEVEL_HIGH>;
    clocks = <&rcc ADC_CK>;
    acme,sample-rate-hz = <8000>;
};
```

## Binding schema (Documentation/devicetree/bindings/iio/adc/acme,adc100.yaml)
```yaml
$id: http://devicetree.org/schemas/iio/adc/acme,adc100.yaml#
$schema: http://devicetree.org/meta-schemas/core.yaml#
title: ACME ADC100 family
maintainers: [ "Jane Dev <jane@example.com>" ]
properties:
  compatible:
    oneOf:
      - const: acme,adc100
      - items: [ { const: acme,adc200 }, { const: acme,adc100 } ]
  reg: { maxItems: 1 }
  interrupts: { maxItems: 1 }
  clocks: { maxItems: 1 }
  acme,sample-rate-hz: { description: Sample rate, minimum: 1, maximum: 100000 }
required: [ compatible, reg, interrupts, clocks ]
additionalProperties: false
```
Validate: `make dt_binding_check DT_SCHEMA_FILES=acme,adc100.yaml` and `make dtbs_check`
(`dtbs_check` skips schema files with errors, so run `dt_binding_check` first). Vendor prefixes
are registered in `vendor-prefixes.yaml`; use your own vendor prefix for real hardware.

## Gotchas
- Driver doesn't probe: compatible typo, node `status = "disabled"`, parent bus not probed, or
  module not loaded (missing `MODULE_DEVICE_TABLE`). Check `/sys/bus/platform/devices/`.
- Never invent properties when a standard one exists (`clocks`, `resets`, `*-gpios`, `*-supply`).

## Verify
- [ ] `dt_binding_check` and `dtbs_check` clean.
- [ ] Module autoloads at boot (`lsmod`), probe logs once per node.

## Checked

2026-10-26, Linux kernel documentation tree and headers (mainline, v7.3 tag, checked 2026-10-26).
Confirmed in Documentation/devicetree/bindings/writing-schema.rst: $id, $schema, maintainers, additionalProperties/unevaluatedProperties, make dt_binding_check with DT_SCHEMA_FILES, make dtbs_check (skips schemas with errors). Confirmed in writing-bindings.rst: use SoC-specific compatibles followed by a fallback. Confirmed in include/linux/property.h: device_property_read_u32 and device_get_match_data. Confirmed in Documentation/devicetree/bindings/vendor-prefixes.yaml: file exists and registers prefixes (note it already lists "acme", so the example vendor prefix is illustrative). Removed the /sys/firmware/devicetree/base path from the gotchas and the unconfirmed "vendor prefix must exist" rule was reworded to what the file does.

Method: documentation only; no commands were run.
