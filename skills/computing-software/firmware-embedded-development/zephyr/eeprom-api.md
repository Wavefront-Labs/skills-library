---
id: computing-software.firmware-embedded-development.zephyr.eeprom-api
name: eeprom-api
category: computing-software
field: firmware-embedded-development
product: zephyr
tags: [zephyr-eeprom, eeprom-read, eeprom-write, at24-eeprom, eeprom-emulator, zephyr, firmware-embedded-development]
level: practitioner
status: docs-checked
description: "Store small persistent data with Zephyr's EEPROM API: AT24/AT25 devicetree nodes, page-write handling, the flash-backed EEPROM emulator, and simulator for tests."
sources:
  - https://github.com/zephyrproject-rtos/zephyr/blob/main/dts/bindings/mtd/atmel,at2x-base.yaml
  - https://github.com/zephyrproject-rtos/zephyr/blob/main/dts/bindings/mtd/atmel,at24.yaml
  - https://github.com/zephyrproject-rtos/zephyr/blob/main/dts/bindings/mtd/zephyr,emu-eeprom.yaml
  - https://github.com/zephyrproject-rtos/zephyr/blob/main/dts/bindings/mtd/zephyr,sim-eeprom.yaml
  - https://github.com/zephyrproject-rtos/zephyr/blob/main/drivers/eeprom/eeprom_at2x.c
  - https://github.com/zephyrproject-rtos/zephyr/blob/main/include/zephyr/drivers/eeprom.h
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# EEPROM API

## Devicetree (I2C AT24-family)
```dts
&i2c0 {
    eeprom0: eeprom@50 {
        compatible = "atmel,at24";
        reg = <0x50>;
        size = <32768>;          /* bytes (24C256) */
        pagesize = <64>;
        address-width = <16>;
        timeout = <5>;           /* ms write cycle */
        wp-gpios = <&gpio0 7 GPIO_ACTIVE_HIGH>;  /* optional write protect; check polarity against the schematic */
    };
};
```
SPI parts use `atmel,at25`. The binding says many vendors' EEPROMs share the AT24 programming model: list the
specific model first and keep `atmel,at24` as the least-specific compatible, and take `size`, `pagesize`,
`address-width` and `timeout` (write-cycle timeout in ms) from the datasheet. All four are required properties.

## API
```c
#include <zephyr/drivers/eeprom.h>
static const struct device *const ee = DEVICE_DT_GET(DT_NODELABEL(eeprom0));

struct cal { uint32_t magic; int16_t offset; int16_t gain; uint16_t crc; };

int cal_load(struct cal *c) {
    if (!device_is_ready(ee)) return -ENODEV;
    int rc = eeprom_read(ee, 0x0000, c, sizeof *c);
    if (rc) return rc;
    return (c->magic == 0xCA11AB1E && crc16_ccitt(0xffff, (uint8_t *)c, offsetof(struct cal, crc)) == c->crc) ? 0 : -EINVAL;
}

int cal_save(struct cal *c) {
    c->magic = 0xCA11AB1E;
    c->crc = crc16_ccitt(0xffff, (uint8_t *)c, offsetof(struct cal, crc));
    return eeprom_write(ee, 0x0000, c, sizeof *c);
}
size_t sz = eeprom_get_size(ee);
```
The AT24/AT25 driver writes at most one page at a time and never across a page boundary, polling for the write
cycle up to `timeout`, so arbitrary offsets and lengths work. A write spanning several pages is **not atomic**: power loss can leave it half
written. Use a CRC plus two copies (A/B with a sequence number) for important data.

## Flash-backed emulator
No EEPROM chip? `compatible = "zephyr,emu-eeprom"` on a flash partition:
```dts
eeprom_emu: emu-eeprom {
    compatible = "zephyr,emu-eeprom";
    size = <1024>;
    pagesize = <4096>;
    partition = <&eeprom_partition>;
    rambuf;
};
```
The binding describes it as an emulated EEPROM stored in a flash partition (`rambuf` keeps a RAM copy for faster
reads; `partition-erase` delays erase until the whole partition is used, and data is lost if power fails during that
erase). NVS/ZMS or settings are usually better choices for new designs, but the emulator keeps EEPROM-style code working.

## Testing
`compatible = "zephyr,sim-eeprom"` gives a simulated EEPROM (RAM or a file, default `eeprom.bin`) for native simulator builds.

## Gotchas
- Endurance (see the datasheet) still matters for counters written every second; spread writes or keep
  counters in RAM and save periodically.
- With `wp-gpios` set, the driver sets the pin logical 1 to write-protect and logical 0 to allow writes, so the
  devicetree polarity flag must match the wiring.

## Verify
- [ ] Size/pagesize/address-width match the part's datasheet.
- [ ] Records carry a CRC and survive power cuts mid-write (A/B scheme).

## Checked

Checked 2026-10-26 against the Zephyr main branch on GitHub: AT24/AT25 bindings (required `size`, `pagesize`, `address-width`,
`timeout`; `wp-gpios`), `eeprom_at2x.c` (one page per write, never across a boundary; write-protect pin driven by logical level),
`zephyr,emu-eeprom` and `zephyr,sim-eeprom` bindings and simulator source, and `eeprom_read()`/`eeprom_write()`/`eeprom_get_size()`
and `crc16_ccitt()` declarations. Removed the wear-levelling, 1M-cycle endurance and `-EIO` diagnosis claims, which no Zephyr
source or document confirms.

Method: documentation only; no commands were run.
