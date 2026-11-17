---
id: computing-software.firmware-embedded-development.esp-idf.spi-master-driver
name: spi-master-driver
category: computing-software
field: firmware-embedded-development
product: esp-idf
tags: [esp-peripherals, esp-spi-master, spi-dma, spi-device-interface, spi-transaction, esp-idf, firmware-embedded-development]
level: practitioner
status: docs-checked
description: "Use the ESP-IDF SPI master driver: bus and device setup, DMA buffers, polling vs queued transactions, IOMUX pins for high clocks and multiple devices on one bus."
sources:
  - https://github.com/espressif/esp-idf/blob/master/docs/en/api-reference/peripherals/spi_master.rst
  - https://github.com/espressif/esp-idf/blob/master/components/esp_driver_spi/include/driver/spi_master.h
  - https://github.com/espressif/esp-idf/blob/master/components/esp_driver_spi/include/driver/spi_common.h
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# SPI master driver

## Bus and device
```c
spi_bus_config_t bus = { .mosi_io_num = 11, .miso_io_num = 13, .sclk_io_num = 12,
                         .quadwp_io_num = -1, .quadhd_io_num = -1, .max_transfer_sz = 4096 };
ESP_ERROR_CHECK(spi_bus_initialize(SPI2_HOST, &bus, SPI_DMA_CH_AUTO));

spi_device_interface_config_t dev = { .clock_speed_hz = 20 * 1000 * 1000, .mode = 0,
    .spics_io_num = 10, .queue_size = 4, .command_bits = 8, .address_bits = 0,
    .pre_cb = NULL };
spi_device_handle_t h;
ESP_ERROR_CHECK(spi_bus_add_device(SPI2_HOST, &dev, &h));
```
SPI1 is not a general-purpose SPI (the flash uses it; the driver supports it with many limitations); use the
GP-SPI hosts `SPI2_HOST` and `SPI3_HOST` where the chip has them.

## Transactions
```c
spi_transaction_t t = { .cmd = 0x9F, .length = 8 * 3 /* bits */, .rxlength = 8 * 3,
                        .flags = SPI_TRANS_USE_RXDATA };       /* up to 4 bytes in t.rx_data */
ESP_ERROR_CHECK(spi_device_polling_transmit(h, &t));            /* lowest latency, busy waits */
```
For large transfers queue several and do other work:
```c
spi_device_queue_trans(h, &t1, portMAX_DELAY);
spi_device_queue_trans(h, &t2, portMAX_DELAY);
spi_transaction_t *done; spi_device_get_trans_result(h, &done, portMAX_DELAY);
```
Wrap multi-transaction sequences with `spi_device_acquire_bus(h, portMAX_DELAY)` /
`spi_device_release_bus(h)` to keep other devices off the bus.

## DMA rules
- With DMA, buffers should be in DMA-capable internal memory (`heap_caps_malloc(n, MALLOC_CAP_DMA)`) and 32-bit aligned
  (start and length a multiple of 4 bytes); otherwise the driver allocates and copies temporary buffers, which costs
  efficiency. Chips with `SOC_PSRAM_DMA_CAPABLE` can DMA to PSRAM with the `SPI_TRANS_DMA_USE_PSRAM` flag.
- `max_transfer_sz` is the maximum transfer size in bytes (default 4092 with DMA when 0).

## Speed and pins
- The GPIO matrix adds MISO input delay and limits signals to 40 MHz versus 80 MHz on IO_MUX pins; if one signal
  uses the matrix all do. The `spi_master.h` note gives ESP32 sampling limits of about 80 MHz (IOMUX) and 26 MHz (GPIO
  matrix) for an ideal slave. Half-duplex transactions with dummy cycles can compensate: set `.input_delay_ns` correctly.
- Long wires: lower the clock or set `.input_delay_ns`.

## Several devices
Each `spi_bus_add_device` gets its own CS; the header says every host has three CS pins and can control up to three
devices. For more devices, drive extra CS lines yourself, for example in `pre_cb` / `post_cb`.

## Verify
- [ ] Logic analyser capture matches mode, bit order and CS timing of the device datasheet.
- [ ] Throughput measured; buffers are DMA-capable and aligned so the driver does not copy them.

## Checked

2026-10-26, against ESP-IDF master docs and headers (espressif/esp-idf, pushed 2026-10-24). Confirmed in peripherals/spi_master.rst, spi_master.h and spi_common.h: SPI1 note, buffer DMA and 32-bit alignment rules and the efficiency penalty, SPI_TRANS_DMA_USE_PSRAM on PSRAM-DMA chips, max_transfer_sz default, GPIO matrix versus IO_MUX limits, ESP32 26 MHz note, input_delay_ns, HALFDUPLEX flag, three CS pins per host, polling transmit and bus acquire/release. Fixed: non-DMA or unaligned buffers are copied (not rejected with ESP_ERR_INVALID_ARG), aligned-PSRAM claim replaced by the documented flag, the 6-CS claim removed.

Method: documentation only; no commands were run.
