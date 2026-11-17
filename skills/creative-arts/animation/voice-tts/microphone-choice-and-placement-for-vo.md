---
id: creative-arts.animation.voice-tts.microphone-choice-and-placement-for-vo
name: microphone-choice-and-placement-for-vo
category: creative-arts
field: animation
product: voice-tts
tags: [mic-technique, microphone, vo-recording, pop-filter, proximity-effect, voice-over]
level: practitioner
status: draft
description: "Choose and place a microphone for animation voice-over: large-diaphragm condenser basics, distance, off-axis placement, pop control and room-matched pickups."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Microphone choice and placement for VO

## Choosing the mic
- The usual studio default for character voice is a large-diaphragm condenser (a cardioid pattern, with a balanced XLR path to a clean preamp). It captures detail and the subtle breath and mouth sounds that animation editors can cut around.
- Dynamic mics (e.g. broadcast-style) are more forgiving in untreated rooms and with loud, energetic actors. They pick up less room, which can be a feature at home.
- Use the same model for a character across the whole series. Different mics change timbre enough that pickups noticeably mismatch.
- Match to the voice, not the price tag: try two mics on the actor and choose by ear, while the actor reads a representative line.

## Placement
- **Distance**: roughly a hand-span (about 15-20 cm / 6-8 in) from the capsule to the mouth is a typical starting point for close-mic dialogue. Closer increases proximity effect (bass boost) and intimacy; farther increases room sound.
- **Angle**: place the mic slightly above or below the mouth and angled, not directly in front of the airstream. This reduces plosives (p, b) and breath blasts.
- **Pop filter**: put a nylon or metal screen 5-8 cm in front of the capsule so it also keeps the actor at a consistent distance.
- **Consistency**: mark the actor's position (tape on the floor, stand fixed). Ask the actor to hold their distance when they get animated; performance moves such as leaning back are fine for effort sounds, but treat them as separate takes.
- **Shout lines**: pull the mic back or enable a pad on the mic/preamp, and record the loud line separately so you can set gain correctly.
- **Off-axis for loud takes**: turning the actor's head or angling the mic slightly reduces peaks.

## Settings
- Cardioid pattern (omni and figure-8 let in the room).
- High-pass at 70-100 Hz if the mic or preamp offers it, only to remove rumble; do not rely on it to hide a handling-noise problem.
- Record with headroom: peaks around -12 to -6 dBFS in a 24-bit session is a common comfortable range.

## Common faults and fixes
| Symptom | Cause | Fix |
|---|---|---|
| Boomy, bassy voice | Too close, proximity effect | Move back 5 cm, or high-pass lightly in post |
| Plosives | On-axis airstream | Angle mic, add pop screen |
| Hollow, roomy tone | Too far or bare room | Move in, add absorption (see `booth-and-room-treatment.md`) |
| Level jumps | Actor moving | Mark the position, coach the actor |

## Verify
- [ ] Same mic, preamp and distance as previous sessions for that character.
- [ ] A test line shows no clipping and no audible plosives on playback.
