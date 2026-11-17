---
id: creative-arts.music.mixing-mastering.tempo-synced-delays-and-throws
name: tempo-synced-delays-and-throws
category: creative-arts
field: music
product: mixing-mastering
tags: [mixing-mastering, reverb, delay, tempo-synced-delay, delay-throws, slapback, ping-pong-delay, dotted-eighth, feedback, filtered-delay, delay-time-calculation, send-automation, echo]
level: practitioner
status: draft
description: "Use delay in a mix: calculating tempo-synced times, slapback and dotted-eighth settings, filtering and saturating repeats, ducking, and automating throws on single words."
sources: ["Mike Senior, Mixing Secrets for the Small Studio (2nd ed.), ch. Mixing with Delays", "https://www.soundtoys.com/ (EchoBoy manual)"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Tempo-synced delays and throws

**Goal:** depth and rhythmic interest from delays that sit inside the groove.

## 1. Delay time
- **Quarter note (ms) = 60000 / bpm**. At 120 bpm: 1/4 = 500 ms, 1/8 = 250, dotted 1/8 = 375, 1/8 triplet = 167, 1/16 = 125.
- Most delay plugins sync to host tempo; still know the numbers for hardware and for nudging.

## 2. Common delay types
| Type | Setting | Use |
|---|---|---|
| **Slapback** | 80-140 ms, 0-1 repeat | rockabilly, rock vocals, guitars: thickness without obvious echo |
| Quarter/eighth | tempo, 2-4 repeats (feedback 20-35%) | subtle depth on vocals and leads |
| **Dotted eighth** | 3/16 of a bar, ping-pong | U2/The Edge-style rhythmic guitar, vocal width |
| Ping-pong | alternating L/R | width, ear candy |
| Short doubler | 10-30 ms, modulated | thickening (like a double-track) |

## 3. Make delays sit
- **Filter the returns**: high-pass ~200-400 Hz and low-pass 3-6 kHz so repeats sit behind the dry sound (tape/analogue delays roll off naturally).
- Saturation and slight modulation on repeats for warmth.
- **Ducking**: sidechain the delay return to the dry vocal so repeats appear in gaps.
- Feed a little delay into the reverb return for a softer, washed tail.

## 4. Throws
- Automate the **send** level (not the return) to send only specific words or phrase ends to a long delay (e.g. the last word of a chorus line, 1/4 or 1/2 note, more feedback).
- In Live/Logic/Pro Tools, draw a send automation spike on the word; or use a separate "throw" delay return with high feedback.

## Gotchas
- Delay times that fight the groove (unsynced) sound messy unless deliberately free.
- Too much feedback builds up into mud; automate feedback down after throws.
- Bright, unfiltered repeats compete with the lead.

## Verify
- Mute the delay return: the vocal should feel smaller and flatter, but the dry balance unchanged.
- Throws land on intended words only (check by soloing the return).
