---
id: energy-mining-utilities.amateur-radio.contesting.running-search-and-pounce-and-rate-management
name: running-search-and-pounce-and-rate-management
category: energy-mining-utilities
field: amateur-radio
product: contesting
tags: [contesting, radiosport, amateur-radio, ham-radio, contest-strategy, running, run-frequency, search-and-pounce, s-and-p, rate, rate-meter, qso-rate, multipliers, mults, exchange, dupe, n1mm, n1mm-logger, win-test, dxlog, esm, enter-sends-message, function-keys, cw-macros, voice-keyer, super-check-partial, scp, call-history, cabrillo, log-submission, ubn, so2r, cqww, arrl-dx]
level: practitioner
status: draft
description: "Score more in a ham radio contest: run vs search-and-pounce, N1MM-style macros and ESM, reading the rate meter, chasing multipliers, clean logging and Cabrillo submission."
sources:
  - "N1MM Logger+ documentation on ESM and function keys; general contest operating guides from contest clubs and national societies; paraphrased"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Running, search-and-pounce and rate management

**Goal:** maximise score = contacts × multipliers (the formula varies by contest)
within the rules, with a log accurate enough that few contacts are removed in checking.
Read the specific contest's rules first: exchange, multipliers, categories, off-time
requirements and power limits all differ.

## 1. Two ways to make contacts
- **Running:** you hold a frequency and call CQ; stations come to you. Highest rate
  when your signal is strong enough to attract callers (good antennas, high power, a
  rare location or an opening into a dense population of stations).
- **Search-and-pounce (S&P):** you tune the band and answer other stations' CQs.
  Best for picking up **new multipliers** and when your signal can't sustain a run.
- Most operators mix them: run while the rate holds, S&P when it drops or to collect
  mults, sweeping each band before moving.

## 2. Logger setup (N1MM Logger+ as example; Win-Test and DXLog are similar)
- Load the correct contest module and your exchange; set the start time and category.
- **Function keys** for run and S&P modes (CW or voice keyer):
  `F1` CQ, `F2` exchange, `F3` TU/QRZ, `F4` my call, `F5` his call, plus "AGN?" and "?".
  Keep messages short: "TU W1XYZ" between contacts, not long sign-offs.
- Turn on **ESM (Enter Sends Message)**: the Enter key sends the right message for
  the stage of the contact, so hands stay on the keyboard.
- Load a fresh **Super Check Partial** (MASTER.SCP) and call-history files; they
  suggest likely calls and exchanges from partial copy. Treat them as hints — log
  what you hear, not what the database says.
- Sync the PC clock; connect rig control so frequency/mode log automatically.

## 3. Reading the rate meter
- Watch the **last 10 and last 100 contacts per hour** rates. A run that slides from
  120/h to 40/h with long CQ gaps is finished: change band, or S&P for a while.
- Don't abandon a run during a short lull; a few unanswered CQs is normal.
- Track the band plan through the day with propagation: high bands in daylight toward
  the sunlit populations, low bands at night (see
  `energy-mining-utilities.amateur-radio.hf-operating.reading-propagation-and-working-dx-pileups`).

## 4. Multipliers
- Keep the multiplier window open; it shows which countries/zones/sections you
  still need on each band.
- Late in the contest, a new multiplier is usually worth far more than a few extra
  contacts — spend time finding them.
- Use spotting assistance (cluster) **only if your category allows it**; unassisted
  categories forbid it.

## 5. Accuracy
- Copy the call fully before logging; ask for repeats when unsure ("AGN?" or the
  partial with a question mark). A busted call costs the contact and sometimes a
  penalty.
- Check for **dupes** before working someone (the logger flags them). Working a
  dupe is harmless in most contests; arguing about it isn't.
- After the contest, check the log for obvious busts against SCP and correct only
  what you are sure of.

## 6. Stamina
Plan sleep and off-times per the rules; schedule breaks during your worst
propagation hours. Food and water at the operating position.

## 7. Submission
Export **Cabrillo**, check the header (category, power, operators, location),
submit via the sponsor's web upload before the deadline. Later, read your checking
report (UBN: unique, busted, not-in-log) — it shows exactly where accuracy slips.

## Verify
- [ ] Rules read: exchange, mults, category, off-times.
- [ ] Logger configured with correct contest, exchange, ESM and fresh SCP.
- [ ] Rate watched; run/S&P switched on evidence, not habit.
- [ ] Multiplier window used, assistance only if allowed.
- [ ] Cabrillo header correct and log submitted on time; UBN report reviewed.
