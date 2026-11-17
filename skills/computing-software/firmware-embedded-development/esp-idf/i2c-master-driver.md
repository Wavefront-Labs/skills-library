---
id: computing-software.firmware-embedded-development.esp-idf.i2c-master-driver
name: i2c-master-driver
category: computing-software
field: firmware-embedded-development
product: esp-idf
tags: [esp-peripherals, esp-i2c-master, i2c-new-master-bus, i2c-master-transmit-receive, i2c-probe, legacy-driver-conflict, esp-idf, firmware-embedded-development]
level: practitioner
status: docs-checked
description: "Talk to I2C devices with the ESP-IDF i2c_master driver: bus and device handles, register reads, probing, pull-ups, timeouts, and the legacy-driver conflict."
sources:
  - https://github.com/espressif/esp-idf/blob/master/docs/en/api-reference/peripherals/i2c.rst
  - https://github.com/espressif/esp-idf/blob/master/components/esp_driver_i2c/include/driver/i2c_master.h
  - https://github.com/espressif/esp-idf/blob/master/components/driver/i2c/i2c.c
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# I2C master driver (new API)

`driver/i2c_master.h` uses a bus handle plus one handle per device, replacing the command-link API
of the legacy `driver/i2c.h`.

## Bus and devices
```c
#include "driver/i2c_master.h"
static i2c_master_bus_handle_t bus;
static i2c_master_dev_handle_t tmp;

void i2c_init(void)
{
    i2c_master_bus_config_t bc = {
        .i2c_port = -1,                        /* -1: pick a free port (see the i2c_port field docs) */
        .sda_io_num = GPIO_NUM_8,
        .scl_io_num = GPIO_NUM_9,
        .clk_source = I2C_CLK_SRC_DEFAULT,
        .glitch_ignore_cnt = 7,
        .flags.enable_internal_pullup = true,  /* weak; see pull-ups below */
    };
    ESP_ERROR_CHECK(i2c_new_master_bus(&bc, &bus));

    i2c_device_config_t dc = {
        .dev_addr_length = I2C_ADDR_BIT_LEN_7,
        .device_address = 0x48,                /* 7-bit address, not shifted */
        .scl_speed_hz = 400000,
    };
    ESP_ERROR_CHECK(i2c_master_bus_add_device(bus, &dc, &tmp));
}
```

## Transfers
```c
esp_err_t reg_read(uint8_t reg, uint8_t *out, size_t n)
{   /* write register address, repeated START, read n bytes */
    return i2c_master_transmit_receive(tmp, &reg, 1, out, n, 50 /* ms */);
}
esp_err_t reg_write(uint8_t reg, uint8_t val)
{
    uint8_t buf[2] = { reg, val };
    return i2c_master_transmit(tmp, buf, sizeof buf, 50);
}
```
Timeouts are in ms; `-1` waits forever (avoid: a stuck bus then hangs the task). `ESP_ERR_TIMEOUT` means the
operation exceeded the timeout because the bus is busy or hardware crashed; handle other errors (for example a
NACK from a wrong address) by checking each function's return codes in `i2c_master.h`.

## Scan
```c
for (uint8_t a = 0x08; a < 0x78; a++)
    if (i2c_master_probe(bus, a, 20) == ESP_OK) printf("found 0x%02x\n", a);
```

## Pull-ups
The internal pull-up is not strong enough for high-speed buses; the guide recommends suitable external pull-ups
(1 kOhm to 10 kOhm usual range, 2 kOhm to 5 kOhm recommended, never below 1 kOhm; higher frequency needs a smaller
value). Standard mode is up to 100 kHz and fast mode up to 400 kHz. `i2c_master_probe` needs pull-ups fitted and
returns `ESP_ERR_TIMEOUT` without them. Check the rise time on a scope against the I2C specification.

## Concurrency
One device handle per device; master operation functions are thread safe through a bus operation semaphore.
Asynchronous operation (marked experimental in the guide) needs `.trans_queue_depth` in the bus config and a
callback registered with `i2c_master_register_event_callbacks`; on one bus only one device can use async mode.

## Legacy driver conflict
The old `driver/i2c.h` and new `driver/i2c_master.h` can't both be used: the legacy driver logs
"CONFLICT! driver_ng is not allowed to be used with this old driver" (the check can be skipped with
`CONFIG_I2C_SKIP_LEGACY_CONFLICT_CHECK`, but mixing is unsupported). This often comes from a third-party component
still using the legacy API. Migrate it.

## Bus recovery
A slave holding SDA low after a reset mid-transfer blocks the bus. `i2c_master_bus_reset(bus)` resets the I2C
master bus (the header gives no more detail); try it after repeated timeouts before giving up.

## Verify
- [ ] Probe finds every expected address at boot; missing device is logged clearly.
- [ ] Scope: rise time and clock frequency within spec at chosen speed.
- [ ] No component in the build includes `driver/i2c.h`.

## Checked

2026-10-26, against ESP-IDF master docs and headers (espressif/esp-idf, pushed 2026-10-24). Confirmed in peripherals/i2c.rst, i2c_master.h and components/driver/i2c/i2c.c: bus and device config fields (i2c_port, glitch_ignore_cnt typically 7, enable_internal_pullup, dev_addr_length, 7-bit device_address, scl_speed_hz), i2c_master_transmit_receive, i2c_master_probe signature and pull-up requirement, timeout -1 means wait forever, ESP_ERR_TIMEOUT meaning, bus operation thread safety, trans_queue_depth and callbacks, async experimental note, legacy conflict message and Kconfig skip option, i2c_master_bus_reset. Removed: the 5.2 version gate, internal pull-up resistance range, 300 ns rise-time figure, ESP_FAIL / INVALID_RESPONSE mapping, bus-reset clocking description.

Method: documentation only; no commands were run.
