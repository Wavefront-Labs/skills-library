---
id: creative-arts.animation.sound-design.surround-mix-and-fold-down
name: surround-mix-and-fold-down
category: creative-arts
field: animation
product: sound-design
tags: [surround-mix, 5-1, fold-down, downmix, lo-ro, lt-rt, lfe, centre-channel, re-recording-mix, ffmpeg]
level: advanced
status: draft
description: "Mix in 5.1 for animation: what goes in each channel, LFE use, centre dialogue, and checking the stereo fold-down (Lo/Ro) so the downmix still plays."
sources:
  - https://www.itu.int/rec/R-REC-BS.775
  - https://www.dolby.com/
  - https://ffmpeg.org/ffmpeg-filters.html#pan-1
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# 5.1 mixing and fold-down

**Goal:** a 5.1 mix that uses the room, and a stereo fold-down of it that is still balanced.

## Channel order and roles (SMPTE/ITU order: L R C LFE Ls Rs)

| Channel | Carries |
|---|---|
| C | dialogue (almost all of it), on-screen centred effects |
| L / R | music, effects, BGs, panned dialogue for off-centre characters (sparingly) |
| Ls / Rs | BGs, reverb returns, music spread, fly-overs and effects with surround intent |
| LFE | low-frequency **effects** only (explosions, impacts), below about 120 Hz, +10 dB in-band gain on playback |

Do not rely on LFE for essential content; the stereo downmix usually discards it.

## Mixing rules

- Keep dialogue in C, it anchors the screen for every seat.
- Pan movement across the screen in L-C-R; reserve surround pans for clear intent (a ship flying overhead).
- Bass management: content in L/R/C below 80 Hz goes to the sub in most home systems; check on a bass-managed
  monitor setup.

## Fold-down

ITU-style stereo downmix (Lo/Ro): `Lo = L + 0.707*C + 0.707*Ls`, `Ro = R + 0.707*C + 0.707*Rs`, LFE dropped.
Check it:

```
ffmpeg -i mix51.wav -af "pan=stereo|FL=FL+0.707*FC+0.707*BL|FR=FR+0.707*FC+0.707*BR" fold.wav
```
(`BL/BR` or `SL/SR` depending on the file's channel layout; check with ffprobe.) Many deliveries also require a
**separate** stereo mix rather than an automatic downmix; if so, mix it as its own pass.

## Gotchas

- Surround reverb returns duplicated in fronts build up in the fold-down and make dialogue muddy.
- Out-of-phase content between L and R or between fronts and surrounds can cancel in the fold-down.
- Loudness of the fold-down is usually higher than the 5.1's; measure both
  (`creative-arts.animation.sound-design.atsc-a85-broadcast-loudness`).

## Verify

Listen to the fold-down: dialogue still on top, no element disappears, level within the delivery target; channel
order of the 5.1 file confirmed with `ffprobe -show_streams` (channel_layout 5.1).
