---
id: transportation-logistics.unmanned-aircraft-operations.mission-planning-airspace.site-assessment-airspace-checks-and-crew-briefing
name: site-assessment-airspace-checks-and-crew-briefing
category: transportation-logistics
field: unmanned-aircraft-operations
product: mission-planning-airspace
tags: [drone-mission-planning, site-survey, site-risk-assessment, airspace-check, notam, tfr, b4ufly, drone-assist, geozones, controlled-airspace, part-107, uk-caa, easa-open-category, a1-a2-a3, specific-category, sora, weather-limits, kp-index, density-altitude, visual-observer, crew-roles, preflight-briefing, emergency-plan, landowner-permission]
level: practitioner
status: gated
description: "Planning a drone job from desk to site: airspace and NOTAM/TFR checks, category rules, site risk assessment, weather go/no-go limits, crew roles and a pre-flight briefing script."
sources: ["https://www.ecfr.gov/current/title-14/section-107.51", "https://www.ecfr.gov/current/title-14/section-107.31", "https://www.faa.gov/uas", "https://www.easa.europa.eu/en/domains/drones-air-mobility"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Site assessment, airspace checks and crew briefing

**Goal:** arrive on site already knowing you are allowed to fly, what can go wrong, and
who does what — then confirm it in five minutes on the ground.

## 1. Desk check (days before)
1. **Category and rules:** US Part 107 (or recreational rules); EU/UK Open (A1/A2/A3),
   Specific (operational authorisation, SORA/PDRA/standard scenario) or Certified (gated: unconfirmed, source is paywalled or blocked). EASA and CAA pages were not read.
   Your aircraft's class mark and pilot competence must match the subcategory and
   distances from people.
2. **Airspace:** controlled airspace (needs LAANC/ATC permission), aerodrome
   flight-restriction zones, prisons, military areas, national parks (often
   prohibited), geozones. Tools: B4UFLY/LAANC apps (US), NATS Drone Assist / CAA
   map (UK), national geozone portals (EU).
3. **NOTAMs and TFRs** for the date: VIP movements, wildfire, events, air displays.
4. **Permissions:** landowner/take-off-and-landing consent; local by-laws; client
   safety rules (site induction, permits to work).
5. **Map review:** satellite imagery and terrain for obstacles (power lines, masts,
   cranes), people concentrations, roads, livestock, radio towers (interference).

## 2. Weather limits (set before you look at the forecast)
- Wind: sustained and gust limits from the manufacturer, reduced for payloads and
  crew experience. Check wind **at altitude** (forecast models give 100 m winds).
- Precipitation: most aircraft are not waterproof (check IP rating).
- Temperature: battery performance below ~10 °C; overheating above ~35–40 °C.
- Visibility and cloud base: VLOS legal minimums; US Part 107: 3 SM visibility,
  500 ft below / 2,000 ft horizontally from clouds.
- Geomagnetic storms can degrade GNSS — check space-weather forecasts (the Kp threshold is not stated here because it was not confirmed).
- Density altitude: hot and high reduces lift and endurance.

## 3. Site risk assessment (on arrival)
- Walk the site. Confirm take-off/landing area (flat, clear, away from metal and
  public), the operating area, and **emergency landing spots**.
- Identify hazards: people/uninvolved persons, overhead lines, birds, RF sources,
  reflective surfaces, trees on the RTH path.
- Mitigations: cordon or marshal the TOLA, adjust flight area, schedule around
  people, set RTH altitude above obstacles (see multirotor preflight skill).
- For Specific/BVLOS ops, confirm the risk assessment conditions are actually met.

## 4. Crew roles
- **Remote pilot in command (PIC):** final authority, flies or supervises.
- **Visual observer(s):** scan airspace and ground, report in standard phrases
  ("Traffic, helicopter, 2 o'clock low, moving left").
- **Payload operator** (if dual operator), **ground safety/marshal** for the public.
- Agree the radio channel and a **stop word** ("STOP, STOP, STOP") anyone can call.

## 5. Briefing script (2–5 minutes)
Objective; area and max altitude; airspace permission and its limits; weather and
limits; hazards and mitigations; RTH altitude and lost-link action; emergency
procedures (flyaway, crash, injury, fire — including battery fire with a LiPo bag/sand);
roles and comms; questions. Log the briefing time.

## Gotchas
- TFRs pop up the same day — re-check NOTAMs just before flying.
- Client expectations to "just fly over the crowd" — you are responsible, not them.
- Forgetting to record the risk assessment: if it isn't written, it didn't happen.
- *Rules cited reflect Part 107 and EU/UK frameworks at writing; confirm current versions.*

## Verify
- [ ] Category and pilot/aircraft eligibility confirmed for the operation.
- [ ] Airspace permission obtained and NOTAM/TFR check done on the day.
- [ ] Weather inside pre-set limits at operating altitude.
- [ ] Site walked, hazards recorded with mitigations, emergency landing spots identified.
- [ ] Crew briefed with roles, stop word and emergency procedures; briefing logged.

## Checked

Jurisdiction: United States (14 CFR Part 107) with EU/UK notes. Checked 2026-10-25 against current eCFR: 107.51 (400 ft AGL maximum or within 400 ft of a structure, 3 statute miles visibility, 500 ft below and 2,000 ft horizontally from clouds), 107.31 (visual line of sight; observer optional). The EU/UK category statements were not confirmed (EASA page returned 404) and are marked gated; the Kp threshold was removed.

Method: documentation only; no commands were run.
