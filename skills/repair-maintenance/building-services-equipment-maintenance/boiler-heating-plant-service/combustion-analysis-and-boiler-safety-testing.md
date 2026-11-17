---
id: repair-maintenance.building-services-equipment-maintenance.boiler-heating-plant-service.combustion-analysis-and-boiler-safety-testing
name: combustion-analysis-and-boiler-safety-testing
category: repair-maintenance
field: building-services-equipment-maintenance
product: boiler-heating-plant-service
tags: [building-services-equipment-maintenance, boiler-heating-plant-service, boiler, commercial-boiler, combustion-analysis, flue-gas-analyser, o2, co2, co, excess-air, flue-temperature, combustion-efficiency, burner-service, gas-burner, condensing-boiler, low-water-cutoff, lwco, pressure-relief-valve, safety-valve, flame-safeguard, flame-signal, hydronic, delta-t, gas-safe, heating-plant]
level: practitioner
status: gated
description: "Service a commercial gas boiler: flue-gas analysis (O2, CO2, CO, flue temp) to the maker's window, burner clean and set-up, low-water cutoff and relief valve tests, hydronic checks."
sources: ["https://www.hse.gov.uk/gas/domestic/faqs.htm", "https://www.gassaferegister.co.uk/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Combustion analysis and boiler safety testing

**Goal:** a boiler that burns clean and efficiently inside the maker's combustion window,
with every safety device proven to work. Gas and pressure-vessel work is regulated:
in the UK only Gas Safe registered engineers with the right commercial categories; in
the US state licensing and boiler-inspector rules apply. Follow the boiler maker's
manual — numbers below are typical, not universal.

## 1. Before firing
- Check the plant room: combustion air vents clear and correctly sized, no stored
  combustibles, flue route intact, gas detection/emergency shut-off valve working.
- Check system pressure (to the design value), expansion
  vessel pre-charge, pumps running, flow through the boiler proven.
- Visual: burner, refractory, heat exchanger, flue and condensate trap (condensing boilers)
  — a blocked trap can lock out the boiler or spill flue gas.

## 2. Combustion analysis
1. Use a calibrated flue-gas analyser (calibration in date). Zero it
   in fresh air, outdoors or away from the flue.
2. Sample at the **test point** in the flue, centre of the gas stream, after the boiler
   has run at steady state for several minutes.
3. Test at **high fire and low fire** (and mid-fire for modulating burners).
4. Record: O₂ %, CO₂ %, CO ppm, flue temperature, ambient temperature, calculated
   efficiency and excess air, draught (for atmospheric/open-flue appliances).
5. Compare to the maker's window. O₂, CO₂ and CO limits are model-specific; premix
   condensing boilers have tight CO₂ ranges for high and low fire.
6. **Adjust only per the manual:** gas valve offset/throttle and air damper/fan speed. Too
   little air → CO rises sharply; too much → efficiency falls (more heat to flue).
7. **CO/CO₂ ratio** above the maker's or the standard's limit (gated: unconfirmed, source is paywalled or blocked)
   indicates poor combustion — investigate, don't just tweak.

## 3. Burner service
Isolate gas and electrics, then clean or replace the ignition and ionisation electrodes
(set gaps to spec), clean the burner head/premix burner face, check the fan and air
inlet, replace gaskets you disturb. Check the **flame signal** (µA reading on the flame
safeguard) is in range — weak signal = dirty probe or poor ground.

## 4. Safety device tests
- **Flame failure:** with the burner firing, close the gas or remove the flame signal;
  the safeguard must lock out within its rated safety time.
- **Low-water cutoff (steam and some hot-water boilers):** float-type — blow down to
  remove sediment and confirm the burner cuts out; probe-type — test per maker. Steam
  boilers are often tested daily/weekly per local code.
- **High-limit / overheat stat:** raise setpoint or simulate; confirm lockout and manual reset.
- **Pressure relief valve:** lift-test per maker/code (with discharge safely piped), check it
  reseats; replace if it weeps or is overdue.
- **Gas pressure switches and valve proving systems** (larger burners): test per maker.
- **Gas tightness** on the installation pipework to the required standard.

## 5. Hydronic checks
Boiler ΔT (flow − return) against design; a small ΔT at full fire suggests excess flow,
a large one low flow. Condensing boilers only condense when return water is cool enough
(see the maker's data) — high returns waste their advantage. Check water treatment levels (inhibitor) and strainers.

## Gotchas
- Analysing before the boiler stabilises gives misleading readings.
- Never bypass a safety device to keep heat on — lock out and report.
- Readings "in window" with a CO spike on startup can mean a delayed ignition; watch it light.

## Verify
- [ ] Analyser calibration date checked; zeroed in fresh air.
- [ ] High- and low-fire readings recorded and within the maker's window.
- [ ] Flame failure, high limit, LWCO and relief valve tests recorded with result.
- [ ] Flame signal in range; no gas leaks on test.
- [ ] Service record/certificate completed with all readings.

## Checked

Date checked: 2026-10-25. Jurisdiction: United Kingdom (Gas Safe) and United States (state licensing); the boiler maker's manual governs.
HSE gas pages (via search results): work on gas fittings in domestic and workplace premises must be done by a Gas Safe registered engineer qualified for it. The CO/CO2 ratio action level could not be confirmed because the Gas Safe Technical Bulletin 143 page returned a bot-block page, so the figure is gated; the reason is that the source is blocked. Removed unconfirmed typical figures: O2/CO2/CO ranges, cold system pressure, boiler delta-T, condensing return temperature, analyser calibration interval, flame-failure timing.

Method: documentation only; no commands were run.
