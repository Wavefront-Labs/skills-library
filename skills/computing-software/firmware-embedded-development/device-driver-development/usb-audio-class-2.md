---
id: computing-software.firmware-embedded-development.device-driver-development.usb-audio-class-2
name: usb-audio-class-2
category: computing-software
field: firmware-embedded-development
product: device-driver-development
tags: [usb-audio, usb-device, uac2, isochronous, feedback-endpoint, firmware-embedded-development]
level: sme
status: draft
description: "Implement a USB Audio Class 2.0 device: clock source/terminal/feature unit topology, isochronous endpoints, asynchronous feedback, and keeping the I2S clock locked to the host."
sources:
  - https://www.usb.org/document-library/audio-devices-rev-20-and-adopters-agreement
  - https://learn.microsoft.com/en-us/windows-hardware/drivers/audio/usb-2-0-audio-drivers
  - https://docs.tinyusb.org/en/latest/reference/index.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# USB Audio Class 2

UAC2 is supported natively by macOS, Linux and Windows 10 1703+ (`usbaudio2.sys`). It needs a
High-Speed capable device for its full feature set (it also works at Full Speed with lower rates).

## Topology (speaker example)
Audio Control interface describes units:
```
Clock Source (internal, programmable 44.1/48/96 kHz)
   |
Input Terminal (USB streaming) -> Feature Unit (mute, volume) -> Output Terminal (speaker)
```
Each terminal references the clock source ID. Audio Streaming interface has **alternate setting
0 with no endpoints** (zero bandwidth) and alt 1+ with the isochronous endpoint and format
(`bSubslotSize` 2/3/4 bytes, `bBitResolution` 16/24/32). Host selects alt 1 when playback starts.
An IAD groups control + streaming interfaces.

## Isochronous data
At HS, one packet per microframe (125 us): 48 kHz stereo 24-bit (3-byte subslots) = 6 samples x
2 ch x 3 B = 36 B per microframe (bInterval = 1). Packet sizes vary when the rate doesn't divide
evenly (44.1 kHz: mostly 5 samples, sometimes 6).

## Synchronisation: the hard part
Host and device clocks differ slightly. Without correction, the device's buffer slowly underflows
or overflows (clicks every few seconds/minutes).
- **Asynchronous mode (recommended)**: device runs I2S from its own audio crystal/PLL and sends an
  **explicit feedback endpoint** (isochronous IN) reporting the actual rate in 16.16 format (HS)
  or 10.14 (FS) samples per (micro)frame. Compute from the buffer fill level or by counting I2S
  frames per SOF period (timer captured on SOF). The host adjusts packet sizes.
- **Adaptive mode**: device adjusts its clock (fractional PLL trim) to match incoming data rate.
- **Synchronous**: lock audio clock to SOF; rarely possible on MCUs.

## Control requests
UAC2 uses `CUR`/`RANGE` requests on entity IDs: clock source `SAM_FREQ_CONTROL` (sample rate,
range request returns supported rates), feature unit mute/volume (volume in 1/256 dB, range
min/max/res). Missing or wrong `RANGE` responses make Windows refuse the device.

## Practical
- Start from TinyUSB `uac2_headset`/`uac2_speaker_fb` examples or XMOS/ST reference designs.
- DMA I2S in circular mode with half/complete interrupts; ring buffer between USB and I2S targeting
  half full.
- Windows 10 UAC2 driver is picky about descriptors; test on all three OSes.

## Verify
- [ ] 1-hour playback with no buffer underrun/overrun (log fill level min/max).
- [ ] Feedback values track the actual rate (e.g. 48.0002 kHz) and fill level stays centred.
- [ ] Sample rate switching from the host OS works without re-enumeration.
