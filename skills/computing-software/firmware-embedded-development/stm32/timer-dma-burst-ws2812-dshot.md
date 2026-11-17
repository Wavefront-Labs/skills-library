---
id: computing-software.firmware-embedded-development.stm32.timer-dma-burst-ws2812-dshot
name: timer-dma-burst-ws2812-dshot
category: computing-software
field: firmware-embedded-development
product: stm32
tags: [stm32-timers, timer-dma-burst, ws2812, dshot, pwm-dma, dmar-dcr, stm32, firmware-embedded-development]
level: advanced
status: draft
description: "Drive WS2812 LEDs and DShot ESC protocols from STM32 timers by streaming CCR values with DMA, including timing math, buffer layout, DMA burst (DCR/DMAR) and reset gaps."
sources:
  - https://www.st.com/resource/en/application_note/an4776-generalpurpose-timer-cookbook-for-stm32-microcontrollers-stmicroelectronics.pdf
  - https://www.st.com/resource/en/reference_manual/rm0090-stm32f405415-stm32f407417-stm32f427437-and-stm32f429439-advanced-armbased-32bit-mcus-stmicroelectronics.pdf
  - https://cdn-shop.adafruit.com/datasheets/WS2812B.pdf
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Timer DMA burst (WS2812 and DShot)

Both protocols encode bits as pulse widths in a fixed bit period. A timer in PWM mode with DMA
writing a new CCR value at each update event generates them with no CPU load.

## WS2812 timing
800 kHz bit rate (1.25 us). With an 84 MHz timer clock: ARR = 104. Duty for "0" about 0.4 us
(CCR = 34), "1" about 0.8 us (CCR = 67). Reset/latch: low for > 50 us (newer parts > 280 us):
append 50-300 zero entries (CCR = 0) or stop the timer for that long.

## Buffer
One entry per bit, 24 bits per LED (GRB order, MSB first):
```c
#define LEDS 60
static uint16_t buf[LEDS * 24 + 64];     /* +64 zeros for reset; uint32_t for 32-bit timers' CCR */
void ws_set(int i, uint8_t r, uint8_t g, uint8_t b) {
    uint32_t c = (g << 16) | (r << 8) | b;
    for (int k = 0; k < 24; k++) buf[i * 24 + k] = (c & (1u << (23 - k))) ? 67 : 34;
}
HAL_TIM_PWM_Start_DMA(&htim3, TIM_CHANNEL_1, (uint32_t *)buf, sizeof buf / sizeof buf[0]);
```
DMA: memory-to-peripheral, half-word both sides (word if CCR is accessed as 32-bit with
matching data size), normal mode, triggered by TIMx_UP or TIMx_CHy. Stop the PWM in
`HAL_TIM_PWM_PulseFinishedCallback`.

RAM: 2 bytes per bit (48 bytes per LED). For long strips use a circular DMA with a 2-LED
ping-pong buffer refilled in half/complete callbacks.

## DShot (ESC)
DShot600: bit period 1.67 us, "1" = 75% duty, "0" = 37.5%. Frame: 11-bit throttle, 1 telemetry
bit, 4-bit CRC (XOR of nibbles), 16 bits total, then a short gap. Same DMA technique; for 4 motors
on one timer, use **DMA burst**: `TIMx->DCR` = (DBA = offset of CCR1, DBL = 4 transfers) and the
DMA writes to `TIMx->DMAR`, updating CCR1-4 at each update event from an interleaved buffer.
HAL: `HAL_TIM_DMABurst_MultiWriteStart`.

## Pitfalls
- CCR preload must be enabled (OCxPE=1) so each value takes effect at the next period, not mid-period.
- First bit glitch: preload CCR with the first value or start with a zero entry.
- 3.3 V data into a 5 V WS2812: marginal; use a level shifter (74AHCT125) or open-drain with pull-up on an FT pin.
- On H7, DMA buffers must not be in DTCM and need cache maintenance.

## Verify
- [ ] Logic analyser shows correct T0H/T1H and period within datasheet tolerance.
- [ ] Full strip updates without flicker at target frame rate.
