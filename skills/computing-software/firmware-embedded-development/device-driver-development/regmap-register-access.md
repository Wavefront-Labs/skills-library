---
id: computing-software.firmware-embedded-development.device-driver-development.regmap-register-access
name: regmap-register-access
category: computing-software
field: firmware-embedded-development
product: device-driver-development
tags: [platform-driver, regmap, regmap-config, regmap-update-bits, regcache, volatile-registers, regmap-i2c, regmap-debugfs, firmware-embedded-development]
level: advanced
status: docs-checked
description: "Use Linux regmap for device register access over I2C/SPI/MMIO: regmap_config, caching with volatile/readable tables, update_bits, suspend/resume sync and debugfs inspection."
sources:
  - https://docs.kernel.org/driver-api/regmap.html
  - https://github.com/torvalds/linux/blob/master/include/linux/regmap.h
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# regmap register access

**Goal:** one register API independent of the bus, with locking, caching and debug views for
free, instead of hand-rolled `i2c_smbus_*` wrappers.

## Configuration
```c
static bool acme_volatile(struct device *dev, unsigned int reg) {
    switch (reg) {
    case ACME_REG_STATUS: case ACME_REG_DATA_L: case ACME_REG_DATA_H: return true;
    default: return false;
    }
}
static const struct regmap_config acme_regmap_cfg = {
    .reg_bits = 8, .val_bits = 8,
    .max_register = 0x7F,
    .volatile_reg = acme_volatile,
    .cache_type = REGCACHE_MAPLE,          /* sparse cache; REGCACHE_RBTREE is mainly legacy */
};
/* probe: */
a->map = devm_regmap_init_i2c(client, &acme_regmap_cfg);   /* or _spi, _mmio */
if (IS_ERR(a->map)) return PTR_ERR(a->map);
```

## Using it
```c
regmap_read(a->map, ACME_REG_WHOAMI, &val);
regmap_write(a->map, ACME_REG_CTRL, 0x01);
regmap_update_bits(a->map, ACME_REG_CTRL, ACME_ODR_MASK, FIELD_PREP(ACME_ODR_MASK, odr));
regmap_bulk_read(a->map, ACME_REG_DATA_L, buf, 2);      /* auto-increment burst */
```
`regmap_field` (`devm_regmap_field_alloc` with `REG_FIELD(reg, lsb, msb)`) gives named bitfields.

## Caching
- Non-volatile registers are served from cache: fewer bus transactions; `update_bits` on cached
  registers needs no read.
- **Mark every register the hardware changes as volatile** (status, data, self-clearing bits).
  A missed volatile register returns stale values forever.
- Suspend/resume when the device loses power: `regcache_cache_only(map, true)` + `regcache_mark_dirty`
  on suspend; on resume `regcache_cache_only(map, false)` and `regcache_sync(map)` restores the
  whole configuration.
- Provide `reg_defaults` (power-on values) where known; the sparse caches otherwise initialise
  entries from hardware.

## Debugging
`/sys/kernel/debug/regmap/<dev>/registers` dumps readable registers; the `cache_only`,
`cache_bypass` and `cache_dirty` debugfs entries help isolate cache bugs. regmap also provides
tracepoints (`include/trace/events/regmap.h`).

## Gotchas
- Registers with read side effects (clear-on-read) must be marked `precious_reg` (it must not be
  read outside driver calls) so debugfs dumps don't read them.
- Different endianness / address formats: `.reg_format_endian`, `.val_format_endian`,
  `.read_flag_mask` (SPI read bit), `.pad_bits`.
- Locking: regmap locks internally; multi-register sequences still need a driver mutex.

## Verify
- [ ] debugfs register dump matches the datasheet defaults after probe.
- [ ] Suspend/resume cycle restores configuration (compare dumps).

## Checked

2026-10-26, Linux kernel documentation tree and headers (mainline, v7.3 tag, checked 2026-10-26).
Confirmed in include/linux/regmap.h: REGCACHE_RBTREE and REGCACHE_MAPLE (header calls rbtree mainly legacy and says sparse caches initialise entries from hardware when no default is given), volatile_reg, precious_reg (clear-on-read example), reg_defaults, pad_bits, read_flag_mask, reg_format_endian, val_format_endian, devm_regmap_init_i2c/_spi, regmap_read, regmap_bulk_read, regmap_update_bits, regcache_sync, regcache_cache_only, regcache_mark_dirty, REG_FIELD, devm_regmap_field_alloc. Confirmed in drivers/base/regmap/regmap-debugfs.c: registers, cache_only, cache_bypass and cache_dirty debugfs files. include/trace/events/regmap.h exists. The volatile callback is documented as marking registers whose value cannot be cached.

Method: documentation only; no commands were run.
