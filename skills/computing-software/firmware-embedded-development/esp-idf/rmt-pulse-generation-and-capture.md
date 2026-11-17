---
id: computing-software.firmware-embedded-development.esp-idf.rmt-pulse-generation-and-capture
name: rmt-pulse-generation-and-capture
category: computing-software
field: firmware-embedded-development
product: esp-idf
tags: [esp-peripherals, rmt, rmt-encoder, ws2812, ir-remote, rmt-rx, led-strip, esp-idf, firmware-embedded-development]
level: advanced
status: docs-checked
description: "Generate and capture precisely timed pulse trains with the ESP-IDF RMT driver (v5 API): channels, encoders, WS2812 LEDs, IR receive, and avoiding glitches under Wi-Fi load."
sources:
  - https://github.com/espressif/esp-idf/blob/master/docs/en/api-reference/peripherals/rmt.rst
  - https://github.com/espressif/esp-idf/blob/master/components/esp_driver_rmt/include/driver/rmt_tx.h
  - https://github.com/espressif/esp-idf/blob/master/components/esp_driver_rmt/include/driver/rmt_rx.h
  - https://github.com/espressif/esp-idf/blob/master/examples/peripherals/rmt/led_strip/main/led_strip_encoder.c
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# RMT pulse generation and capture

RMT (remote control transceiver) turns a list of `{level, duration}` symbols into a waveform
with tick-level precision, and the reverse on receive. It's the right tool for WS2812/SK6812
LEDs, IR remotes, one-wire-style protocols, and stepper pulses.

## TX channel
```c
#include "driver/rmt_tx.h"
rmt_channel_handle_t tx;
rmt_tx_channel_config_t tc = {
    .gpio_num = GPIO_NUM_18,
    .clk_src = RMT_CLK_SRC_DEFAULT,
    .resolution_hz = 10 * 1000 * 1000,     /* 1 tick = 100 ns */
    .mem_block_symbols = 64,
    .trans_queue_depth = 4,
};
ESP_ERROR_CHECK(rmt_new_tx_channel(&tc, &tx));
```

## Encoder: bytes to WS2812 symbols
```c
rmt_encoder_handle_t enc;
rmt_bytes_encoder_config_t bc = {
    .bit0 = { .level0 = 1, .duration0 = 3, .level1 = 0, .duration1 = 9 },  /* 0.3 us H, 0.9 us L */
    .bit1 = { .level0 = 1, .duration0 = 9, .level1 = 0, .duration1 = 3 },  /* 0.9 us H, 0.3 us L */
    .flags.msb_first = 1,
};
ESP_ERROR_CHECK(rmt_new_bytes_encoder(&bc, &enc));
ESP_ERROR_CHECK(rmt_enable(tx));

uint8_t grb[3 * NUM_LEDS];
rmt_transmit_config_t xc = { .loop_count = 0 };
ESP_ERROR_CHECK(rmt_transmit(tx, enc, grb, sizeof(grb), &xc));
rmt_tx_wait_all_done(tx, portMAX_DELAY);
```
WS2812-style LEDs also need a low reset period after the data (check the LED datasheet); the IDF `led_strip`
example appends it with a copy encoder (`reset_code`). The bit timings above are the example's T0H 0.3 us / T0L 0.9 us
and T1H 0.9 us / T1L 0.3 us.
Other encoders: `rmt_new_copy_encoder` (raw symbols) or a custom encoder combining both (IR NEC).

## RX channel
```c
#include "driver/rmt_rx.h"
rmt_rx_channel_config_t rc = { .gpio_num = GPIO_NUM_19, .clk_src = RMT_CLK_SRC_DEFAULT,
                               .resolution_hz = 1000000, .mem_block_symbols = 64 };
rmt_new_rx_channel(&rc, &rx);
rmt_rx_event_callbacks_t cbs = { .on_recv_done = rx_done_cb };   /* ISR context: queue it */
rmt_rx_register_event_callbacks(rx, &cbs, queue);
rmt_enable(rx);
rmt_receive_config_t rcv = { .signal_range_min_ns = 1250,      /* shorter = glitch, ignored */
                             .signal_range_max_ns = 12000000 }; /* longer idle = frame end */
rmt_receive(rx, symbols, sizeof(symbols), &rcv);                /* re-arm after each frame */
```

## Glitches under load
Long frames exceed the channel's symbol memory, so the driver refills it from an interrupt; a delayed refill
can show up as flickering LEDs. Options from the guide and Kconfig: the DMA backend (`.flags.with_dma = 1`, not
available on all chips: `ESP_ERR_NOT_SUPPORTED` otherwise), a larger `mem_block_symbols` (with DMA it sets the DMA
buffer size), `.intr_priority`, and the RMT IRAM and cache-safe options (`CONFIG_RMT_TX_ISR_HANDLER_IN_IRAM`,
`CONFIG_RMT_ISR_IRAM_SAFE`, `CONFIG_RMT_ENCODER_FUNC_IN_IRAM`).

## Verify
- [ ] Logic analyser shows bit timing within the device's datasheet tolerance.
- [ ] No flicker or decode errors while Wi-Fi throughput test runs.
- [ ] RX re-armed after every frame; min/max ranges reject noise.

## Checked

2026-10-26, against ESP-IDF master docs and headers (espressif/esp-idf, pushed 2026-10-24). Confirmed in peripherals/rmt.rst, rmt_tx.h / rmt_rx.h / rmt_encoder.h, the driver Kconfig and the IDF rmt led_strip_encoder example: TX and RX channel config fields (mem_block_symbols, trans_queue_depth, with_dma, intr_priority), bytes encoder with msb_first, copy encoder, WS2812 bit timings, receive config signal_range_min_ns / signal_range_max_ns and re-arming rmt_receive after each frame, on_recv_done callback, Kconfig option names. Removed the unconfirmed 50 us reset figure, the +-150 ns tolerance and the claim that a larger memory block borrows other channels' memory.

Method: documentation only; no commands were run.
