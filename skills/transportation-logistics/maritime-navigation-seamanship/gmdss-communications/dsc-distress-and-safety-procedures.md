---
id: transportation-logistics.maritime-navigation-seamanship.gmdss-communications.dsc-distress-and-safety-procedures
name: dsc-distress-and-safety-procedures
category: transportation-logistics
field: maritime-navigation-seamanship
product: gmdss-communications
tags: [gmdss-communications, gmdss, dsc, digital-selective-calling, maritime-navigation-seamanship, vhf, mf, hf, channel-16, channel-70, 2182-khz, mayday, pan-pan, securite, distress-alert, false-alert, cancellation, mmsi, navtex, epirb, sart, inmarsat-c, iridium, sea-areas, a1-a2-a3-a4, radio-log, goc, roc, maritime-radio]
level: practitioner
status: gated
description: "Send and handle GMDSS distress, urgency and safety traffic: DSC alert then MAYDAY voice, acknowledge/relay rules, cancel false alerts, NAVTEX/EPIRB/SART checks and radio log."
sources: ["https://www.ecfr.gov/current/title-47/section-80.1069", "https://www.ecfr.gov/current/title-47/section-80.359", "https://www.ecfr.gov/current/title-47/section-80.1077"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# DSC distress and safety procedures — alert, talk, cancel correctly

**Goal:** get a distress alert to rescue authorities fast and correctly, communicate
on voice in the standard format, handle alerts from others without causing confusion,
and cancel a false alert before it wastes a rescue. Operators need the appropriate
certificate (GOC/ROC/SRC); exact button sequences vary by radio — keep the
manufacturer's quick card at each set.

## 1. Know your equipment and sea area
- Sea areas (47 CFR 80.1069): **A1** within VHF coast station radiotelephone coverage with continuous DSC alerting, **A2** within MF coast station coverage (excluding A1), **A3** within an Inmarsat geostationary satellite coverage (excluding A1 and A2), **A4** everything else. Typical ranges quoted for A1 and A2 (about 20 to 30 nm and 100 to 150 nm) (gated: unconfirmed, source is paywalled or blocked).
- Your **MMSI** is programmed into DSC radios and EPIRB; GNSS position must be fed to
  DSC (check it's current — a manual position goes stale).

## 2. Sending a distress alert (grave and imminent danger)
1. **DSC alert:** lift the distress button cover, select nature of distress if time
   allows (fire, flooding, collision, grounding, listing, sinking, abandoning, MOB…),
   **press and hold** ~3–5 s. Radio sends on VHF ch 70 (or MF 2187.5 kHz / HF).
   It repeats automatically until acknowledged.
2. **Voice on the associated channel** (VHF ch 16, MF 2182 kHz):
   ```
   MAYDAY MAYDAY MAYDAY
   THIS IS <ship name ×3>, <call sign>, MMSI <number>
   MAYDAY <ship name, call sign>
   MMSI <number>
   POSITION <lat/long or bearing and distance from a known point>
   <nature of distress>
   <assistance required>
   <other info: persons on board, intentions, abandoning?>
   OVER
   ```
3. Also: satellite alert (Inmarsat-C distress / Iridium), and **EPIRB** (406 MHz,
   manual activation if not float-free) when vessel may be lost. Take **SART/AIS-SART**
   and portable VHF to the survival craft.

## 3. Urgency and safety
- **PAN PAN** ×3 — urgent, no grave and imminent danger (medical advice, engine failure
  drifting to a lee shore, person overboard where no immediate distress). DSC urgency
  call (all ships or individual) then voice on ch 16.
- **SECURITE** ×3 — navigational or weather warning; announce on ch 16 then move to a
  working channel.

## 4. Receiving a distress alert (another ship)
- **VHF in A1:** don't acknowledge by DSC immediately; listen on ch 16. Coast station
  normally acknowledges. If no coast station acknowledges and you can help,
  acknowledge **by voice** to the distressed vessel on ch 16, inform the RCC.
- **MF/HF:** generally do not acknowledge by DSC (it stops the repeats that the
  shore may need); listen on the voice frequency, inform the RCC.
- **Relay** (MAYDAY RELAY) only when the casualty can't, the RCC hasn't acknowledged,
  or you're instructed — rules tightened over the years; follow current IMO guidance
  posted on board.
- Log everything: times, positions, actions.

## 5. False alert — cancel immediately
1. Switch off/reset the DSC transmission if still sending (or send a DSC
   **cancellation** if the radio supports it).
2. Voice on the associated channel:
   ```
   ALL STATIONS ×3, THIS IS <ship name ×3>, <call sign>, MMSI <number>
   POSITION <...>
   CANCEL MY DISTRESS ALERT OF <date/time UTC>
   MASTER <ship name, call sign, MMSI, date time UTC>
   ```
3. Inform the nearest RCC/coast station. A false EPIRB: switch off and call the RCC.
There is normally no penalty for an honest, promptly cancelled false alert.

## 6. Routine tests and watch
- DSC: test calls to a coast station per schedule; never press distress to test.
- NAVTEX: receiver set for the station(s) and message types (A, B, D mandatory),
  printout/log checked each watch.
- EPIRB/SART: monthly self-test, check battery and hydrostatic release expiry dates.
- Watch: continuous DSC watch on ch 70 (and MF/HF per area), ch 16 listening watch
  where required, plus ch 13 bridge-to-bridge locally.
- Radio log: every distress/urgency/safety communication and tests.

## Gotchas
- DSC sends a stale position if GNSS feed failed — check after any alarm.
- Wrong "all ships" vs individual DSC selection floods the channel.
- Ch 16 is for calling and distress — move traffic to a working channel.

## Verify
- [ ] Distress card at each set with MMSI, call sign and voice format filled in.
- [ ] DSC position live; tests logged; EPIRB/SART tests and expiry dates logged.
- [ ] Crew can demonstrate distress alert and cancellation procedures.

*Uncertainty:* acknowledgement and relay rules are summarised; follow the current IMO procedures posted at the GMDSS station.

## Checked

Jurisdiction: international GMDSS with US FCC rules (47 CFR Part 80). Checked 2026-10-25 on eCFR: 80.1069 (definitions of sea areas A1 to A4), 80.359(b) (DSC distress frequencies 156.525 MHz VHF ch 70 and 2187.5 kHz), 80.1077 (2182 kHz and 156.8 MHz ch 16 radiotelephony, 406.0 to 406.1 MHz EPIRB band). Not confirmed and marked gated: the typical A1/A2 range figures. Operator button-hold times and radio sequences vary by set and were not checked.

Method: documentation only; no commands were run.
