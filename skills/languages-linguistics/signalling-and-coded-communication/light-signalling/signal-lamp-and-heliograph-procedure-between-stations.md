---
id: languages-linguistics.signalling-and-coded-communication.light-signalling.signal-lamp-and-heliograph-procedure-between-stations
name: signal-lamp-and-heliograph-procedure-between-stations
category: languages-linguistics
field: signalling-and-coded-communication
product: light-signalling
tags: [light-signalling, aldis-lamp, signal-lamp, flashing-light, heliograph, signal-mirror, morse-by-light, international-code-of-signals, ics, flashing-light-procedure, call-sign, aa-call, answering-signal, ttt, ar, de, rpt, error-signal, aiming, dark-adaptation, visual-signalling, seamanship]
level: practitioner
status: draft
description: "Send and receive Morse by directed light: aim an Aldis lamp or heliograph, follow the call-answer-text-ending procedure of the International Code of Signals, and pace for readability."
sources: ["IMO/ICS International Code of Signals, flashing-light signalling chapter (paraphrased)", "Historical army heliograph manuals (overview)"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Signal lamp and heliograph procedure between stations

**Goal:** pass a short message by flashing light between ships, shore stations or field
positions, with a procedure both ends recognise so nothing is lost or duplicated.
Prerequisite: Morse characters and 1:3:7 timing
(see `languages-linguistics.signalling-and-coded-communication.morse-code.learning-morse-by-sound-with-correct-timing-and-prosigns`).

## 1. Equipment and aiming
- **Signal (Aldis) lamp:** a steady lamp with a shutter or trigger, plus a sighting telescope
  or ring sight. Aim with the sight, not by eye along the body; at range a lamp's beam is
  narrow and a few degrees off is invisible to the receiver.
- **Heliograph:** a mirror reflecting sunlight with a sighting vane and shutter (or tilting
  mirror) to make flashes. Works only in sun, but ranges of tens of kilometres are
  historically recorded in clear desert air (treat as best case). A **second mirror** is
  needed when the sun is behind you relative to the target.
- **Improvised:** a torch works at short range; cover and uncover it rather than switching
  (switching bulbs fade in and out).
- Brace the instrument; a wobbling beam flickers on and off at the receiver.

## 2. Pace for the eye
Light is read more slowly than sound. Send at a steady **6–10 wpm** unless both operators
are practised, make dashes clearly three times the dot, and **exaggerate gaps** slightly.
Visibility, haze and background lights all slow reading further.

## 3. The procedure (International Code of Signals pattern)
1. **Call:** the general call `AA AA AA…` (or the station's identity) repeated until answered.
2. **Answer:** the receiver replies `TTTT…` (continuous T's) until the sender stops calling.
3. **Identity:** sender gives its identity after `DE`; the receiver may answer with its own.
4. **Text:** sent word by word; the receiver acknowledges **each word** with a single `T`.
   No `T` → the sender repeats the word.
5. **Error:** the sender makes a series of `E`s, then resends the last correct word.
6. **Repetition request:** the receiver uses `RPT` (with "all after"/"all before" qualifiers
   in the ICS) for missed parts.
7. **Ending:** sender signals `AR`; receiver acknowledges with `R` (received).
Check the current ICS text for exact qualifiers; navies and local services add their own
prosigns, so agree the procedure if signalling outside the ICS.

## 4. Receiving well
- Use a **spotter-writer pair**: one watches and calls letters, the other writes.
- At night, protect **dark adaptation** — no white light on the bridge or in the post; look
  slightly beside the lamp if glare blooms.
- Write what you see, including uncertain characters marked `?`, then ask for repeats.

## Gotchas
- **Aiming drift:** ships roll; re-sight every few words.
- Background lights (shore lighting, other vessels) can mimic flashes — confirm the source
  with a call-and-answer first.
- Don't point heliographs or strong lamps at aircraft or drivers; mirror flashes are also
  a recognised **distress** signal, so be clear about intent.
- Long messages invite error: shorten, use ICS code groups where possible.

## Verify
- [ ] You can sight a lamp onto a target and hold it steady for a full word.
- [ ] A practice exchange follows call → TTTT → DE → word-by-word T's → AR → R without prompting.
- [ ] An inserted error is corrected with E's and the word resent.
- [ ] A 10-word message passes with no unacknowledged words at your chosen range.
