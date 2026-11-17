---
id: energy-mining-utilities.amateur-radio.emergency-communications.running-a-directed-net-and-passing-formal-traffic
name: running-a-directed-net-and-passing-formal-traffic
category: energy-mining-utilities
field: amateur-radio
product: emergency-communications
tags: [emergency-communications, emcomm, amateur-radio, ham-radio, ares, races, raynet, net-control, ncs, directed-net, open-net, tactical-call-signs, check-in, net-log, formal-traffic, radiogram, ics-213, message-precedence, emergency-traffic, priority-traffic, welfare-traffic, read-back, word-count, check, served-agency, go-kit, battery-power, solar-power, amp-hours, field-station, shift-handover]
level: practitioner
status: gated
description: "Act as net control in an emergency: open and run a directed net with tactical calls, log check-ins, prioritise traffic, pass written messages accurately (ICS-213/radiogram), and power a field station."
sources:
  - "https://www.ecfr.gov/current/title-47/part-97/section-97.119"
  - "https://training.fema.gov/icsresource/icsforms.aspx"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Running a directed net and passing formal traffic

**Goal:** turn a crowded frequency in an emergency into an orderly channel where the
most urgent message always gets through and every written message arrives word-for-
word. Amateur emergency groups support a **served agency** (emergency management,
Red Cross, hospitals); follow their instructions and your group's plan.

## 1. Directed vs open net
- **Open net:** stations call each other freely. Fine for quiet periods.
- **Directed net:** every transmission goes through **net control (NCS)**, who grants
  permission. Use it whenever traffic is heavy or urgent.

## 2. Opening the net (script it in advance)
1. Listen; confirm the frequency is clear; ask "is this frequency in use?".
2. Read the preamble: net name, purpose, that it is directed, "stations with
   **emergency or priority traffic** call now", then request check-ins by location or
   function.
3. Use **tactical call signs** for locations ("Shelter 2", "EOC", "Hospital") so
   messages follow the post, not the person. Operators still give their own call sign
   at the legally required ID intervals (US, 47 CFR 97.119(a): at the end of each communication and at least every 10 minutes during one).
4. Appoint an **alternate NCS** early and a logger if possible.

## 3. Running it
- Log every check-in: time, call/tactical call, location, traffic held, status (in
  service, going off-air).
- Take **emergency first, then priority, then welfare, then routine** (gated: unconfirmed, source is paywalled or blocked). Ask
  periodically "any emergency or priority traffic?"
- Pair stations: "Shelter 2, call EOC and pass your traffic" — or move them to a
  secondary frequency so the net stays clear.
- Keep it short and plain: no chatting, no Q-codes on voice, plain-language times in
  24-hour format.
- **Shift change:** NCS fatigue causes mistakes; hand over regularly with a
  verbal summary of stations, open traffic and problems.

## 4. Formal messages
Use the agency's form (often **ICS-213, General Message** in the US) or the **radiogram** format.
Radiogram preamble: number, precedence, handling instructions, station of origin,
**check** (word count of the text), place of origin, time filed, date (gated: unconfirmed, source is paywalled or blocked). Then address,
text, signature.
- Sender writes it; you never paraphrase.
- Send slowly, phrase by phrase; spell difficult words and names phonetically
  ("I spell...").
- The receiving station **counts words and compares with the check.** Mismatch =
  find the missing or extra word before accepting.
- **Read back** critical numbers (quantities, addresses, phone numbers).
- Log message number, time sent/received, to and from stations.

## 5. Field station power
- Estimate consumption: receive current × hours + transmit current × hours (assume
  a duty cycle, e.g. 10–25% transmit on a busy net). Example: a radio drawing 1 A on
  receive and 20 A on transmit, 12 hours at 20% transmit ≈ (0.8×12×1) + (0.2×12×20) ≈
  58 Ah.
- Lead-acid batteries should not be discharged much below about 50% (gated: unconfirmed, source is paywalled or blocked) → size
  ~2× the need; lithium iron phosphate can use most of its rated capacity.
- Solar: panel watts × realistic sun-hours × ~0.7 losses must replace the daily Ah.
- Fuses at the battery; fresh spares; check terminal voltage at the radio under
  transmit (drops below ~11.5 V on a 12 V system (gated: unconfirmed, source is paywalled or blocked) cause distorted audio and resets).

## 6. Go-kit essentials
Radio(s), antennas and coax, power and charging, headphones, notebooks and pens,
blank message forms, frequency/repeater lists, ID/credentials, water, food, light,
weather gear, first aid.

## Verify
- [ ] Preamble scripted; tactical calls assigned; alternate NCS named.
- [ ] Check-ins and traffic logged with times.
- [ ] Emergency/priority traffic taken first; side traffic moved off frequency.
- [ ] Every formal message word-counted against its check and critical items read back.
- [ ] Power budget calculated with margin; voltage under transmit checked.

## Checked

Date checked: 2026-10-25. Jurisdiction: United States (47 CFR Part 97; FEMA ICS forms).

Sources: https://www.ecfr.gov/current/title-47/part-97/section-97.119; https://training.fema.gov/icsresource/icsforms.aspx (versions: current eCFR and web pages as read on the date above).

Confirmed: 47 CFR 97.119(a): identify at the end of each communication and at least every 10 minutes during one. FEMA lists ICS Form 213 as General Message. The power example was recomputed: 0.8 x 12 x 1 + 0.2 x 12 x 20 = 57.6 Ah.

Gated: claims marked as gated were not confirmed. The ARRL radiogram preamble fields and precedence order, the lead-acid 50 percent depth-of-discharge rule and the 11.5 V transmit-voltage figure come from sources that were not fetched.

Method: documentation only; no commands were run.
