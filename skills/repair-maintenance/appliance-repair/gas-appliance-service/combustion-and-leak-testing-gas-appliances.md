---
id: repair-maintenance.appliance-repair.gas-appliance-service.combustion-and-leak-testing-gas-appliances
name: combustion-and-leak-testing-gas-appliances
category: repair-maintenance
field: appliance-repair
product: gas-appliance-service
tags: [appliance-repair, gas-appliance-service, gas-safety, gas-leak-test, tightness-test, manometer, inlet-pressure, burner-pressure, flue-gas-analyser, co, co2-ratio, combustion-analysis, flame-picture, thermocouple, flame-failure-device, ffd, flame-rectification, gas-valve, natural-gas, lpg, propane, conversion-kit, gas-safe, nfpa-54, leak-detection-fluid]
level: advanced
status: docs-checked
description: "Service gas cookers, dryers and heaters safely: tightness test, inlet/burner pressure by manometer, flame picture, flame-failure checks and flue-gas CO/CO2 analysis. Licensed work."
sources: ["https://www.hse.gov.uk/gas/domestic/faqs.htm", "https://www.hse.gov.uk/gas/employers.htm"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Combustion and leak testing of gas appliances

**Goal:** leave a gas appliance leak-free, burning cleanly at the right pressure, with
working flame safety. **Legal:** in the UK only Gas Safe registered engineers may work on
gas fittings; in the US/Canada, licensing is by state/province (often a gas fitter or
licensed appliance tech). Many jurisdictions forbid homeowner gas work. This is the
procedure outline for qualified technicians.

## 0. Smell of gas on arrival
Don't operate switches; ventilate; isolate at the meter/ECV; evacuate if strong; call the
gas emergency number. Diagnose only after the area is safe.

## 1. Tightness (leak) test
- Before and after any work that disturbs gas pipework or connections.
- UK domestic (IGEM/UP/1B style): isolate, connect a manometer to the meter test point,
  let-by test (does the meter valve pass?), then raise to operating pressure,
  isolate, stabilise, then test for the period and permitted drop in the current standard
  — and no smell of gas.
- US: soap/approved leak-detection solution on every disturbed joint with gas on;
  pressure test new piping per NFPA 54 and local code; electronic combustible gas
  detector for hard-to-reach joints.
- Never test with a flame.

## 2. Pressure checks (manometer)
- **Inlet (working) pressure** at the appliance inlet test point with all appliances in
  the house running: natural gas and LP have different working pressures — read the data plate and the
  national standard. Low working pressure → undersized pipe or regulator issue upstream.
- **Burner (manifold) pressure** downstream of the appliance regulator: compare to the data
  plate. Adjust only where the appliance has an
  adjustable regulator and the data plate gives a value.
- **Fuel type:** NG vs LP use different orifices and regulator springs. Converting requires
  the manufacturer's conversion kit; an NG appliance on LP will over-fire dangerously.

## 3. Flame picture and burners
- Natural gas: crisp blue cones, slight orange tips acceptable (dust, humidity), no
  lazy, yellow, sooting or lifting flames.
- Yellow/sooting → insufficient primary air (blocked air shutter, spider webs in venturi),
  wrong orifice, or over-pressure. Lifting/blowing → over-aeration or high pressure.
- Clean burner ports with a soft wire brush or appropriately sized drill held by hand;
  never enlarge orifices.

## 4. Flame-failure / flame-supervision devices
- **Thermocouple (cookers, older fires, some ovens):** the thermocouple generates
  millivolts in the flame; the magnet unit holds the valve open at a lower value. Test
  open-circuit mV with a meter and adapter against the maker's value; replace if weak. Hob
  FFDs should close the gas within the time the standard allows after the flame is blown out.
- **Flame rectification** (dryers, modern ovens, boilers): microamp DC signal through the flame;
  low µA → dirty sensor rod (clean with fine abrasive pad) or poor burner ground.
- Never bypass or wedge an FFD.

## 5. Combustion analysis (where the appliance has a flue or a CO test is required)
- Calibrated flue-gas analyser (in date, auto-zeroed in fresh air).
- Measure CO ppm, CO2 %, and the **CO/CO2 ratio**; compare to the appliance's
  manufacturer limits or the standard (confirm the ratio limit for the appliance type in
  the manufacturer's data or current Gas Safe guidance).
- For cookers, room CO testing per the relevant standard if a fault is suspected (close
  windows, run burners/oven for the defined time, monitor room CO).
- Check flue spillage on open-flued appliances with a smoke match/pellet at the draught diverter.

## Gotchas
- A good flame and a bad flue still kill: open-flued appliances need spillage testing.
- Rubber hoses on cookers perish and kink; use the correct bayonet hose length and
  stability bracket/chain for free-standing cookers.
- Uncertain: pressures and limits quoted are typical; national standards and data plates govern.

## Verify
- [ ] Tightness test passed before and after work; no smell of gas; all disturbed joints leak-checked.
- [ ] Inlet working pressure and burner pressure within data-plate values; correct fuel/orifices.
- [ ] Flames stable and blue; burners and venturis clean.
- [ ] Flame-failure device shuts off within allowed time.
- [ ] Combustion/CO and spillage checks within limits; record/certificate completed.

## Checked

Date checked: 2026-10-25. Jurisdiction: United Kingdom (Gas Safe) and US/Canada (state or provincial licensing); national standards and the data plate govern.
HSE gas pages (via search results): work on gas fittings in domestic properties and workplaces must be carried out by a Gas Safe registered engineer qualified for it and it is illegal for anyone else to do it. The pressure figures, tightness test timings, thermocouple millivolt output, flame-failure times and CO/CO2 ratio levels could not be confirmed on a free official page (Gas Safe TB 143 returned a bot-block page), so they were removed and the skill now defers to the data plate, manufacturer and current national standard.

Method: documentation only; no commands were run.
