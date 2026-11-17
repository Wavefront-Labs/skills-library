---
id: energy-mining-utilities.amateur-radio.digital-mode-software.setting-up-wsjt-x-for-ft8-cat-audio-levels-and-time-sync
name: setting-up-wsjt-x-for-ft8-cat-audio-levels-and-time-sync
category: energy-mining-utilities
field: amateur-radio
product: digital-mode-software
tags: [digital-mode-software, wsjt-x, wsjtx, ft8, ft4, fldigi, digital-modes, amateur-radio, ham-radio, cat-control, hamlib, rig-control, ptt, vox, usb-audio-codec, sound-card, audio-levels, alc, overdrive, split-operation, fake-it, time-sync, ntp, chrony, meinberg, dt, 14074, waterfall, jtalert, gridtracker, adif, udp-logging, fox-hound]
level: intro
status: gated
description: "Get WSJT-X working cleanly for FT8/FT4: CAT and PTT via Hamlib, accurate PC clock, receive level near 30 dB, transmit with zero ALC, split mode for a clean signal, and logging hand-off."
sources:
  - "https://wsjt.sourceforge.io/wsjtx-doc/wsjtx-main-2.7.0.html"
  - "https://www.ecfr.gov/current/title-47/part-97/section-97.109"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Setting up WSJT-X for FT8: CAT, audio levels and time sync

**Goal:** decode lots of stations and transmit a clean, narrow signal. Most FT8
problems are one of three things: **clock off**, **audio overdriven (ALC)**, or
**CAT/PTT misconfigured**. fldigi (for RTTY, PSK31 and others) uses the same rig
interface ideas; its menus differ.

## 1. Connect the radio
- Modern rigs often have a single USB cable providing both a serial CAT port and a USB
  sound card ("USB Audio CODEC"). Install the manufacturer's USB driver first.
- Older rigs need an interface (e.g. SignaLink-style) for audio, and a CAT cable.
- In the radio's menus: **USB (upper sideband) data mode**, data input from USB (not
  mic), widest receive filter, compression/processor off, noise reduction off.

## 2. WSJT-X Settings → Radio
- **Rig:** choose your model from the Hamlib list; **serial port** (the CAT COM port)
  and **baud rate** must match the radio's menu setting.
- **PTT method:** CAT is simplest if supported; otherwise RTS/DTR on a serial
  line, or VOX as a last resort.
- **Mode:** Data/Pkt (or USB if the rig has no data mode).
- **Split operation: "Rig" or "Fake It".** WSJT-X then shifts the radio's dial so the
  transmitted audio stays around 1500–2000 Hz, where the rig's filters are flat and
  harmonics are suppressed.
- Press **Test CAT** (turns green) and **Test PTT** (radio transmits). Fix these
  before anything else.

## 3. Settings → Audio
- **Input:** the rig's USB codec (or interface); **Output:** same device. Not your
  PC speakers.
- On Windows, set the codec's sample rate to 48 kHz and turn off "enhancements"
  where available.

## 4. Clock — the most common failure
FT8 uses fixed **15-second** transmit/receive periods (FT4: 7.5 s). Your PC clock must
be accurate to well under a second.
- Use a proper NTP client (chrony on Linux; Meinberg NTP or a time-sync utility on
  Windows; macOS automatic time is usually OK).
- Check the **DT** column on decodes: most stations near 0.0 s means you're synced. If
  everyone shows +1.5 s, your clock is off. (Large DT offsets reduce decodes and
  make your calls ignored.)

## 5. Receive level
With the band noise only (no strong signals), adjust the radio's USB audio output
level or the PC recording level so the WSJT-X input meter sits around **30 dB** (gated: unconfirmed, source is paywalled or blocked)
(green). Too low loses weak decodes; too high (red) distorts.

## 6. Transmit level — no ALC
1. Into a dummy load or on a clear frequency, select Tune.
2. Set the radio to the power you want (FT8 is a 100% duty-cycle mode for each 13 s
   transmission; many operators run well below the rig's max to avoid heat).
3. Adjust the WSJT-X **Pwr slider** and/or the PC playback level so the radio's
   **ALC meter shows zero or barely moves** while reaching desired power.
   **Overdriven audio with ALC action splatters** extra signals across the waterfall.
4. Check by asking a nearby station or a WebSDR to look at your signal, or watch
   PSKReporter for ghost reports.

## 7. Operating basics
- Standard dial frequencies (USB) (gated: unconfirmed, source is paywalled or blocked): 80 m 3.573, 40 m 7.074, 30 m 10.136, 20 m 14.074,
  17 m 18.100, 15 m 21.074, 10 m 28.074, 6 m 50.313 MHz. Check your band plan.
- Transmit on a clear spot in the waterfall; enable "Hold Tx Freq".
- Answer a CQ by double-clicking; let the auto-sequence run, but **stay at the
  station** — the software is built for attended operation and in the US, 47 CFR 97.109 requires a control operator at the control point except where Part 97 designates a station for automatic control; check your own country's rules.
- DXpeditions may use **Fox/Hound** mode; read their instructions and call only in
  the hound range.

## 8. Logging
Log QSO pops up at the end; WSJT-X writes ADIF. Companion apps (JTAlert,
GridTracker, N1MM, loggers) receive contacts over **UDP**; enable the UDP server
in Settings → Reporting and point the companion app at the same port.

## Verify
- [ ] Test CAT and Test PTT both pass.
- [ ] DT of most decodes near 0.0 s.
- [ ] Receive level ~30 dB on quiet band (gated: unconfirmed, source is paywalled or blocked).
- [ ] Transmit at chosen power with ALC at zero; split mode on.
- [ ] Contacts appear in your logger via UDP/ADIF.

## Checked

Date checked: 2026-10-25. Jurisdiction: United States for the control-operator rule (47 CFR 97.109); the software guidance is jurisdiction-neutral.

Sources: https://wsjt.sourceforge.io/wsjtx-doc/wsjtx-main-2.7.0.html; https://www.ecfr.gov/current/title-47/part-97/section-97.109 (versions: current eCFR and web pages as read on the date above).

Confirmed: FT8 uses 15 s and FT4 7.5 s T/R sequences (WSJT-X User Guide). 47 CFR 97.109: each station needs a control point with the control operator present, except automatic control, which is limited to stations other Part 97 sections designate.

Gated: claims marked as gated were not confirmed. The WSJT-X User Guide page is about 960,000 characters and only its first 100,000 were read, so the default frequency table, the 30 dB receive level and the ALC advice are unconfirmed. A secondary community list agrees with the frequencies but is not a primary source.

Method: documentation only; no commands were run.
