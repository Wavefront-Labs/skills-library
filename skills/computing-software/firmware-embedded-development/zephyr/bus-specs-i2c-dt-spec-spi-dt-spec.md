---
id: computing-software.firmware-embedded-development.zephyr.bus-specs-i2c-dt-spec-spi-dt-spec
name: bus-specs-i2c-dt-spec-spi-dt-spec
category: computing-software
field: firmware-embedded-development
product: zephyr
tags: [i2c-dt-spec, spi-dt-spec, i2c-write-read-dt, spi-transceive-dt, spi-cs-gpios, zephyr, firmware-embedded-development]
level: practitioner
status: docs-checked
description: "Talk to I2C and SPI devices in Zephyr with i2c_dt_spec and spi_dt_spec: devicetree child nodes, register read/write helpers, SPI chip select and mode flags."
sources:
  - https://docs.zephyrproject.org/latest/hardware/peripherals/i2c.html
  - https://docs.zephyrproject.org/latest/hardware/peripherals/spi.html
  - https://github.com/zephyrproject-rtos/zephyr/blob/main/include/zephyr/drivers/i2c.h
  - https://github.com/zephyrproject-rtos/zephyr/blob/main/include/zephyr/drivers/spi.h
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Bus specs (i2c_dt_spec and spi_dt_spec)

## Devicetree
```dts
&i2c0 {
    status = "okay";
    clock-frequency = <I2C_BITRATE_FAST>;
    widget: widget@50 { compatible = "acme,widget-i2c"; reg = <0x50>; };
};

&spi1 {
    status = "okay";
    cs-gpios = <&gpio0 17 GPIO_ACTIVE_LOW>, <&gpio0 18 GPIO_ACTIVE_LOW>;
    adc: adc@1 {                         /* reg = chip-select index into cs-gpios */
        compatible = "acme,widget-spi";
        reg = <1>;
        spi-max-frequency = <8000000>;
    };
};
```

## I2C
```c
#include <zephyr/drivers/i2c.h>
static const struct i2c_dt_spec dev = I2C_DT_SPEC_GET(DT_NODELABEL(widget));

if (!i2c_is_ready_dt(&dev)) return -ENODEV;

uint8_t id;
i2c_reg_read_byte_dt(&dev, 0x0F, &id);                    /* 8-bit register */
i2c_reg_write_byte_dt(&dev, 0x20, 0x57);

uint8_t reg = 0x28, buf[6];
i2c_write_read_dt(&dev, &reg, 1, buf, sizeof buf);        /* repeated-start read */

i2c_burst_write_dt(&dev, 0x00, data, len);                /* reg + data, 8-bit reg */
```
Return values: 0 or a negative errno. `i2c_transfer_dt` with `struct i2c_msg[]` covers anything
else (flags `I2C_MSG_WRITE`, `I2C_MSG_READ`, `I2C_MSG_STOP`, `I2C_MSG_RESTART`).

## SPI
```c
#include <zephyr/drivers/spi.h>
/* Zephyr 4.4 and earlier; see the 4.5 note below */
#define SPI_OP (SPI_OP_MODE_MASTER | SPI_WORD_SET(8) | SPI_TRANSFER_MSB | SPI_MODE_CPOL | SPI_MODE_CPHA)
static const struct spi_dt_spec adc = SPI_DT_SPEC_GET(DT_NODELABEL(adc), SPI_OP, 0 /*cs delay us*/);

if (!spi_is_ready_dt(&adc)) return -ENODEV;

uint8_t tx[3] = { 0x01, 0x80, 0x00 }, rx[3];
struct spi_buf txb = { .buf = tx, .len = sizeof tx };
struct spi_buf rxb = { .buf = rx, .len = sizeof rx };
struct spi_buf_set txs = { .buffers = &txb, .count = 1 };
struct spi_buf_set rxs = { .buffers = &rxb, .count = 1 };
spi_transceive_dt(&adc, &txs, &rxs);
```
- Mode: the `SPI_MODE_CPOL`/`SPI_MODE_CPHA` flags select the clock polarity and phase. The macro
  also reads the node's `spi-cpol`, `spi-cpha`, `spi-hold-cs`, `spi-lsb-first` and `spi-cs-high`
  properties.
- The frequency comes from `spi-max-frequency` in devicetree.
- `SPI_HOLD_ON_CS` + `SPI_LOCK_ON` keep the device selected and locked across several calls;
  release with `spi_release_dt`.
- `spi_write_dt` / `spi_read_dt` for one-direction transfers.
- **Zephyr 4.5 (main) changes:** `SPI_OP_MODE_CONTROLLER` / `SPI_OP_MODE_PERIPHERAL` replace
  `SPI_OP_MODE_MASTER` / `SPI_OP_MODE_SLAVE` (old names deprecated, removal in 5.0), and the
  optional delay argument of `SPI_DT_SPEC_GET` and related macros is removed; set
  `spi-cs-setup-delay-ns` and `spi-cs-hold-delay-ns` in devicetree instead (nanoseconds, not
  microseconds).

## Gotchas
- I2C node `reg` is the 7-bit address; don't shift it.
- SPI `reg` is the CS index, not an address.
- The synchronous transfer calls are not marked ISR-safe; in the I2C API only the asynchronous
  variants (`i2c_transfer_cb`, `i2c_transfer_signal`) are documented `@isr_ok`.

## Verify
- [ ] Device addresses/CS indices in DT match the schematic.
- [ ] Logic analyser capture of a register read matches the datasheet sequence.

## Checked

Checked 2026-10-25 against the Zephyr source: include/zephyr/drivers/i2c.h and spi.h on main (post-4.4), spi.h at tag v4.4.2 (latest release), include/zephyr/dt-bindings/i2c/i2c.h and the 4.5 migration guide.
Confirmed: `I2C_DT_SPEC_GET`, `i2c_is_ready_dt`, `i2c_reg_read_byte_dt`, `i2c_reg_write_byte_dt`, `i2c_write_read_dt`, `i2c_burst_write_dt`, `i2c_transfer_dt` and the `I2C_MSG_*` flags; `I2C_BITRATE_FAST`; `SPI_DT_SPEC_GET`, `spi_is_ready_dt`, `spi_transceive_dt`, `spi_read_dt`, `spi_write_dt`, `spi_release_dt`, `SPI_HOLD_ON_CS`, `SPI_LOCK_ON`, `SPI_MODE_CPOL`/`CPHA`, `SPI_WORD_SET`, `SPI_TRANSFER_MSB`; at v4.4.2 `SPI_OP_MODE_MASTER` exists and `SPI_DT_SPEC_GET` takes an optional delay argument; on main the delay argument is removed and the MASTER/SLAVE names are deprecated.

Method: documentation only; no commands were run.
