---
id: transportation-logistics.aviation-piloting.radiotelephony.phraseology-and-clearance-readback
name: phraseology-and-clearance-readback
category: transportation-logistics
field: aviation-piloting
product: radiotelephony
tags: [aviation-piloting, radiotelephony, rt, r-t, radio, atc-communication, phraseology, icao-phraseology, standard-phraseology, readback, hearback, clearance-readback, callsign, phonetic-alphabet, numbers, ctaf, unicom, uncontrolled-airport, traffic-pattern-calls, class-b, class-c, class-d, controlled-airspace, transition, frequency-change, squawk, say-again, wilco, roger, atis, craft, mayday, pan-pan, 7600]
level: intro
status: gated
description: "Talk on aviation radio: standard phraseology and phonetic numbers, what must be read back, initial call structure, airspace transition requests, and uncontrolled-field position calls."
sources: ["https://www.faa.gov/air_traffic/publications/atpubs/aim_html/chap6_section_4.html", "https://www.faa.gov/air_traffic/publications/atpubs/aim_html/chap4_section_1.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Phraseology and clearance readback

**Goal:** short, standard transmissions that controllers and other pilots can't
misunderstand — and a readback that catches every error before it becomes a deviation.

> Draft: based on ICAO Doc 9432/Annex 10 phraseology with notes where US (FAA AIM)
> usage differs. Your country's AIP/radiotelephony manual is authoritative.

## 1. Basics
- **Listen before you transmit**; don't step on others.
- Think, press, pause half a second, speak, release.
- **Phonetics**: Alfa, Bravo, Charlie, Delta, Echo, Foxtrot, Golf, Hotel, India,
  Juliett, Kilo, Lima, Mike, November, Oscar, Papa, Quebec, Romeo, Sierra, Tango,
  Uniform, Victor, Whiskey, X-ray, Yankee, Zulu.
- Numbers: "tree" (3), "fife" (5), "niner" (9) in ICAO (gated: unconfirmed, source is paywalled or blocked); say each digit for headings,
  squawks, frequencies ("one two one decimal five"); altitudes by thousands and
  hundreds ("two thousand five hundred"); flight levels digit by digit ("flight level
  one two zero").
- Key words: **Roger** (received), **Wilco** (will comply — not used with readbacks),
  **Affirm** (ICAO, yes) / "affirmative" (US), **Negative**, **Say again**, **Standby**,
  **Unable**. Never say "repeat" for "say again" (it means re-fire in military usage).

## 2. Initial call (when you want something)
Order: **who you're calling, who you are, where you are, what you want** — and the ATIS
letter.
"Springfield Approach, Cessna one two three alfa bravo, ten miles south at three
thousand five hundred, information Delta, request transition through the class Charlie
to the north."
If the controller is busy, the first call can be just the callsigns ("Springfield
Approach, Cessna one two three alfa bravo") and wait.

## 3. What must be read back
Read back (ICAO and most States): **ATC route clearances, runway clearances** (enter,
land, take off, cross, backtrack, **hold short**), **runway in use, altimeter settings,
SSR codes, level/altitude instructions, heading and speed instructions, transition
levels**, and frequency changes in many States.
- Read back in the same order, end with your callsign:
  "Climb flight level one two zero, heading two seven zero, one two three alfa bravo."
- Use the controller's exact numbers; don't paraphrase. "Hold short runway two seven,
  one two three alfa bravo" — never just "roger".
- If unsure: "Say again altitude" — never guess.

## 4. IFR clearance (copy and read back)
Use a template on your kneeboard: **C**learance limit, **R**oute, **A**ltitude,
**F**requency, **T**ransponder (CRAFT). Write it before reading it back.

## 5. Uncontrolled airports (CTAF/UNICOM/A/G)
Position calls with **location name at start and end** (US practice):
"Pine Valley traffic, Cessna one two three alfa bravo, left downwind runway one eight,
full stop, Pine Valley."
Typical call points (gated: unconfirmed, source is paywalled or blocked): ~10 NM out, entering downwind (often at 45° to the downwind
midfield), base, final, clear of runway; departure: taking runway and departing direction.
Listen for traffic; radio calls don't replace looking out.

## 6. Abnormal communications
- Lost comms: squawk **7600**; follow published lost-comms procedures (VFR: stay VFR,
  land as soon as practicable; IFR: route/altitude rules as published).
- Urgency: "PAN PAN" ×3; distress: "MAYDAY" ×3 + nature, position, intentions, POB (gated: unconfirmed, source is paywalled or blocked).
- Language: "Unable" plus reason is fine and correct — never accept an instruction you
  can't comply with.

## Gotchas
- Similar callsigns: listen for yours, confirm if in doubt.
- Readback is the pilot's barrier; hearback is the controller's — both fail when the
  frequency is busy and people rush. Be brief, not fast.
- Altitude confusion: "climb to two one zero" vs "two one thousand" — say "flight level".

## Verify
- [ ] Your initial calls follow who/who/where/what plus ATIS.
- [ ] Every hold short, runway, altitude, heading, squawk and altimeter was read back.
- [ ] Clearances were copied onto a CRAFT template before readback.
- [ ] CTAF calls start and end with the airport name.
- [ ] You know 7600, 7700, Mayday and Pan-Pan formats without notes.

## Checked

Jurisdiction: ICAO phraseology with FAA AIM notes. Checked 2026-10-25 via search excerpts of the FAA AIM: a pilot with lost two-way radio sets the transponder to Mode A/3 code 7600; code 7700 alerts radar to an emergency when ATC cannot be contacted without delay. Phonetic number pronunciation, urgency and distress call formats and uncontrolled-airport call points were not confirmed (FAA AIM and ICAO sources returned 403 or are paywalled) and are marked gated.

Method: documentation only; no commands were run.
