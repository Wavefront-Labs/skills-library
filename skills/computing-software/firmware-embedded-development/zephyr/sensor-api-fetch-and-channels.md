---
id: computing-software.firmware-embedded-development.zephyr.sensor-api-fetch-and-channels
name: sensor-api-fetch-and-channels
category: computing-software
field: firmware-embedded-development
product: zephyr
tags: [sensor-channel-get, sensor-sample-fetch, sensor-value, sensor-trigger, sensor-attr-set, rtio-sensor-read, zephyr, firmware-embedded-development]
level: practitioner
status: docs-checked
description: "Read Zephyr sensors with sensor_sample_fetch and sensor_channel_get, convert sensor_value, set attributes and triggers, and know when to use the newer read/decode API."
sources:
  - https://github.com/zephyrproject-rtos/zephyr/blob/main/include/zephyr/drivers/sensor.h
  - https://github.com/zephyrproject-rtos/zephyr/blob/main/doc/hardware/peripherals/sensor/read_and_decode.rst
  - https://github.com/zephyrproject-rtos/zephyr/blob/main/drivers/sensor/Kconfig
  - https://github.com/zephyrproject-rtos/zephyr/blob/main/drivers/sensor/st/lis2dh/Kconfig
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Sensor API

## Fetch and get (classic)
```c
#include <zephyr/drivers/sensor.h>

static const struct device *const bme = DEVICE_DT_GET_ONE(bosch_bme280);

int read_env(void)
{
    struct sensor_value t, p, h;
    if (!device_is_ready(bme)) return -ENODEV;

    int rc = sensor_sample_fetch(bme);                 /* one bus transaction, cached in driver */
    if (rc) return rc;
    sensor_channel_get(bme, SENSOR_CHAN_AMBIENT_TEMP, &t);
    sensor_channel_get(bme, SENSOR_CHAN_PRESS, &p);
    sensor_channel_get(bme, SENSOR_CHAN_HUMIDITY, &h);

    printk("T=%d.%06d C\n", t.val1, t.val2);
    double tc = sensor_value_to_double(&t);           /* needs FP; or sensor_value_to_milli() */
    return 0;
}
```
- `struct sensor_value` is `val1 + val2 * 10^-6`, and negative values also follow that formula
  (-0.5 is `val1 = 0, val2 = -500000`; -1.5 is `val1 = -1, val2 = -500000`).
- Units are fixed per channel: pressure in **kPa**, acceleration in m/s^2, angular velocity in rad/s, magnetic
  field in G (gauss). Read the channel comments in `sensor.h` before converting.
- `sensor_sample_fetch()` fetches all channels (`SENSOR_CHAN_ALL`) and blocks until done; it is unsafe in an ISR
  for I2C/SPI devices. `sensor_sample_fetch_chan(dev, chan)` fetches one channel type.
- Multi-axis: pass the `_XYZ` channel (for example `SENSOR_CHAN_ACCEL_XYZ`) to `sensor_channel_get()` with an
  array; the values come back at `val[0]`, `val[1]`, `val[2]` (X, Y, Z).

## Attributes
```c
struct sensor_value odr = { .val1 = 100 };            /* 100 Hz */
sensor_attr_set(accel, SENSOR_CHAN_ACCEL_XYZ, SENSOR_ATTR_SAMPLING_FREQUENCY, &odr);
sensor_attr_set(accel, SENSOR_CHAN_ACCEL_XYZ, SENSOR_ATTR_FULL_SCALE, &(struct sensor_value){ .val1 = 16 });
```
Support varies by driver; check the return value (a negative errno such as `-ENOTSUP`, or `-ENOSYS` if the
driver has no attribute support).

## Triggers (data-ready, threshold, motion)
```c
static void drdy_handler(const struct device *dev, const struct sensor_trigger *trig) {
    sensor_sample_fetch(dev);         /* called from a thread, so I2C/SPI access is safe */
    ...
}
static struct sensor_trigger trig = { .type = SENSOR_TRIG_DATA_READY, .chan = SENSOR_CHAN_ALL };
sensor_trigger_set(accel, &trig, drdy_handler);
```
The handler runs in a thread whose stack is limited and defined by the driver, so keep it small. The driver
stores a pointer to the trigger rather than a copy, so the trigger must not live on the stack (hence `static`).
Enable the driver's trigger mode Kconfig (for example `CONFIG_LIS2DH_TRIGGER_OWN_THREAD` or
`CONFIG_LIS2DH_TRIGGER_GLOBAL_THREAD`) and wire the interrupt GPIO in devicetree as the driver's binding requires.

## Read and decode (newer, RTIO-based)
`CONFIG_SENSOR_ASYNC_API=y` (built on RTIO), `SENSOR_DT_READ_IODEV()` to define the read request, then
`sensor_read()` into a caller-provided buffer and decode with the driver's decoder (`sensor_get_decoder()`
and `sensor_decode()`), giving `q31_t` fixed-point vectors per channel. The guide calls these the forward-looking
APIs: they allow reads started from an interrupt handler or against several sensors at once, and
ping-pong buffering. Use it when the driver provides a decoder; fetch/get remains fine for slow polling.

## Gotchas
- `sensor_channel_get()` returns data from the driver's last fetch, so two gets without a new fetch return the
  same value.
- Driver not ready: wrong I2C address in DT or bus not enabled; `device_is_ready` catches it.
- `sensor_value_to_double` pulls in FP; use integer helpers (`sensor_value_to_milli`,
  `sensor_value_to_micro`) on FPU-less MCUs.

## Verify
- [ ] Units converted per channel docs (kPa vs Pa is the classic error).
- [ ] Return codes of fetch/get/attr checked.

## Checked

Checked 2026-10-26 against `include/zephyr/drivers/sensor.h`, the sensor read-and-decode guide and Kconfig files on Zephyr main:
`struct sensor_value` representation and negative examples, channel units (kPa, m/s^2, rad/s, G), `sensor_sample_fetch()` and
`sensor_sample_fetch_chan()` semantics, `sensor_channel_get()` behaviour and `_XYZ` array order, `sensor_attr_set()` and
`SENSOR_ATTR_*`, `sensor_trigger_set()` threading and no-stack-allocation rule (the example's local trigger was fixed to `static`),
`SENSOR_TRIG_DATA_READY`, `CONFIG_SENSOR_ASYNC_API`, `SENSOR_DT_READ_IODEV()`, `sensor_read()`, `sensor_get_decoder()`,
`sensor_value_to_double/milli/micro()` and the LIS2DH trigger options. Removed the unconfirmed system-workqueue remark.

Method: documentation only; no commands were run.
