---
id: energy-mining-utilities.amateur-radio.software-defined-radio.sdr-receiver-setup-gain-and-reading-the-waterfall
name: sdr-receiver-setup-gain-and-reading-the-waterfall
category: energy-mining-utilities
field: amateur-radio
product: software-defined-radio
tags: [software-defined-radio, sdr, rtl-sdr, rtl-sdr-blog, airspy, sdrplay, hackrf, sdr-plus-plus, sdrpp, sdrsharp, sdr-sharp, gqrx, sdrangel, hdsdr, zadig, winusb, sample-rate, rf-gain, agc, overload, dc-spike, image, ppm-correction, tcxo, bias-tee, lna, fm-bandstop-filter, waterfall, panadapter, signal-identification, sigidwiki, adsb, dump1090, aprs, airband, websdr, kiwisdr]
level: intro
status: draft
description: "Set up a USB SDR receiver properly: drivers, sample rate, gain set just below overload, PPM correction, filters and bias-tee, then identify signals on the waterfall by width, shape and band."
sources:
  - "RTL-SDR Blog quick-start guides, SDR++/GQRX/SDR# documentation and the Signal Identification Wiki, paraphrased"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# SDR receiver setup, gain and reading the waterfall

**Goal:** turn a cheap USB software-defined radio into a receiver that shows real
signals rather than overload junk, and learn to recognise what you're looking at.
Examples use an RTL-SDR-type dongle with SDR++, SDR# or GQRX; Airspy, SDRplay and
HackRF behave similarly with more range or dynamic range.

## 1. Drivers and software
- **Windows:** RTL-SDR dongles need the WinUSB driver installed with **Zadig**
  (select "Bulk-In, Interface 0" — **not** your keyboard or another device).
  SDRplay and Airspy have their own installers.
- **Linux:** install `rtl-sdr` packages; blacklist the DVB-T kernel module
  (`dvb_usb_rtl28xxu`) so it doesn't grab the device.
- Pick one application to learn first: **SDR++** (cross-platform), **SDR#** (Windows),
  **GQRX** (Linux/macOS).

## 2. Sample rate
The sample rate sets how much spectrum you see at once. An RTL-SDR is stable up to
about **2.4 MS/s** (≈2.4 MHz wide); higher rates may drop samples on some machines. A
narrower rate uses less CPU and can lower the noise floor slightly.

## 3. Gain — the key adjustment
Too much gain creates **overload**: the noise floor jumps up, phantom copies of strong
signals (intermod, images) appear everywhere, and weak signals vanish.
1. Turn AGC off; start with gain low.
2. Raise gain step by step and watch the **noise floor and the signal of interest**.
3. Stop when the noise floor starts rising faster than the signal (or rises
   noticeably). That's your setting **for this band and this location**; it changes
   between bands.
4. Near strong FM broadcast, pager or cellular transmitters, add an **FM band-stop
   filter** or a band-pass filter for your target band. Filtering often helps more
   than a bigger antenna.

## 4. Other settings
- **DC spike:** a spike at the exact centre is normal with these receivers; offset-
  tune so your signal isn't on it.
- **PPM correction:** cheap crystals drift (older dongles by tens of ppm); modern
  dongles with a TCXO are close to 0–1 ppm. Tune a known signal (an NOAA weather radio,
  a broadcast station's carrier) and adjust PPM until it sits on frequency.
- **Bias-tee** powers an external LNA or active antenna through the coax — turn it on
  **only** when that device needs it; it can damage some passive equipment or a short.
- **HF:** some dongles (e.g. RTL-SDR Blog V4) cover HF directly; older ones need
  direct-sampling mode or an upconverter. A long wire outdoors beats any indoor
  antenna, and indoor HF noise (switching supplies, LEDs) is often the limit.

## 5. Reading the waterfall
Time scrolls down; frequency left to right; colour = strength. Identify by **width,
shape and band**:
- **Wideband FM broadcast:** ~200 kHz wide blocks in 88–108 MHz.
- **Narrow FM voice** (repeaters, PMR): ~10–12.5 kHz bursts that come and go.
- **AM airband** (118–137 MHz): a carrier with sidebands; tune in AM mode.
- **SSB voice:** irregular shapes with no carrier, one-sided.
- **CW:** thin dashed lines. **FT8:** many tiny blocks in a 3 kHz slice, starting
  together every 15 seconds.
- **Digital data** (pagers, APRS, ADS-B at 1090 MHz) as regular bursts or blocks; ADS-B
  needs a decoder like dump1090 rather than audio.
- Use the **Signal Identification Wiki** (sigidwiki.com) to match audio and
  waterfall appearance to known signals.

## 6. Law and ethics
Receiving rules differ by country: some forbid listening to certain services
(cellular, some public-safety or encrypted traffic) or disclosing what you hear.
Check your local law. Transmitting needs a licence for that band; HackRF-type
transceivers make it easy to transmit illegally.

## Verify
- [ ] Driver installed on the correct device; software sees the SDR.
- [ ] Sample rate stable with no dropped samples.
- [ ] Gain set just below where the noise floor rises; no phantom signals.
- [ ] Frequency accuracy checked against a known signal (PPM).
- [ ] You can identify FM broadcast, NFM, AM, SSB, CW and FT8 by eye.
