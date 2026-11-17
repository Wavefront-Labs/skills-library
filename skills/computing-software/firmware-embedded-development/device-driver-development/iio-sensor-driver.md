---
id: computing-software.firmware-embedded-development.device-driver-development.iio-sensor-driver
name: iio-sensor-driver
category: computing-software
field: firmware-embedded-development
product: device-driver-development
tags: [linux-driver-subsystem, iio-driver, iio-chan-spec, read-raw, iio-triggered-buffer, scale-offset, iio-sysfs, libiio, firmware-embedded-development]
level: advanced
status: docs-checked
description: "Expose ADCs, IMUs and environmental sensors through the Linux IIO subsystem: channel specs, read_raw with scale/offset, triggered buffers for streaming, and testing with iio tools."
sources:
  - https://docs.kernel.org/driver-api/iio/index.html
  - https://docs.kernel.org/driver-api/iio/buffers.html
  - https://docs.kernel.org/driver-api/iio/triggers.html
  - https://github.com/torvalds/linux/blob/master/Documentation/ABI/testing/sysfs-bus-iio
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# IIO sensor driver

**Goal:** a sensor driver whose data appears in standard sysfs files and buffered streams, so
user space can use it through sysfs and the IIO buffer interface without custom ioctls.

## Channels
```c
static const struct iio_chan_spec acme_channels[] = {
    { .type = IIO_TEMP,
      .info_mask_separate = BIT(IIO_CHAN_INFO_RAW) | BIT(IIO_CHAN_INFO_SCALE) | BIT(IIO_CHAN_INFO_OFFSET),
      .scan_index = 0,
      .scan_type = { .sign = 's', .realbits = 16, .storagebits = 16, .endianness = IIO_BE } },
    { .type = IIO_HUMIDITYRELATIVE,
      .info_mask_separate = BIT(IIO_CHAN_INFO_RAW) | BIT(IIO_CHAN_INFO_SCALE),
      .scan_index = 1,
      .scan_type = { .sign = 'u', .realbits = 16, .storagebits = 16, .endianness = IIO_BE } },
    IIO_CHAN_SOFT_TIMESTAMP(2),
};
```
Creates `in_temp_raw`, `in_temp_scale`, `in_temp_offset`, `in_humidityrelative_raw`, ...
under `/sys/bus/iio/devices/iio:deviceN/`.

## read_raw
```c
static int acme_read_raw(struct iio_dev *indio, struct iio_chan_spec const *ch,
                         int *val, int *val2, long mask) {
    struct acme *a = iio_priv(indio);
    switch (mask) {
    case IIO_CHAN_INFO_RAW:
        return acme_read_channel(a, ch->scan_index, val) ?: IIO_VAL_INT;
    case IIO_CHAN_INFO_SCALE:                /* processed = (raw + offset) * scale */
        *val = 2670; *val2 = 0;               /* illustrative value */
        return IIO_VAL_INT;
    case IIO_CHAN_INFO_OFFSET:
        *val = -16852; return IIO_VAL_INT;
    }
    return -EINVAL;
}
```
Units are fixed by the ABI (`Documentation/ABI/testing/sysfs-bus-iio`): temperature in
milli-degrees C, voltage in millivolts, acceleration in m/s^2, after applying scale/offset
(the offset is added to the raw value before scaling).
Use `IIO_VAL_INT_PLUS_MICRO` / `IIO_VAL_FRACTIONAL` for non-integer scales.

## Streaming: triggered buffer
```c
devm_iio_triggered_buffer_setup(dev, indio, iio_pollfunc_store_time, acme_trigger_handler, NULL);
static irqreturn_t acme_trigger_handler(int irq, void *p) {
    struct iio_poll_func *pf = p; struct iio_dev *indio = pf->indio_dev;
    struct { __be16 ch[2]; aligned_s64 ts; } scan = {};
    acme_read_all(iio_priv(indio), scan.ch);
    iio_push_to_buffers_with_ts(indio, &scan, sizeof(scan), pf->timestamp);
    iio_trigger_notify_done(indio->trig);
    return IRQ_HANDLED;
}
```
`iio_push_to_buffers_with_timestamp()` is marked deprecated in favour of `iio_push_to_buffers_with_ts()`,
which also checks the buffer size. A data-ready interrupt can be exposed as the device's own trigger;
otherwise triggers from a separate driver (timer, GPIO, or sysfs) drive sampling.

## Testing
```
cat /sys/bus/iio/devices/iio:device0/in_temp_raw
# buffered capture: enable channels under scan_elements/, write a trigger name to
# trigger/current_trigger, set buffer/length, then write 1 to buffer/enable
```

## Verify
- [ ] Processed values (raw + offset) x scale match a reference instrument in ABI units.
- [ ] Buffered capture at the target rate shows no gaps (timestamps evenly spaced).

## Checked

2026-10-27, Linux kernel (mainline v7.3).
Confirmed in include/linux/iio/buffer.h: iio_push_to_buffers_with_timestamp() is deprecated in favour of iio_push_to_buffers_with_ts(indio, data, data_total_len, timestamp). Confirmed in include/linux/iio/triggered_buffer.h: devm_iio_triggered_buffer_setup(dev, indio_dev, h, thread, setup_ops). Confirmed in iio.h and types.h: IIO_CHAN_SOFT_TIMESTAMP, IIO_DECLARE_BUFFER_WITH_TS, IIO_BE, IIO_VAL_INT_PLUS_MICRO, IIO_VAL_FRACTIONAL, IIO_CHAN_INFO_OFFSET. Confirmed in the ABI file: in_temp_raw, in_humidityrelative_raw, offset added before scaling, units of milli degrees Celsius, millivolts and m/s^2. Confirmed in buffers.rst and triggers.rst: buffer/length and buffer/enable, scan_elements, trigger/current_trigger. Replaced the deprecated push call. Removed the libiio command lines and the iio-sensor-proxy mention (not read) and the Analog Devices wiki source.

Method: documentation only; no commands were run.
