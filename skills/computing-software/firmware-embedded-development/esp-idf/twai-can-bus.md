---
id: computing-software.firmware-embedded-development.esp-idf.twai-can-bus
name: twai-can-bus
category: computing-software
field: firmware-embedded-development
product: esp-idf
tags: [esp-peripherals, twai, can-bus, can-acceptance-filter, bus-off-recovery, esp-idf, firmware-embedded-development]
level: advanced
status: docs-checked
description: "Use the ESP-IDF node-based TWAI (CAN) driver: transceiver wiring, bit timing, mask filters, callbacks, error states and bus-off recovery for vehicle and industrial buses."
sources:
  - https://github.com/espressif/esp-idf/blob/master/docs/en/api-reference/peripherals/twai.rst
  - https://github.com/espressif/esp-idf/blob/master/components/esp_driver_twai/include/esp_twai.h
  - https://github.com/espressif/esp-idf/blob/master/components/driver/twai/include/driver/twai.h
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# TWAI (CAN)

TWAI is Espressif's CAN controller, compatible with the ISO 11898-1 frame structure. Chips with `SOC_TWAI_FD_SUPPORTED`
also handle CAN FD frames; on other chips FD frames are interpreted as errors. The chip has no internal transceiver:
use an external one matched to your physical layer (the guide cites TJA105x for ISO 11898-2) and terminate the bus
according to your bus standard. For single-node testing you can short TX to RX or use self-test mode.

The legacy `driver/twai.h` API (`twai_driver_install`, `twai_transmit`) is deprecated (its header warns "please use
esp_twai.h"). The current driver is node-based.

## Create a node
```c
#include "esp_twai.h"
#include "esp_twai_onchip.h"
twai_node_handle_t node = NULL;
twai_onchip_node_config_t nc = {
    .io_cfg.tx = 4, .io_cfg.rx = 5,
    .bit_timing.bitrate = 500000,
    .tx_queue_depth = 5,
};
ESP_ERROR_CHECK(twai_new_node_onchip(&nc, &node));
twai_event_callbacks_t cbs = { .on_rx_done = rx_cb, .on_state_change = state_cb, .on_error = err_cb };
ESP_ERROR_CHECK(twai_node_register_event_callbacks(node, &cbs, NULL));   /* before enabling */
ESP_ERROR_CHECK(twai_node_enable(node));
```
Useful config fields: `bit_timing.sp_permill` (sample point), `fail_retry_cnt` (-1 retry forever, 0 single shot),
`intr_priority` (0 to 3), and flags `enable_self_test` (no ACK check), `enable_loopback`, `enable_listen_only`,
`no_receive_rtr`.

## Send and receive
```c
uint8_t data[8] = {0};
twai_frame_t tx = { .header.id = 0x123, .buffer = data, .buffer_len = sizeof(data) };
ESP_ERROR_CHECK(twai_node_transmit(node, &tx, 0));          /* timeout 0: return at once if the queue is full */
ESP_ERROR_CHECK(twai_node_transmit_wait_all_done(node, -1));
```
The driver passes frames by pointer, so the frame and its buffer must stay valid until transmission completes (wait, or
use `on_tx_done`). Set `.header.ide = true` for a 29-bit identifier. Receiving happens in the `on_rx_done` callback:
set `buffer` and `buffer_len` on a `twai_frame_t` and call `twai_node_receive_from_isr(handle, &frame)`; hand the data
to a task.

## Acceptance filter
```c
twai_mask_filter_config_t f = { .id = 0x10, .mask = 0x7f0, .is_ext = false };   /* accepts 0x10..0x1f */
ESP_ERROR_CHECK(twai_node_config_mask_filter(node, 0, &f));
```
In this API a mask bit of 1 means the bit must match and 0 means ignore it; id and mask both 0 accepts everything. The
number of mask filters is chip dependent. A node that filters a frame out still sends the ACK.

## Errors and bus-off
Error counters move the node through error active (TEC and REC below 96), warning (96 or more), passive (128 or more)
and bus-off (TEC 256 or more). Use `twai_node_get_info`, `on_error` and `on_state_change`. In bus-off the node stays
offline until you call `twai_node_recover` from a task; recovery is not immediate and `on_state_change` fires when the
node returns to error active. Repeated bus-off points to wiring, termination, bit timing, or a lone node with no
ACKing peer (use `enable_self_test`).

## Verify
- [ ] A bus analyser shows frames with the right ID and DLC and no error frames.
- [ ] Unplug and replug the bus: the node recovers from bus-off (`twai_node_recover` called and state returns to active).
- [ ] No frames are lost at peak bus load (check receive handling keeps up).

## Checked

2026-10-26, against ESP-IDF master docs and headers (espressif/esp-idf, pushed 2026-10-24). Confirmed in peripherals/twai.rst, esp_twai.h and the legacy twai.h: node-based API (twai_new_node_onchip, twai_node_enable, twai_node_transmit, receive in on_rx_done, twai_node_config_mask_filter, twai_node_recover, twai_node_get_info), mask semantics (1 = must match), error states and thresholds, flags enable_self_test / enable_loopback / enable_listen_only, external transceiver requirement, CAN FD only on chips with SOC_TWAI_FD_SUPPORTED, legacy driver deprecation warning. Fixed: the skill taught the deprecated driver/twai.h API and its inverted filter-mask meaning; transceiver part numbers, 128 x 11 recovery wording and sample-point advice removed as unconfirmed.

Method: documentation only; no commands were run.
