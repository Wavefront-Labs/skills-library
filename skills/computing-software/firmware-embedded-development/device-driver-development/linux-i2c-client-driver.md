---
id: computing-software.firmware-embedded-development.device-driver-development.linux-i2c-client-driver
name: linux-i2c-client-driver
category: computing-software
field: firmware-embedded-development
product: device-driver-development
tags: [linux-driver-subsystem, linux-i2c-client, i2c-driver, module-i2c-driver, i2c-device-id, i2c-smbus, i2c-transfer, i2cdetect, firmware-embedded-development]
level: advanced
status: docs-checked
description: "Write a Linux I2C client driver: i2c_driver with OF and ID tables, probe with regmap or SMBus helpers, raw i2c_transfer for combined messages, and debugging with i2c-tools."
sources:
  - https://docs.kernel.org/i2c/writing-clients.html
  - https://docs.kernel.org/i2c/smbus-protocol.html
  - https://docs.kernel.org/i2c/i2c-sysfs.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Linux I2C client driver

**Goal:** a kernel driver for an I2C chip (sensor, PMIC, GPIO expander) instantiated from
devicetree, using the kernel's I2C core correctly.

## Skeleton
```c
static int acme_probe(struct i2c_client *client) {
    struct device *dev = &client->dev;
    if (!i2c_check_functionality(client->adapter, I2C_FUNC_SMBUS_BYTE_DATA))
        return -EOPNOTSUPP;
    int id = i2c_smbus_read_byte_data(client, ACME_REG_WHOAMI);
    if (id < 0) return dev_err_probe(dev, id, "no response\n");
    if (id != ACME_WHOAMI) return dev_err_probe(dev, -ENODEV, "bad id 0x%02x\n", id);
    ...
    return 0;
}
static const struct of_device_id acme_of_match[] = { { .compatible = "acme,th100" }, { } };
MODULE_DEVICE_TABLE(of, acme_of_match);
static const struct i2c_device_id acme_id[] = { { "th100" }, { } };
MODULE_DEVICE_TABLE(i2c, acme_id);
static struct i2c_driver acme_driver = {
    .driver = { .name = "acme-th100", .of_match_table = acme_of_match },
    .probe = acme_probe,          /* int (*probe)(struct i2c_client *client) */
    .id_table = acme_id,
};
module_i2c_driver(acme_driver);
```
DT: a child node of the I2C controller with `reg = <0x44>` (7-bit address).

## Bus access choices
- SMBus helpers: `i2c_smbus_read_byte_data`, `_word_data` (little-endian!; use
  `_swapped` variants for big-endian chips), `i2c_smbus_read_i2c_block_data` (SMBus limits blocks to 32 bytes).
- `regmap` (`devm_regmap_init_i2c`): preferred for register-based chips (caching, debugfs).
- Raw `i2c_transfer` for combined write-then-read without STOP, or non-register protocols:
  ```c
  struct i2c_msg msgs[] = {
      { .addr = client->addr, .flags = 0, .len = 1, .buf = &reg },
      { .addr = client->addr, .flags = I2C_M_RD, .len = n, .buf = data } };
  ret = i2c_transfer(client->adapter, msgs, 2);   /* returns number of msgs or -errno */
  ```
  Buffers must be DMA-safe (not on the stack) for adapters using DMA; use kmalloc'd or
  `i2c_get_dma_safe_msg_buf`.

## Debugging with i2c-tools
`i2cdetect -l` lists the adapters and `i2cget -y <bus> <addr>` reads a device (both appear in the
kernel I2C documentation; the tools come from the i2c-tools project). Unbind your driver first to
avoid interfering.

## Gotchas
- Return values: negative errno on failure; check every call.
- Instantiating from user space for testing: `echo th100 0x44 > /sys/bus/i2c/devices/i2c-1/new_device`.

## Verify
- [ ] Driver binds from DT (`ls /sys/bus/i2c/drivers/acme-th100/`).
- [ ] Unbind/bind cycle and missing-device case handled without oops.

## Checked

2026-10-26, Linux kernel documentation tree and headers (mainline, v7.3 tag, checked 2026-10-26).
Confirmed in Documentation/i2c/writing-clients.rst: i2c_driver with single-argument int foo_probe(struct i2c_client *client). Confirmed in include/linux/i2c.h: probe member takes only the client, module_i2c_driver, i2c_smbus_read_word_swapped, i2c_get_dma_safe_msg_buf, I2C_SMBUS_BLOCK_MAX. Confirmed in Documentation/i2c/smbus-protocol.rst: block reads and writes of up to 32 bytes, swapped word helpers. Confirmed in Documentation/i2c/i2c-sysfs.rst: new_device file under the adapter. Removed as unconfirmed: the "since 6.3" probe gate and the adapter clock-stretching remark. Confirmed in Documentation/i2c/dev-interface.rst and gpio-fault-injection.rst: i2cdetect -l and i2cget -y exist and come from i2c-tools. Removed as unconfirmed: the i2cdetect "UU" marker, i2cdump and i2ctransfer syntax.

Method: documentation only; no commands were run.
