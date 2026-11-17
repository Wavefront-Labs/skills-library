---
id: languages-linguistics.signalling-and-coded-communication.morse-code.learning-morse-by-sound-with-correct-timing-and-prosigns
name: learning-morse-by-sound-with-correct-timing-and-prosigns
category: languages-linguistics
field: signalling-and-coded-communication
product: morse-code
tags: [morse-code, international-morse, cw, koch-method, farnsworth-timing, paris-standard, wpm, dit-dah, morse-timing, head-copy, straight-key, keying, prosigns, sos, ar, sk, bt, error-signal, morse-abbreviations, q-codes, morse-by-light, morse-by-sound, tapping-morse]
level: intro
status: draft
description: "Learn International Morse as sound patterns with the Koch and Farnsworth methods, send with exact 1:3:7 timing, and use prosigns and abbreviations correctly in any medium."
sources: ["ITU-R M.1677 International Morse code", "ARRL and amateur-radio training material on Koch/Farnsworth (paraphrased)"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Learning Morse by sound with correct timing and prosigns

**Goal:** recognise and send International Morse reliably — by sound, light or tapping —
with timing another operator can read. For on-air amateur-radio practice (paddles, QSO
structure) see `energy-mining-utilities.amateur-radio.cw-morse.learning-head-copy-paddle-sending-and-a-standard-cw-qso`.

## 1. The timing is the code
Everything is measured in **units** (one dot length):
| Element | Length |
|---|---|
| dot (dit) | 1 |
| dash (dah) | 3 |
| gap inside a character | 1 |
| gap between characters | 3 |
| gap between words | 7 |
- Speed: the standard word **PARIS** is 50 units, so **dot length (ms) = 1200 ÷ wpm**.
  At 20 wpm a dot is 60 ms.
- Most sending problems are spacing, not dots and dashes: run-together characters
  (`A N` sent as `P`) and clipped word gaps make copy impossible.

## 2. Learn by sound, never by chart
Memorising "A = dot dash" creates a lookup step that caps you around 5–10 wpm.
Learn each character as a **rhythm** ("di-dah" for A).
- **Koch method:** start at your target character speed (e.g. 20 wpm) with just **two
  characters**; practise random groups until you copy **90%**, then add one character. Repeat
  through the alphabet, digits and common punctuation.
- **Farnsworth timing:** characters sent at full speed but with **stretched gaps** between
  them, so you have thinking time without learning slow, distorted rhythms. Tighten gaps
  as you improve.
- 10–20 minutes, daily, beats long weekly sessions. Many free trainer apps implement both
  methods — set character speed and effective speed separately.
- Move from writing letters down to **head copy** (understanding words without writing)
  once single characters are automatic.

## 3. Sending
- On a **straight key**: relaxed wrist, light touch, close with the arm not the fingers; send
  slightly *slower* than you can receive.
- Off the radio (torch, whistle, tapping), keep the same 1:3:7 proportions; with light,
  lengthen everything a little because the receiver's eye needs time.
- Record yourself and decode the recording (or use a decoder app); if software struggles,
  so will humans.

## 4. Prosigns and abbreviations
Prosigns are sent as one run-together character (shown with an overbar or as letters):
- **SOS** `···−−−···` — distress, sent continuously, not as three letters.
- **AR** end of message · **SK** end of contact · **BT** break/new paragraph (`−···−`)
- **AS** wait · **K** go ahead (anyone) · **KN** go ahead (named station only)
- **Error:** eight dots (`········`), then resend the last correct word.
Common abbreviations: `R` received, `?` repeat, `TU` thank you, `73` best regards, and
the Q-codes (QTH location, QRS send slower, QRZ who is calling?).

## Gotchas
- Learning at slow character speed builds rhythms you must later unlearn — use Farnsworth instead.
- Confusable pairs: `E`/`T`, `I`/`M`, `S`/`O`, `H`/`5`, `U`/`V`; drill them side by side.
- Plateaus around 10 and 20 wpm are normal; push through with copying slightly above comfort.
- Numbers are long (five elements) — easy to miscount under stress; drill them separately.

## Verify
- [ ] You copy random 5-character groups at 90% at your chosen character speed.
- [ ] Your sending, recorded and decoded by software, comes out error-free.
- [ ] You can state dot length for a given wpm (1200 ÷ wpm).
- [ ] You send SOS and AR as single run-together prosigns, and correct an error with eight dots.
