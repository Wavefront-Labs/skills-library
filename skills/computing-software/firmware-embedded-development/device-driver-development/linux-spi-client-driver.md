---
id: computing-software.firmware-embedded-development.device-driver-development.linux-spi-client-driver
name: linux-spi-client-driver
category: computing-software
field: firmware-embedded-development
product: device-driver-development
tags: [linux-spi-client, linux-driver-subsystem, spi-sync, spi-message, spidev, firmware-embedded-development]
level: advanced
status: docs-checked
description: "Write a Linux SPI client (protocol) driver: of_match and spi_device_id tables, spi_setup, spi_sync with messages and transfers, cs_change, DMA-safe buffers, and regmap_spi."
sources:
  - https://docs.kernel.org/spi/spi-summary.html
  - https://docs.kernel.org/driver-api/spi.html
  - https://github.com/torvalds/linux/blob/master/Documentation/devicetree/bindings/spi/spi-peripheral-props.yaml
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# SPI client drivers

## Device tree
```dts
&spi1 {
    status = "okay";
    cs-gpios = <&gpioa 4 GPIO_ACTIVE_LOW>;
    adc@0 {
        compatible = "acme,adc128";
        reg = <0>;                        /* chip select index */
        spi-max-frequency = <10000000>;
        spi-cpol; spi-cpha;               /* mode 3 */
        interrupts-extended = <&gpiob 2 IRQ_TYPE_EDGE_FALLING>;
    };
};
```

## Driver skeleton
```c
static int adc128_probe(struct spi_device *spi) {
    spi->bits_per_word = 8;
    int ret = spi_setup(spi);                     /* applies mode/speed from DT plus overrides */
    if (ret) return ret;
    struct adc128 *st = devm_kzalloc(&spi->dev, sizeof(*st), GFP_KERNEL);
    if (!st) return -ENOMEM;
    st->spi = spi;
    spi_set_drvdata(spi, st);
    return 0;
}
static const struct of_device_id adc128_of[] = { { .compatible = "acme,adc128" }, { } };
MODULE_DEVICE_TABLE(of, adc128_of);
static const struct spi_device_id adc128_id[] = { { "adc128" }, { } };   /* needed for module autoload */
MODULE_DEVICE_TABLE(spi, adc128_id);
static struct spi_driver adc128_driver = {
    .driver = { .name = "adc128", .of_match_table = adc128_of },
    .probe = adc128_probe, .id_table = adc128_id,
};
module_spi_driver(adc128_driver);
```
Missing `spi_device_id` table: the SPI core warns "SPI driver %s has no spi_device_id for %s"
because DT modules use `spi:` modaliases, so module autoloading will not work without the table.

## Transfers
```c
/* simple helpers */
spi_write(spi, buf, len);
spi_write_then_read(spi, &cmd, 1, rx, 2);   /* copies tx/rx data: for small transfers only */

/* full control: one CS assertion, two transfers */
struct spi_transfer xfers[] = {
    { .tx_buf = st->tx, .len = 2 },
    { .rx_buf = st->rx, .len = 4, .delay = { .value = 5, .unit = SPI_DELAY_UNIT_USECS } },
};
ret = spi_sync_transfer(spi, xfers, ARRAY_SIZE(xfers));
```
`cs_change = 1` on a transfer toggles CS after it (or keeps CS asserted after the last one).
`spi_sync` sleeps; `spi_async` + completion callback for non-sleeping contexts.

## DMA-safe buffers
Buffers passed to `spi_sync` must be DMA-safe: do not use the stack or anything declared
`static` (spi-summary), and not vmalloc memory or memory sharing a cache line with other fields.
IIO drivers put them at the end of the state struct with `__aligned(IIO_DMA_MINALIGN)`.

## Prefer regmap
For register-based devices, `devm_regmap_init_spi(spi, &cfg)` provides regmap access with
configurable read/write flag bits and optional caching.

## Testing from userspace
`spidev` with a specific compatible from its id table (the DT must not use the bare string
`spidev`, which the driver rejects) plus the `spidev_test` tool from `tools/spi`
(`-D` device, `-s` max speed, `-v` verbose) for bring-up before writing the kernel driver.

## Verify
- [ ] Device probes from DT; module autoloads; logic analyser shows correct mode, speed and CS framing.

## Checked

2026-10-26, Linux kernel documentation tree and headers (mainline, v7.3 tag, checked 2026-10-26).
Confirmed in include/linux/spi/spi.h: module_spi_driver, spi_async, spi_sync_transfer, spi_write_then_read ("copies txbuf and rxbuf data; for small transfers only"), struct spi_delay with SPI_DELAY_UNIT_USECS, cs_change. Confirmed in include/linux/regmap.h: devm_regmap_init_spi. Confirmed in drivers/spi/spi.c: warning text "SPI driver %s has no spi_device_id for %s" and the comment that spi: modaliases are used so autoloading fails without a spi_device_id. Confirmed in Documentation/spi/spi-summary.rst: spi_setup, DMA-safe buffers (no stack, nothing static), cs_change flag, synchronous wrappers may sleep and are layered over spi_async. Confirmed in spi-controller.yaml (cs-gpios) and spi-peripheral-props.yaml (reg, spi-max-frequency, spi-rx-bus-width). Confirmed in drivers/spi/spidev.c: spidev_of_check rejects the bare "spidev" compatible and specific compatibles are listed; tools/spi/spidev_test.c options -D, -s, -v. Confirmed in include/linux/iio/iio.h: IIO_DMA_MINALIGN. Removed the unconfirmed regmap debugfs path and the claim about an internal DMA-safe buffer for spi_write_then_read.

Method: documentation only; no commands were run.
