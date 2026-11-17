---
id: repair-maintenance.appliance-repair.commercial-kitchen-equipment-repair.fryer-combi-oven-and-warewasher-service
name: fryer-combi-oven-and-warewasher-service
category: repair-maintenance
field: appliance-repair
product: commercial-kitchen-equipment-repair
tags: [appliance-repair, commercial-kitchen-equipment-repair, foodservice-equipment, commercial-fryer, high-limit, millivolt-fryer, thermopile, pilot, combi-oven, rational, steam-generator, descaling, water-treatment, warewasher, commercial-dishwasher, booster-heater, rinse-temperature, 180f, nsf-3, griddle, thermostat-calibration, refrigeration-case, cfesa, preventive-maintenance]
level: practitioner
status: draft
description: "Service commercial kitchen kit: millivolt gas fryers (pilot, thermopile, high-limit), combi oven steam and scale faults, warewasher wash/rinse temperatures, and preventive maintenance."
sources: ["NSF/ANSI 3 Commercial Warewashing Equipment (temperature requirements)", "FDA Food Code 4-501 (warewashing temperatures)", "CFESA technician training outline (general practice)"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Fryer, combi oven and warewasher service

**Goal:** get a commercial kitchen's critical equipment back in service fast and keep it
there. Downtime costs the operator money every hour, so diagnose methodically, carry the
common parts, and leave a preventive-maintenance note. Gas work requires the appropriate
licence (see `repair-maintenance.appliance-repair.gas-appliance-service.combustion-and-leak-testing-gas-appliances`);
lock out/tag out electrical supplies; **hot oil burns are severe** — work on fryers cold
or with extreme care.

## 1. Gas fryers (millivolt/standing-pilot type)
Many common open-pot fryers have no mains power at all: a pilot heats a **thermopile**
that powers the gas valve and thermostat circuit.
1. **Pilot won't stay lit:** pilot orifice dirty, low flame not heating the thermopile,
   or weak thermopile. Measure thermopile output with the pilot lit: open circuit typically
   ~500–750 mV; under load (valve circuit closed) a few hundred mV. Low → clean pilot,
   adjust pilot flame to envelop the thermopile tip, or replace.
2. **Pilot lit but burners won't come on:** the circuit runs through thermostat → high-limit
   → valve operator. Measure mV across each switch while calling for heat; a large drop
   across a closed switch (e.g. the high-limit) means it's open or failing.
3. **High-limit tripped/failed:** the high-limit (safety) shuts gas at ~ 450 °F/230 °C-ish
   (model-specific) to prevent oil fires. If it tripped, find out why (thermostat stuck
   closed, wrong calibration) before resetting; never bypass it.
4. **Thermostat calibration:** fill to the oil line, set e.g. 350 °F (177 °C), let it
   cycle 3 times, measure oil temperature with a calibrated probe 1 in (25 mm) below the
   surface near the thermostat bulb; adjust per the manual (calibration screw) to within a
   few degrees.
5. Burners: soot or lazy yellow flames → clean burner tubes and orifices, check air shutters.

## 2. Combi ovens (steam + convection)
- **Scale is the No. 1 enemy.** Boiler-type steam generators scale up without proper
  water treatment/softening; symptoms: slow steaming, boiler level sensor errors, overheat.
  Run the built-in descale programme (e.g. with the maker's descaler) and check the
  water filter/softener cartridge capacity versus local hardness.
- Boilerless (injection) combis: spray nozzle and fan wheel scale; clean per schedule.
- **Error codes** are detailed — use the manufacturer's service menu (often password-gated
  for service techs) for sensor readings: cavity temperature, core probe, boiler level,
  humidity sensor.
- Door gasket leaks steam → poor results and moisture damage to electronics; replace
  gaskets rather than adjusting hinges to compensate.
- Fan motor and cooling-fan faults cause overheating shutdowns; clean cooling air filters.

## 3. Warewashers (commercial dishwashers)
Sanitation is the spec, not cleanliness:
- **High-temperature machines:** wash tank typically ≥ 150–160 °F (66–71 °C) depending on
  type; **final rinse 180 °F (82 °C) at the manifold** (and ≤ 194 °F), produced by a
  **booster heater** (FDA Food Code / NSF 3 values — check the machine data plate).
  Verify with a maximum-registering thermometer or thermolabels run through on a rack.
- **Low-temperature chemical machines:** sanitise with chlorine (e.g. 50–100 ppm at
  stated temperature); verify with test strips; check the chemical pump tubing (peristaltic
  squeeze tubes wear out) and that drums aren't empty.
- Low rinse temp: booster element (resistance test), thermostat, contactor, scaled heater,
  or incoming water too cold for the booster's rise.
- Poor wash: clogged wash arms/strainers, low tank temperature, low detergent, worn wash pump.

## 4. Preventive maintenance (leave this behind)
- Fryers: boil-out schedule, filter oil daily, check flue clear.
- Combis: daily cleaning cycle, weekly descale checks, water filter changes.
- Warewashers: delime monthly or per hardness, check rinse arms and temperatures weekly.
- Refrigerated cases: clean condensers monthly in kitchens (grease + flour = fast clogging).

## Gotchas
- Operators often descale with the wrong acid (e.g. strong hydrochloric) — damages
  stainless and seals.
- Fryer oil temperature probes must be in oil, not touching the pot or element.
- Uncertain: temperatures/limits are typical published figures; data plates and local
  health codes govern.

## Verify
- [ ] Gas fryer: thermopile mV and switch drops measured; high-limit functional, not bypassed.
- [ ] Fryer thermostat within a few degrees of set point by calibrated probe.
- [ ] Combi descaled/water treatment checked; error history reviewed.
- [ ] Warewasher final rinse (or chemical ppm) proven on a rack test.
- [ ] PM recommendations recorded for the operator.
