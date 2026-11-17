---
id: engineering-technology.aerospace-engineering.propulsion-engineering.icao-annex-16-engine-emissions
name: icao-annex-16-engine-emissions
category: engineering-technology
field: aerospace-engineering
product: propulsion-engineering
tags: [propulsion, combustors, emissions, icao-annex-16, lto-cycle, nox, smoke-number, nvpm, caep]
level: practitioner
status: verified
description: "Understand ICAO Annex 16 Volume II engine emissions certification: LTO cycle thrust settings and times, regulated species, and how results are reported."
sources:
  - "ICAO Annex 16 Environmental Protection Volume II (Aircraft Engine Emissions)"
  - "ICAO Engine Emissions Databank"
  - "CAEP documents"
  - "US EPA, 40 CFR 1031.140 Table 1 (LTO test cycles): https://www.ecfr.gov/current/title-40/part-1031/section-1031.140"
  - "EASA, ICAO Aircraft Engine Emissions Databank: https://www.easa.europa.eu/en/domains/environment/icao-aircraft-engine-emissions-databank"
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# ICAO Annex 16 Volume II: engine emissions

**Goal:** know what is measured and how it is characterised, so engine design and installation decisions can be assessed. Practice guidance; the Annex and national regulations govern.

## LTO cycle
The landing and take-off cycle below 3000 ft (gated: unconfirmed, source is paywalled or blocked) consists of four modes with the reference thrust settings and times in mode: take-off 100% for 0.7 min, climb-out 85% for 2.2 min, approach 30% for 4.0 min, taxi/idle 7% for 26.0 min (confirm in the current Annex text). These four settings and times match the subsonic turbojet and turbofan column of the US EPA LTO table in 40 CFR 1031.140 Table 1; turboprop and supersonic engines use different modes and times there. The databank covers turbojet and turbofan engines above 26.7 kN rated output (per the EASA hosting page).

## Regulated species
- Hydrocarbons (HC), carbon monoxide (CO), oxides of nitrogen (NOx), smoke number and, in recent amendments, non-volatile particulate matter (nvPM) mass and number.
- Results are expressed as emission index (g/kg fuel) per mode and as characteristic value `Dp/Foo` (grams per kN of rated output, over the LTO cycle) (gated: unconfirmed, source is paywalled or blocked).
- NOx stringency levels are set by ICAO's Committee on Aviation Environmental Protection (CAEP) in steps (for example CAEP/6 and CAEP/8 limit lines; confirm the lines in the Annex (gated: unconfirmed, source is paywalled or blocked)) as functions of overall pressure ratio and rated output.

## Practice
1. Engine rig and engine tests per the Annex test procedure and measurement specification; data is corrected to reference conditions.
2. Results reported to the national authority and published in the ICAO Engine Emissions Databank.
3. Design levers: combustor type, pressure ratio vs NOx trade, fuel-air mixing, staging.

## Gotchas
- Higher pressure ratio improves cycle efficiency but raises NOx, so the trade is built into the limit lines.
- LTO emissions differ from cruise emissions, which are not regulated by the Annex.

## Verify
- [ ] The LTO thrust settings, times and species list agree with the current Annex edition and amendment.
