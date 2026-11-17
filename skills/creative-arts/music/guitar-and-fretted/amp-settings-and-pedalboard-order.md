---
id: creative-arts.music.guitar-and-fretted.amp-settings-and-pedalboard-order
name: amp-settings-and-pedalboard-order
category: creative-arts
field: music
product: guitar-and-fretted
tags: [guitar-and-fretted, guitar, guitar-tone, pedal-order, pedalboard, amp-settings, effects-loop, overdrive, distortion, fuzz, buffer, true-bypass, power-supply, ground-loop, amp-modeller, kemper, helix]
level: practitioner
status: draft
description: "Set up guitar tone: amp EQ and gain staging, the standard pedal order, effects loop use, buffers and cable runs, and isolated power to kill noise; applies to modellers too."
sources: ["https://www.boss.info/ (BOSS effects guides - pedal order and effects loop)", "https://www.fender.com/articles/ (amp setup)", "https://line6.com/ (Helix manual - signal chain)", "https://www.voodoolab.com/ (power supply and ground loop guidance)"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Amp settings and pedalboard order

**Goal:** a good core tone, a quiet board, and effects that sit in the right place.

## 1. Amp starting point
- All EQ at 12 o'clock, gain low, master/volume to the needed level.
- Set gain first (how much breakup), then EQ: **mids** are where a guitar lives in a band mix; scooping them sounds big alone and vanishes in the band.
- Bass lower than you think on stage (the room adds lows); treble/presence to taste for clarity.
- Use the guitar's volume knob to clean up a slightly driven amp.

## 2. Standard pedal order (guitar -> amp input)
1. **Tuner** (first, mutes the signal)
2. **Filters/wah/envelope**
3. **Compressor**
4. **Fuzz** (many vintage fuzzes need to see the guitar pickup directly - put before buffers/wah if it misbehaves)
5. **Overdrive / distortion / boost** (low gain into high gain, or boost after drive for a solo lift)
6. **Modulation** (chorus, phaser, flanger, tremolo)
7. **Delay**
8. **Reverb**
- Volume pedal: before drives = acts like the guitar volume (changes gain); after drives = master volume (pre-delay keeps trails natural if placed before delay).
- Rules are starting points: phaser before drive is a classic Van Halen sound.

## 3. Effects loop
- If the amp's **preamp** creates your distortion, put modulation, delay and reverb in the **effects loop** (send/return) so they come after the distortion. Drive pedals stay in front.
- **4-cable method** with a multi-effects unit: drives before the preamp, time effects in the loop.

## 4. Noise and signal integrity
- Long cable runs (> ~6 m total) and many true-bypass pedals load pickups (treble loss): put **one good buffer** early on the board.
- **Isolated power supply** outputs for each pedal; daisy chains cause hum, especially with digital pedals.
- Keep power cables apart from audio cables (cross at right angles).
- Hum that changes with guitar position = single-coil pickup hum, not the board.

## 5. Modellers (Helix, Kemper, Quad Cortex)
- Same order applies inside the signal chain; set output to line level into PA, instrument level into a guitar amp front end (or use the amp's return).
- Gain-stage blocks so the output doesn't clip; match patch volumes.

## Gotchas
- Fuzz Face after a buffer or wah sounds thin and harsh.
- Delay before distortion produces mushy repeats (sometimes desirable, usually not).
- Mid-scooped tones vanish in the band.

## Verify
- Bypass all pedals and compare: no volume drop or treble loss (if there is, add a buffer).
- Board noise check: everything on, guitar volume down - only faint hiss.
