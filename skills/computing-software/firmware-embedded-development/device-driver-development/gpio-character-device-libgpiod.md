---
id: computing-software.firmware-embedded-development.device-driver-development.gpio-character-device-libgpiod
name: gpio-character-device-libgpiod
category: computing-software
field: firmware-embedded-development
product: device-driver-development
tags: [linux-driver-subsystem, libgpiod, gpio-cdev, gpioset, gpiomon, line-request, edge-events, gpio-line-names, sysfs-gpio-deprecated, firmware-embedded-development]
level: practitioner
status: docs-checked
description: "Control GPIOs from Linux user space with the GPIO character device and libgpiod v2 (gpioset/gpioget/gpiomon, C/Python API), naming lines in DT, and replacing deprecated sysfs GPIO."
sources:
  - https://docs.kernel.org/userspace-api/gpio/chardev.html
  - https://docs.kernel.org/userspace-api/gpio/sysfs.html
  - https://github.com/brgl/libgpiod
  - https://github.com/torvalds/linux/blob/master/Documentation/devicetree/bindings/gpio/gpio.txt
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# GPIO character device and libgpiod

**Goal:** user-space GPIO access on embedded Linux that is race-free, supports edge events with
timestamps, and doesn't depend on the deprecated `/sys/class/gpio` interface.

## Why not sysfs GPIO
`/sys/class/gpio/export` is obsolete (`CONFIG_GPIO_SYSFS`): the kernel documentation says new
developments should use the character device and that the sysfs API will be removed in the future.
The character device (`/dev/gpiochipN`) releases requested lines when the process exits and supports
bias, drive, debounce and active-low flags and edge events with timestamps.

## Name the lines in devicetree
```dts
&gpio2 {
    gpio-line-names = "", "", "RELAY_EN", "BTN_USER", "", "LED_STATUS";
};
```
Then tools and code can refer to lines by name rather than chip/offset.

## Command-line tools (libgpiod v2)
```
gpiodetect                                 # list chips
gpioinfo                                   # all lines with names, direction, consumers
gpioget --bias=pull-up BTN_USER
gpioset -z RELAY_EN=1                     # v2: hold the line, daemonised; kill to release
gpiomon --edges=falling --debounce-period=10ms BTN_USER
```
In libgpiod v2, `gpioset` holds the line while the process runs (by default it does not exit); do not
assume a line keeps its state after the process exits, because released lines can be changed by the
kernel or another process. Daemonise (`-z`) or use the API for persistent outputs.

## C API (v2)
```c
struct gpiod_chip *chip = gpiod_chip_open("/dev/gpiochip2");
struct gpiod_line_settings *s = gpiod_line_settings_new();
gpiod_line_settings_set_direction(s, GPIOD_LINE_DIRECTION_OUTPUT);
gpiod_line_settings_set_output_value(s, GPIOD_LINE_VALUE_INACTIVE);
struct gpiod_line_config *lc = gpiod_line_config_new();
unsigned int off = 2;
gpiod_line_config_add_line_settings(lc, &off, 1, s);
struct gpiod_request_config *rc = gpiod_request_config_new();
gpiod_request_config_set_consumer(rc, "relayd");
struct gpiod_line_request *req = gpiod_chip_request_lines(chip, rc, lc);
gpiod_line_request_set_value(req, 2, GPIOD_LINE_VALUE_ACTIVE);
```
Python bindings (`gpiod` package v2) mirror this with `gpiod.request_lines(...)`.

## Kernel-side alternative
If a GPIO belongs to a device with a kernel driver (LED, button, regulator enable), describe it
in DT (`gpio-leds`, `gpio-keys`) and use the standard interfaces (LED class, input events)
instead of user-space GPIO.

## Gotchas
- `Device or resource busy`: the line is claimed by a kernel driver or another process (check
  `gpioinfo` consumer column).
- Active-low handling: call `gpiod_line_settings_set_active_low()` (or `gpioset -l`) so logical values match meaning.

## Verify
- [ ] `gpioinfo` shows named lines and your consumer label while running.
- [ ] Edge events timestamps (`gpiomon`) correlate with a scope capture.

## Checked

2026-10-27, Linux kernel documentation (mainline v7.3) and libgpiod master.
Confirmed in Documentation/userspace-api/gpio/sysfs.rst: the sysfs API is obsolete and will be removed. Confirmed in drivers/gpio/Kconfig: GPIO_SYSFS option. Confirmed in libgpiod tools source: gpioset -z/--daemonize, default of not exiting and the note about lines not keeping state, -l/--active-low, gpiomon --edges and -p/--debounce-period with ms units, gpioget --bias. Confirmed in include/gpiod.h: gpiod_chip_open, gpiod_line_settings_new/set_direction/set_output_value/set_active_low, gpiod_line_config_new/add_line_settings, gpiod_request_config_new/set_consumer, gpiod_chip_request_lines, gpiod_line_request_set_value, GPIOD_LINE_VALUE_ACTIVE. Confirmed in the Python bindings: gpiod.request_lines. Corrected the active-low call, which was written as a settings constant. Removed the claims about changing global numbers, lines left exported after a crash and racy edge handling, and the v1 tool behaviour.

Method: documentation only; no commands were run.
