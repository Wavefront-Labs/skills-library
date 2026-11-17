---
id: repair-maintenance.building-services-equipment-maintenance.standby-generator-ups-maintenance.generator-load-testing-and-ups-battery-care
name: generator-load-testing-and-ups-battery-care
category: repair-maintenance
field: building-services-equipment-maintenance
product: standby-generator-ups-maintenance
tags: [building-services-equipment-maintenance, standby-generator-ups-maintenance, standby-generator, diesel-generator, genset, emergency-power, ats, automatic-transfer-switch, transfer-switch-exercise, load-bank, load-bank-test, wet-stacking, nfpa-110, monthly-generator-test, block-heater, fuel-polishing, diesel-bug, ups, ups-battery, vrla, battery-impedance, battery-monitoring, bypass, runtime, critical-power, black-building-test]
level: practitioner
status: gated
description: "Keep emergency power ready: weekly generator inspection, monthly loaded runs and ATS exercise, load-bank testing to beat wet stacking, fuel care, and UPS battery and bypass checks."
sources: ["https://www.nfpa.org/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Generator load testing and UPS battery care

**Goal:** emergency power that starts, transfers and carries load every time it's
needed. Most generator failures are batteries, fuel and controls left in the wrong mode;
most UPS failures are batteries. In the US, NFPA 110 sets emergency-power testing for
many buildings; in the UK BS 7698 / ISO 8528 and the insurer often govern. Check your
site's requirement and the OEM manual.

## 1. Generator — weekly inspection (not running)
- Controller in **AUTO** (the most common "failure" is a set left in OFF/manual after work).
- No active alarms; fault log read.
- Starting batteries: voltage (≈12.6–13 V per 12 V battery at rest, more on float),
  charger output and alarms, terminals clean and tight.
- Fluids: oil, coolant (and antifreeze strength), fuel day tank level; no leaks.
- **Block/jacket water heater** working (engine warm to the touch in cold climates) — a
  cold engine starts slowly and may miss the start-time requirement for emergency
  systems (10 s for NFPA 110 Type 10; gated: unconfirmed, source is paywalled or blocked).
- Air intake and louvres clear, exhaust intact, rain cap OK.

## 2. Monthly run and transfer
1. Notify the building/occupants and anyone affected by a transfer.
2. Start via the **ATS test function** (simulating mains failure) so the whole chain is
   exercised — start signal, start, voltage/frequency, transfer.
3. US NFPA 110 monthly test: run under load for **≥30 minutes** at a load that achieves
   the maker's minimum exhaust temperature **or ≥30% of nameplate kW** (gated: unconfirmed, source is paywalled or blocked).
4. Record: start time to rated voltage/frequency, voltage, frequency, kW/amps per phase,
   oil pressure, coolant temperature, any alarms.
5. Retransfer: ATS timers (return-to-mains delay, cool-down run) operate as set.

## 3. Load bank testing (annual, or when monthly loads are light)
- Diesel engines run lightly loaded for long periods suffer **wet stacking**: unburnt fuel
  and soot in the exhaust (black, oily drips at joints). Fix: run on a resistive load
  bank at stepped loads. NFPA 110 requires a supplemental load-bank test where monthly loading is
  insufficient; the load steps and durations differ between editions, so confirm them in
  the edition you work to.
- Connect via a load bank connection point/cabinet by a competent electrician; never
  over-load beyond rating.
- Some codes add a periodic multi-hour test (e.g. 4 h every 36 months for Level 1 in NFPA
  110; gated: unconfirmed, source is paywalled or blocked) — check edition.

## 4. Fuel
- Diesel degrades: water and microbial growth ("diesel bug") block filters. Drain water
  from tank sumps, test fuel annually, polish or treat as needed. Keep tanks topped up to
  limit condensation.
- Change fuel filters and water separators per hours/annual service.

## 5. UPS
- Daily/weekly: UPS on **normal/online**, no alarms, load % and runtime estimate
  recorded, room temperature (batteries age faster when warm; stay within the maker's limit).
- **Batteries (VRLA):** quarterly visual for swelling/leaks; measure string and cell/block
  voltage and **internal resistance/impedance** — trend it; a block whose impedance rises
  well above its peers or baseline (use the battery maker's threshold) is failing.
- Annual service by the maker: capacitor and fan checks, firmware, a controlled
  discharge/runtime test if the risk assessment allows.
- **Bypass:** know the procedure for maintenance bypass; transferring the wrong way can
  drop the critical load. Keep the procedure laminated at the UPS.

## Gotchas
- A successful no-load start proves the engine, not the system — test through the ATS
  with load.
- Generator in AUTO but the ATS in manual/inhibit = no transfer.
- Replace UPS blocks in matched strings, not singly from different batches, where possible.

## Verify
- [ ] Generator in AUTO, no alarms, batteries and heater checked weekly.
- [ ] Monthly loaded run via ATS logged with start time, kW and exhaust/load criteria.
- [ ] Load-bank test done when monthly loading is light; no wet-stacking signs.
- [ ] Fuel tested and water drained; filters in date.
- [ ] UPS battery impedance trended; bypass procedure posted; logs signed.

## Checked

Date checked: 2026-10-25. Jurisdiction: United States (NFPA 110) and United Kingdom (BS 7698 / ISO 8528); the edition in force and the OEM manual govern.
NFPA 110 is paywalled and the vendor pages found disagree on the annual load-bank steps (one gives 50 percent for 30 minutes then 75 percent for 1 hour, another gives stepped 25 to 100 percent), so the stepped schedule was replaced by a deferral to the edition in force. The monthly 30 minute and 30 percent of nameplate figures and the 36-month Level 1 test are marked gated. Removed unconfirmed battery heuristics (temperature halving, impedance percentage, VRLA service life).

Method: documentation only; no commands were run.
