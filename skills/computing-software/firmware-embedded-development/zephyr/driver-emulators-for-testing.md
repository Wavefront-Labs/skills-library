---
id: computing-software.firmware-embedded-development.zephyr.driver-emulators-for-testing
name: driver-emulators-for-testing
category: computing-software
field: firmware-embedded-development
product: zephyr
tags: [zephyr-emul, emul-dt-inst-define, i2c-emul, backend-api, native-sim, driver-testing, zephyr, firmware-embedded-development]
level: advanced
status: docs-checked
description: "Test Zephyr device drivers without hardware by writing an I2C/SPI emulator (EMUL_DT_INST_DEFINE) bound to the same devicetree node and running on native_sim."
sources:
  - https://docs.zephyrproject.org/latest/hardware/emulator/index.html
  - https://docs.zephyrproject.org/latest/hardware/emulator/bus_emulators.html
  - https://docs.zephyrproject.org/latest/develop/test/twister.html
  - https://github.com/zephyrproject-rtos/zephyr/blob/main/include/zephyr/drivers/emul.h
  - https://github.com/zephyrproject-rtos/zephyr/blob/main/include/zephyr/drivers/i2c_emul.h
  - https://github.com/zephyrproject-rtos/zephyr/blob/main/include/zephyr/drivers/emul_sensor.h
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Driver emulators for testing

An emulator plays the device on the other side of the bus. The real driver runs unchanged
and talks over an **emulated bus controller**; the test pokes the emulator's registers through
a backend API.

## Devicetree (test overlay for native_sim)
```dts
/ {
    test_i2c: i2c@100 {
        compatible = "zephyr,i2c-emul-controller";
        reg = <0x100 4>;
        #address-cells = <1>;
        #size-cells = <0>;
        clock-frequency = <I2C_BITRATE_STANDARD>;
        status = "okay";

        tmp42: tmp42@48 {
            compatible = "acme,tmp42";        /* same node the real driver binds */
            reg = <0x48>;
        };
    };
};
```
```
CONFIG_EMUL=y
CONFIG_I2C=y
CONFIG_I2C_EMUL=y
CONFIG_ZTEST=y
```

## Emulator
```c
#define DT_DRV_COMPAT acme_tmp42
#include <zephyr/drivers/emul.h>
#include <zephyr/drivers/i2c_emul.h>

struct tmp42_emul_data { uint8_t regs[16]; uint8_t cur; };

static int tmp42_emul_transfer(const struct emul *e, struct i2c_msg *msgs, int n, int addr) {
    struct tmp42_emul_data *d = e->data;
    for (int i = 0; i < n; i++) {
        if (msgs[i].flags & I2C_MSG_READ) {
            for (int j = 0; j < msgs[i].len; j++) msgs[i].buf[j] = d->regs[d->cur++ & 0xF];
        } else {
            d->cur = msgs[i].buf[0];
            for (int j = 1; j < msgs[i].len; j++) d->regs[d->cur++ & 0xF] = msgs[i].buf[j];
        }
    }
    return 0;
}
static const struct i2c_emul_api tmp42_bus_api = { .transfer = tmp42_emul_transfer };
static int tmp42_emul_init(const struct emul *e, const struct device *parent) { return 0; }

/* backend for tests */
void tmp42_emul_set_reg(const struct emul *e, uint8_t r, uint8_t v)
{ ((struct tmp42_emul_data *)e->data)->regs[r] = v; }

#define TMP42_EMUL(n) \
    static struct tmp42_emul_data tmp42_emul_data_##n; \
    EMUL_DT_INST_DEFINE(n, tmp42_emul_init, &tmp42_emul_data_##n, NULL, &tmp42_bus_api, NULL);
DT_INST_FOREACH_STATUS_OKAY(TMP42_EMUL)
```
For sensors, implementing `emul_sensor_driver_api` (backend_api argument) lets generic tests
use `emul_sensor_backend_set_channel()`.

## Test
```c
ZTEST(tmp42, test_reads_positive_temp) {
    const struct emul *e = EMUL_DT_GET(DT_NODELABEL(tmp42));
    const struct device *dev = DEVICE_DT_GET(DT_NODELABEL(tmp42));
    tmp42_emul_set_reg(e, 0x00, 0x19);                /* 25 C */
    struct sensor_value v;
    zassert_ok(sensor_sample_fetch(dev));
    zassert_ok(sensor_channel_get(dev, SENSOR_CHAN_AMBIENT_TEMP, &v));
    zassert_equal(v.val1, 25);
}
```
Run: `west twister -p native_sim -T <path to your test>` (`-p` selects the platform, `-T` the test root).

## What to emulate
Register map, reset values, read-only/clear-on-read bits, and **error injection** (return
`-EIO` from transfer, NAK on a set address) so the driver's error paths get tested. Data
sheets' quirks belong in the emulator; that's where most driver bugs hide.

## Verify
- [ ] Driver tests pass on native_sim in CI, no hardware.
- [ ] At least one test injects a bus error and checks the driver's recovery.
- [ ] Emulator lives next to the driver (same module) so they evolve together.

## Checked

Zephyr v4.4.2 documentation and source (latest release on 2026-10-27), read from the zephyr repository.
Confirmed in the headers, bindings and Kconfig: `EMUL_DT_DEFINE`/`EMUL_DT_INST_DEFINE(inst, init_fn, data_ptr, cfg_ptr, bus_api, backend_api)`, `EMUL_DT_GET`, the `emul_init_t` signature (emul, parent), `struct i2c_emul_api { transfer }` with `int (*)(const struct emul *, struct i2c_msg *, int num_msgs, int addr)` returning 0 or -EIO, the `zephyr,i2c-emul-controller` binding (requires `reg`), `CONFIG_EMUL` and `CONFIG_I2C_EMUL` (default y when the controller node is enabled), `emul_sensor_driver_api` and `emul_sensor_backend_set_channel`; the emulator reuses the same devicetree node as the real device (bus emulators doc); twister `-p`/`--platform` and `-T`.
Removed the specific example test path (tests/drivers/tmp42 is not a Zephyr path).

Method: documentation only; no commands were run.
