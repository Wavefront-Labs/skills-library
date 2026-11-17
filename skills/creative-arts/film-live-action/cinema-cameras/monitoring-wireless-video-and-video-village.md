---
id: creative-arts.film-live-action.cinema-cameras.monitoring-wireless-video-and-video-village
name: monitoring-wireless-video-and-video-village
category: creative-arts
field: film-live-action
product: cinema-cameras
tags: [cinema-cameras, film-live-action, video-assist, vtr, video-village, monitoring, wireless-video, teradek, bolt, teradek-bolt, hollyland, dji-transmission, sdi, 3g-sdi, 12g-sdi, hdmi, onboard-monitor, smallhd, evf, viewfinder, director-monitor, client-monitor, calibrated-monitor, rec709, lut-box, lut-loading, frame-lines, false-colour, waveform, zebras, peaking, anamorphic-desqueeze, playback, qtake, video-assist-playback, timecode-overlay, rf-interference, antenna, 5ghz, latency, cable-runs, fiber, video-distribution, da, distribution-amplifier, monitor-calibration, probe-calibration, on-set-monitor-setup, wireless-video-setup, bolt-pairing, video-range, village-layout, village-etiquette, client-monitors, monitor-lut-chain, lut-on-monitor, monitor-chain, video-assist-operation, qtake-setup, playback-on-set-video, evf-setup, operator-monitor, viewfinder-setup]
level: practitioner
status: draft
description: "Build the on-set video chain: SDI from camera, LUT boxes, wireless transmitters and RF planning, calibrated monitors for DP/director/client, exposure tools and frame lines, QTAKE playback."
sources:
  - "https://teradek.com/pages/support (Teradek Bolt user guides and RF best practice)"
  - "https://www.smallhd.com/ (SmallHD monitor tools - false colour, waveform, LUTs)"
  - "https://qtake.com/ (QTAKE video assist documentation)"
  - "American Cinematographer Manual, 10th ed. - On-set monitoring and viewing"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Monitoring, wireless video and video village

**Goal:** everyone who makes a decision sees a trustworthy picture at the right time:
the operator frames, the AC focuses, the DP judges exposure, the director watches
performance, and the client sees the look - without a cable across the set or a monitor
that lies.

## 1. The signal chain
`Camera SDI out (log + LUT applied, or clean) -> LUT box / wireless TX -> wireless RX ->
distribution amplifier -> monitors (DP/director/script/AC/village) -> video assist
(record + playback)`.
- Cameras offer multiple SDI outputs: typically one **clean** (for VFX/record) and one
  with **LUT, frame lines and status overlays**. Decide which goes where: operators and
  ACs often want overlays; the village wants clean picture + frame lines only.
- **3G-SDI** carries 1080p; **12G-SDI** for 4K; HDMI only for the last metre. Use
  quality BNC cable; long runs (>50-70 m for 3G) need a DA/re-clocker or fibre.
- **LUT application** in the camera (fastest) or a LUT box (Teradek Colr, BoxIO,
  AJA FS-HDR) fed by the DIT with show LUT + CDL. Monitor paths must all see the *same*
  LUT; a village on a different LUT makes different decisions.

## 2. Wireless
- **Zero-delay 5 GHz systems** (Teradek Bolt 4K/6 series, DJI Transmission, Hollyland
  Mars/Pyro, Vaxis): <1 frame latency, line of sight 150-500 m depending on model;
  one TX to multiple RX (Bolt: up to 4-6 RX).
- **RF planning**: scan the 5 GHz band (Teradek's spectrum tool) and lock to a clean
  channel; coordinate with the sound department's wireless and the DIT's Wi-Fi; keep
  antennas vertical, unobstructed, away from metal and bodies. Panel antennas on the
  RX for long throws. Set the TX to a fixed channel on a multi-camera shoot and label.
- Long-range/lower-quality systems (H.264 streaming to iPads, QTAKE Monitor) are fine for
  the client tent, never for focus.
- Cable where you can: a cabled village is more reliable than any wireless.

## 3. Monitors and tools
- **Operator**: EVF or 7" onboard (SmallHD, TVLogic) with frame lines, desqueeze for
  anamorphic, peaking, zoom. Anamorphic: every monitor in the chain must desqueeze
  (camera does it on the SDI with overlays or the monitor does it).
- **1st AC**: 7" on the hand-unit side or on the camera with **peaking** and 1:1 zoom; some
  hand units (Hi-5, Preston) show depth-of-field bars.
- **DP/DIT**: a **calibrated** reference monitor (Flanders, Sony BVM/PVM, TVLogic) in a
  tent at Rec.709 gamma 2.4 ~100 nits, or an HDR reference for HDR shows, with waveform,
  vectorscope, false colour. Calibrate with a probe each week; a monitor off by half a
  stop costs the whole show.
- **Director's monitor**: 17-24", bright enough for the viewing condition (daylight
  needs 1500+ nits or a tent); clean picture, frame lines, timecode overlay.
- **Video village**: 1-2 monitors, headphones for sound (comms feed from the mixer),
  chairs, cover. Keep it close enough to walk to the actors, far enough to be silent.
- **Exposure tools** are only trustworthy on the log signal or through a known LUT;
  false colour scales differ per monitor brand - learn the one you use.

## 4. Video assist / playback
QTAKE (or Video Devices Pix, a Blackmagic HyperDeck for simple setups) records every
take from every camera with timecode and metadata, offers instant playback, A/B compare,
split screen for continuity, live compositing (previs, VFX comp with greenscreen keys),
frame grabs for continuity/wardrobe, and streams to iPads. The video assist operator
logs takes with scene/take from the script supervisor. On a multi-camera show this is the
only way to see all cameras at once.

## 5. Power and rigging
Each wireless RX and monitor needs a battery plate (V-mount/Gold mount) or D-tap; run a
battery count. Monitors on C-stands with sandbags; rain covers; sunshades. Tape every
cable path.

## Gotchas
- LUT baked into the camera's main recording because the LUT output was routed wrong.
- Village on a bright consumer TV, director complains the shot is "too dark".
- 5 GHz channel shared with the sound team's video or the hotel Wi-Fi; dropouts on the take.
- Anamorphic not desqueezed on the AC's monitor; marks pulled on a squeezed image.
- Monitors never calibrated after the rental house.

## Verify
- [ ] Clean and LUT'd SDI outputs routed deliberately; recording is log/RAW.
- [ ] One show LUT on every monitor in the chain; DP monitor calibrated this week.
- [ ] Wireless channel scanned and locked; antennas placed; backup cable run.
- [ ] Video assist recording all cameras with timecode; playback tested before the first take.
