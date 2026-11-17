---
id: computing-software.firmware-embedded-development.device-driver-development.shared-spi-bus-arbitration
name: shared-spi-bus-arbitration
category: computing-software
field: firmware-embedded-development
product: device-driver-development
tags: [shared-spi-bus, spi, bus-locking, per-device-config, chip-select-discipline, firmware-embedded-development]
level: advanced
status: draft
description: "Share one SPI bus between several device drivers: per-device mode/clock reconfiguration, bus locking around whole transactions, CS discipline, and RTOS/ISR access rules."
sources:
  - https://docs.zephyrproject.org/latest/hardware/peripherals/spi.html
  - https://docs.espressif.com/projects/esp-idf/en/stable/esp32/api-reference/peripherals/spi_master.html
  - https://docs.kernel.org/spi/spi-summary.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Sharing one SPI bus between drivers

A flash chip, a display and an IMU on SPI1: each needs its own mode, clock and CS, and each
driver performs multi-transfer sequences (command, address, data) that must not interleave.

## Device descriptor + bus lock
```c
typedef struct {
    spi_bus_t *bus;
    gpio_t cs;
    uint32_t hz;
    uint8_t mode;          /* CPOL/CPHA */
    uint8_t bits;
} spi_dev_t;

void spi_acquire(spi_dev_t *d) {
    mutex_lock(&d->bus->lock);                  /* RTOS mutex; bare metal: ownership flag */
    if (d->bus->cfg_owner != d) {               /* reconfigure only on owner change */
        spi_disable(d->bus);
        spi_set(d->bus, d->hz, d->mode, d->bits);
        d->bus->cfg_owner = d;
    }
    gpio_clear(d->cs);
}
void spi_release(spi_dev_t *d) {
    spi_wait_idle(d->bus);                      /* BSY = 0: last bit out before CS high */
    gpio_set(d->cs);
    mutex_unlock(&d->bus->lock);
}
```
A flash read becomes: `acquire; xfer(cmd+addr); xfer(data); release;`. The lock covers the
whole transaction, not each byte transfer.

## Rules
- **Change mode only with the peripheral disabled** and CS high; changing CPOL while enabled
  glitches SCK and some devices see an extra clock.
- **All CS lines idle high at boot**, before the first transaction on any device (external
  pull-ups help during reset). One floating CS corrupts traffic for every other device.
- **Wait for BSY=0** before raising CS; TXE only means the data register is empty.
- **No bus access from ISRs** if tasks also use the bus: an ISR can't wait on a mutex. Defer to a
  task, or give the ISR-driven device its own bus.
- **Long transfers** (display frame) starve other devices: chunk them and release between chunks
  if latency for the IMU matters, or prioritise with separate buses.
- **SD cards in SPI mode** need 74+ clocks with CS high at init and may drive MISO when not
  selected until initialised; put them on their own bus if possible.

## Frameworks that do this already
Zephyr `spi_transceive_dt()` with `spi_dt_spec` (per-device config, `SPI_LOCK_ON` for
multi-transfer holds); ESP-IDF `spi_bus_add_device()` + `spi_device_acquire_bus()`; Linux
`spi_sync()` with `spi_message` containing several `spi_transfer`s (`cs_change`).

## Verify
- [ ] Logic analyser on all CS lines: never two low at once; each CS frame contains one complete transaction.
- [ ] Stress test with all drivers active in parallel tasks: no corrupted reads.
