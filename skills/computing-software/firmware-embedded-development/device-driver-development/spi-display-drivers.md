---
id: computing-software.firmware-embedded-development.device-driver-development.spi-display-drivers
name: spi-display-drivers
category: computing-software
field: firmware-embedded-development
product: device-driver-development
tags: [spi-display, spi, st7789, ili9341, dc-pin, partial-update, firmware-embedded-development]
level: advanced
status: draft
description: "Drive SPI TFT/OLED controllers (ST7789, ILI9341, SSD1306): D/C pin, init sequences, address windows, RGB565 byte order, DMA line buffers, and tearing control."
sources:
  - https://www.rhydolabz.com/documents/33/ST7789.pdf
  - https://cdn-shop.adafruit.com/datasheets/ILI9341.pdf
  - https://docs.lvgl.io/master/porting/display.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# SPI display drivers

## Command/data protocol
Most small TFT controllers use 4-wire SPI: SCK, MOSI, CS and **D/C** (data/command). D/C low =
the byte is a command, high = parameters/pixel data. D/C must be stable before the last bit of
each byte; with DMA, change D/C only after `BSY=0`.

## Init sequence (ST7789 240x240 example)
```c
cmd(0x01); delay_ms(150);                 /* SWRESET */
cmd(0x11); delay_ms(120);                 /* SLPOUT: wait before next command */
cmd(0x3A); data(0x55);                    /* COLMOD: 16-bit RGB565 */
cmd(0x36); data(0x00);                    /* MADCTL: orientation, RGB/BGR order */
cmd(0x21);                                /* INVON: many ST7789 panels need inversion on */
cmd(0x13); cmd(0x29);                     /* NORON, DISPON */
```
Vendor modules differ (gamma, voltage, panel offsets). Start from the module maker's sequence.

## Drawing: address window + memory write
```c
void set_window(uint16_t x0, uint16_t y0, uint16_t x1, uint16_t y1) {
    cmd(0x2A); data16(x0 + X_OFS); data16(x1 + X_OFS);   /* CASET */
    cmd(0x2B); data16(y0 + Y_OFS); data16(y1 + Y_OFS);   /* RASET */
    cmd(0x2C);                                           /* RAMWR: pixel data follows */
}
```
240x240 panels on a 240x320 controller need offsets (e.g. Y_OFS = 80 in some rotations).

## Pixel format
RGB565 is sent **MSB first** on the wire. Little-endian MCUs store `uint16_t` LSB first, so
either swap bytes (`__REV16`) when filling buffers, set the SPI to 16-bit frames (byte order then
handled by the peripheral), or use LVGL's `LV_COLOR_16_SWAP`.

## Throughput
240x240x2 bytes = 115 KB per frame; at 40 MHz SPI that is 23 ms (43 fps max). Use DMA with two
line buffers (ping-pong: render one while the other transfers) and **partial updates** of dirty
rectangles only. GUI libraries (LVGL, emWin) call a `flush_cb(area, buf)` you implement with
`set_window` + DMA, then call `lv_display_flush_ready()` in the DMA-complete interrupt.

## Tearing
If the panel exposes TE (tearing effect) output, enable it (`cmd(0x35)`) and start frame writes on
the TE edge so the write pointer stays ahead of the scan.

## Monochrome OLED (SSD1306)
Page-addressed (8 vertical pixels per byte); keep a 1 KB framebuffer for 128x64 and send whole
pages. I2C versions use a control byte (0x00 command, 0x40 data) instead of D/C.

## Verify
- [ ] Colour test pattern: red, green, blue bars appear in the right order (MADCTL BGR bit, byte swap).
- [ ] Measured frame time vs calculated; no tearing on fast animations with TE enabled.
