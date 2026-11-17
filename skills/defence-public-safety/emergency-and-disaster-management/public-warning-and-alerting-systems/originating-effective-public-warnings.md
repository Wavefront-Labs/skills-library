---
id: defence-public-safety.emergency-and-disaster-management.public-warning-and-alerting-systems.originating-effective-public-warnings
name: originating-effective-public-warnings
category: defence-public-safety
field: emergency-and-disaster-management
product: public-warning-and-alerting-systems
tags: [public-warning-and-alerting-systems, public-warning, emergency-alerts, alert-origination, ipaws, wea, wireless-emergency-alerts, eas, emergency-alert-system, cell-broadcast, location-based-sms, uk-emergency-alerts, eu-alert, nl-alert, cap, common-alerting-protocol, sirens, outdoor-warning-sirens, warning-message-design, protective-action, evacuation-order, shelter-in-place, warning-fatigue, false-alarm, alert-cancellation, geotargeting, polygon, multilingual-alerts, accessibility, mileti, warning-response-model]
level: practitioner
status: docs-checked
description: "Issue public warnings that people act on: choose channels (cell broadcast, WEA/EAS, sirens), write source-hazard-location-action-time messages, geotarget, update and cancel, avoid false alerts."
sources: ["https://www.fema.gov/emergency-managers/practitioners/integrated-public-alert-warning-system/public/wireless-emergency-alerts", "https://www.fema.gov/sites/default/files/documents/fema_ipaws-best-practices-guide.pdf", "https://www.fcc.gov/node/215906", "https://docs.oasis-open.org/emergency/cap/v1.2/CAP-v1.2-os.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Originating effective public warnings

**Goal:** a warning that reaches the people at risk — and only them, as far as possible —
fast, and that they understand, believe and act on. Research consistently shows people
don't act on the first alert: they look for confirmation. A warning programme is
designed around that.

## 1. Before the event (most of the work)
- **Authority and approval:** written policy on who may originate which alert types,
  for which hazards, with what sign-off. Practise with the console regularly; credentials
  and certificates (e.g. IPAWS COG authorisation in the US) expire.
- **Templates:** pre-written, pre-approved messages per hazard and protective action,
  in each needed language, at each character limit. Under pressure, writers make errors —
  templates prevent them.
- **Channels mapped** to hazards:
  - **Cell broadcast** (WEA in the US, EU-Alert / national systems such as UK Emergency
    Alerts, NL-Alert) — reaches compatible phones in an area without registration.
  - Broadcast **EAS** (radio/TV), outdoor **sirens** (signal "go inside and get
    information", not the message itself), opt-in SMS/app systems, social media,
    websites, door-to-door and loudspeaker for the hardest-to-reach.
  - CAP (Common Alerting Protocol) lets one message feed several channels.
- **Test** and publicise tests, so the public recognises the alert tone.

## 2. Writing the message
Include five elements (FEMA IPAWS best practices; the order can vary, and source goes first in short formats):
1. **Source** — who is issuing it ("Riverside County Sheriff").
2. **Hazard** — what is happening and its impact ("Flash flooding with dangerous water levels").
3. **Location** — where, in terms people recognise (neighbourhoods, landmarks, roads,
   not only grid references or polygons).
4. **Protective action** — what to do, specifically ("Leave now for higher ground. Do
   not drive through water").
5. **Time** — when it takes effect / expires, and when the next update is.
Plus where to get more information (URL/radio station). Style rules:
- Plain language, imperative, no jargon or acronyms ("shelter in place" may need
  explaining: "Go inside, close windows and doors").
- Lead with the action if the character limit is tight. WEA messages are up to 360 characters, with a 90-character version for older WEA-capable phones (FEMA IPAWS).
- Say *how bad* and *how certain*; mention who's at risk and who isn't, to reduce
  congestion from people who needn't move.

## 3. Targeting and timing
- **Geotarget** to the risk area plus a sensible buffer; overwarning breeds complacency,
  underwarning kills. Know your channel's actual spill-over (cell broadcast bleeds across
  cell sectors).
- **Issue early.** Waiting for certainty is the most common failure in post-event reviews
  (several wildfire and flash-flood inquiries have found alerts were too late).
- **Update** at stated intervals and when the situation changes; issue an **all clear**
  or cancellation explicitly — people otherwise don't know when it's safe.

## 4. Mistakes and false alerts
- Two-person check for live sends; "test" and "live" interfaces visually distinct.
- If a false alert goes out, correct it **on the same channel(s) within minutes**, with a
  clear statement it was an error. The 2018 Hawaii false missile alert took 38 minutes to correct through EAS and WEA (FCC report) — the textbook lesson.

## 5. Accessibility and equity
Multilingual messages, alternatives for deaf/hard-of-hearing and blind residents,
people without mobile phones, tourists unfamiliar with place names, and people in
care settings. Partner with community organisations to relay warnings.

## Gotchas
- Sirens are inaudible indoors in many conditions; never rely on them alone.
- Polygons drawn by hand at speed often miss edges of the hazard area — use pre-drawn zones.
- Conflicting messages from different agencies stall action; coordinate wording through
  the PIO/joint information centre.

## Verify
- [ ] Originators authorised and practised; templates exist for each hazard.
- [ ] Message contains source, hazard, location, action and time.
- [ ] Target area matches the risk zone with known overspill.
- [ ] Updates and an all-clear are scheduled.
- [ ] Error-correction procedure tested on every channel.

## Checked

Checked 2026-10-25. Jurisdiction: United States (FEMA IPAWS, WEA); other national systems named only as examples. Source versions: FEMA WEA page and IPAWS Best Practices Guide; FCC report on the 13 January 2018 Hawaii false alert (via search extracts, the FCC page returned 403 to the fetch tool); OASIS CAP v1.2. Confirmed: WEA messages are up to 360 characters with a 90-character version for older WEA-capable phones; the five message elements (source, hazard, location, protective action, expiration time); source goes first in short formats; the Hawaii false-alert correction through EAS and WEA took 38 minutes. Removed an unconfirmed claim about cell broadcast overriding silent mode.

Method: documentation only; no commands were run.
