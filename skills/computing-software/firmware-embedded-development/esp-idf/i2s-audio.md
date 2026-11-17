---
id: computing-software.firmware-embedded-development.esp-idf.i2s-audio
name: i2s-audio
category: computing-software
field: firmware-embedded-development
product: esp-idf
tags: [esp-peripherals, i2s, i2s-std, i2s-pdm, i2s-tdm, audio-dma, esp-idf, firmware-embedded-development]
level: practitioner
status: docs-checked
description: "Stream audio with the ESP-IDF v5 I2S driver: standard Philips mode for DACs/amps and MEMS mics, PDM and TDM, DMA buffer sizing, MCLK and underrun handling."
sources:
  - https://docs.espressif.com/projects/esp-idf/en/stable/esp32/api-reference/peripherals/i2s.html
  - https://github.com/espressif/esp-idf/tree/v6.1/components/esp_driver_i2s/include/driver
  - https://github.com/espressif/esp-idf/tree/master/examples/peripherals/i2s
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# I2S audio

## Standard mode TX (MAX98357A, PCM5102)
```c
#include "driver/i2s_std.h"
i2s_chan_handle_t tx;
i2s_chan_config_t cc = I2S_CHANNEL_DEFAULT_CONFIG(I2S_NUM_0, I2S_ROLE_MASTER);
cc.dma_desc_num = 6; cc.dma_frame_num = 240;              /* 6 x 5 ms at 48 kHz */
ESP_ERROR_CHECK(i2s_new_channel(&cc, &tx, NULL));
i2s_std_config_t sc = {
    .clk_cfg = I2S_STD_CLK_DEFAULT_CONFIG(48000),
    .slot_cfg = I2S_STD_PHILIPS_SLOT_DEFAULT_CONFIG(I2S_DATA_BIT_WIDTH_16BIT, I2S_SLOT_MODE_STEREO),
    .gpio_cfg = { .mclk = I2S_GPIO_UNUSED, .bclk = 26, .ws = 25, .dout = 22, .din = I2S_GPIO_UNUSED },
};
ESP_ERROR_CHECK(i2s_channel_init_std_mode(tx, &sc));
ESP_ERROR_CHECK(i2s_channel_enable(tx));
size_t w; i2s_channel_write(tx, pcm, bytes, &w, 1000);   /* last argument is a timeout in milliseconds */
```

## MEMS mic RX (example: 32-bit slot, mono)
```c
i2s_std_config_t rc = {
    .clk_cfg = I2S_STD_CLK_DEFAULT_CONFIG(16000),
    .slot_cfg = I2S_STD_PHILIPS_SLOT_DEFAULT_CONFIG(I2S_DATA_BIT_WIDTH_32BIT, I2S_SLOT_MODE_MONO),
    .gpio_cfg = { .bclk = 14, .ws = 15, .din = 32, .dout = I2S_GPIO_UNUSED, .mclk = I2S_GPIO_UNUSED } };
rc.slot_cfg.slot_mask = I2S_STD_SLOT_LEFT;       /* match the mic's L/R pin */
```
How the mic's sample bits sit inside the 32-bit slot, and which channel it drives, comes from its datasheet; scale or shift the samples to match.

## Other modes
- PDM RX for PDM microphones and PDM TX (`driver/i2s_pdm.h`). Which I2S ports support PDM, and which have the PCM-to-PDM or PDM-to-PCM converter (I2S0 on the chips listed), is in the per-target table of the I2S docs; without a converter the port only reads or writes raw PDM.
- TDM (`driver/i2s_tdm.h`) for multi-slot codecs: up to 16 slots selected with `slot_mask`, limited by slot width (4 slots at 32-bit, 8 at 16-bit, 16 at 8-bit). The ESP32 and ESP32-S2 have no TDM.
- Codecs needing MCLK: set `.mclk` and `clk_cfg.mclk_multiple` (`I2S_MCLK_MULTIPLE_256` is enough in most cases). On ESP32 the MCLK pin must be GPIO0, GPIO1 or GPIO3.

## Buffering
Latency = `dma_desc_num x dma_frame_num / fs`. With `auto_clear_after_cb` (alias `auto_clear`) or
`auto_clear_before_cb` set in the channel config, the TX channel sends zeros when no data is queued.
`on_sent` and `on_send_q_ovf` (TX) and `on_recv` and `on_recv_q_ovf` (RX) are registered through
`i2s_channel_register_event_callback`; the overflow callbacks report buffer data that was overwritten.
Keep a ring buffer between the decoder and I2S and feed it from a task with enough priority.

## Pitfalls
- Wrong bit width/slot mask gives loud noise or half-rate audio.
- `I2S_CLK_SRC_APLL` (chips with an audio PLL) is configurable per sample rate and so more precise at high rates, but if EMAC or another channel already holds the APLL its frequency cannot change and clock configuration can fail.

## Verify
- [ ] 1 kHz sine plays clean (scope/analyser, no glitches at buffer boundaries).
- [ ] Mic capture spectrum shows signal at the right sample rate.

## Checked

Checked against ESP-IDF v6.1 (docs/en/api-reference/peripherals/i2s.rst and components/esp_driver_i2s/include/driver/i2s_common.h, i2s_std.h, i2s_pdm.h).
Confirmed: `I2S_CHANNEL_DEFAULT_CONFIG` (dma_desc_num 6, dma_frame_num 240), `I2S_STD_CLK_DEFAULT_CONFIG`, `I2S_STD_PHILIPS_SLOT_DEFAULT_CONFIG`, `i2s_channel_init_std_mode`, `i2s_channel_write(..., timeout_ms)`, `I2S_GPIO_UNUSED`, GPIO config fields mclk/bclk/ws/dout/din, `slot_mask` with `I2S_STD_SLOT_LEFT`, `auto_clear`/`auto_clear_after_cb`/`auto_clear_before_cb`, callback names on_sent/on_send_q_ovf/on_recv/on_recv_q_ovf, `mclk_multiple` default 256, ESP32 MCLK pins GPIO0/1/3, TDM slot limits, per-target PDM/TDM table, APLL description. Removed unconfirmed claims: the INMP441 24-bit shift of 8 or 14 and its datasheet details, the ES7210/ES8388/WM8960 codec names, the 384x multiple, the claim that default PLL gives a small rate error and the PSRAM DMA remark.

Method: documentation only; no commands were run.
