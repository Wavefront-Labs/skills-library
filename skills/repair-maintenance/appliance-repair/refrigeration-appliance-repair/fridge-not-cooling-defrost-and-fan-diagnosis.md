---
id: repair-maintenance.appliance-repair.refrigeration-appliance-repair.fridge-not-cooling-defrost-and-fan-diagnosis
name: fridge-not-cooling-defrost-and-fan-diagnosis
category: repair-maintenance
field: appliance-repair
product: refrigeration-appliance-repair
tags: [appliance-repair, refrigeration-appliance-repair, refrigerator, fridge, freezer, frost-free, defrost-heater, defrost-thermostat, defrost-timer, adaptive-defrost-control, evaporator-fan, condenser-fan, condenser-coils, start-relay, ptc-relay, compressor, ice-maker, door-gasket, thermistor, temperature, sealed-system, frost-pattern]
level: practitioner
status: draft
description: "Find why a frost-free fridge is warm while the freezer is cold (or both warm): frost pattern, evaporator and condenser fans, defrost heater/thermostat/timer, start relay, and when it's sealed-system."
sources: ["Manufacturer tech sheets and service manuals (general structure)", "Author's synthesis; values vary by model"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Fridge not cooling: defrost and fan diagnosis

**Goal:** localise a cooling complaint in a domestic frost-free refrigerator to airflow,
defrost, compressor start, or sealed system — and only call it sealed-system once the
cheaper causes are ruled out. Unplug before touching anything inside the machine compartment.

## How a frost-free fridge works (why the order below)
The compressor and evaporator are usually in/behind the **freezer**. An **evaporator fan**
blows cold air over the coil into the freezer and, through a damper/duct, into the fresh
food section. Every 8–12 hours (or adaptively) a **defrost heater** melts frost off the
coil, controlled by a timer or board and limited by a **defrost thermostat/bi-metal**.
So: "freezer cold, fridge warm" almost always means airflow from the freezer is blocked.

## 1. Quick checks (5 minutes)
- Thermometer in a glass of water on the middle shelf after 24 h: target ~3–4 °C
  (37–40 °F) fridge, −18 °C (0 °F) freezer.
- Controls set correctly; not in demo/showroom mode (lights on, no cooling — common
  after moving or a board reset; exit per the manual).
- Door gaskets seal (a paper slip should drag when the door is closed on it). Overpacked
  shelves blocking vents.
- **Condenser coils** (underneath or back) clogged with dust/pet hair → vacuum and brush;
  **condenser fan** (on most under-mount compressors) must run when the compressor runs.

## 2. Look at the evaporator (the decisive check)
Remove the freezer's rear panel (unplug first; there may be a fan and wiring attached).
- **Coil solid with white frost/ice, fan blocked** → defrost failure. Go to step 3.
- **Coil frosted evenly and lightly, fan not spinning** → evaporator fan motor (spin it
  by hand: stiff, noisy or no voltage during a cooling call).
- **Coil frosted only on the first loop or two (near the inlet), rest bare** → low
  refrigerant/restriction → sealed system (see the sealed-system skill
  `repair-maintenance.appliance-repair.sealed-system-refrigerant-service.leak-search-evacuation-and-charging`).
- **Coil completely bare and compressor running** → no refrigeration: compressor not
  pumping or sealed-system fault.
Manually defrost a solidly iced coil (door open, towels, a hair dryer used gently or just
time) — the fridge will work for a few days and then fail again, which confirms defrost.

## 3. Defrost system tests (unplugged, components disconnected)
- **Defrost heater** (glass tube or metal sheath under the coil): resistance commonly in
  the tens of ohms (e.g. ~20–50 Ω — compute from wattage: R = V²/W; 120 V, 450 W ≈ 32 Ω).
  Open = failed.
- **Defrost thermostat/bi-metal:** closed (continuity) only when cold — test it below
  about −5 °C (still frozen, or chilled); at room temperature it's normally open.
- **Defrost timer** (mechanical, older units): turn the slot slowly until it clicks into
  defrost; the compressor should stop and the heater warm. If the heater then works, the
  timer has failed. Adaptive control boards: run a **forced defrost** from the service mode.
- **Drain:** a blocked defrost drain freezes into an ice sheet at the freezer floor;
  flush with warm water and clear the drain tube.

## 4. Compressor won't start (clicking every few minutes)
- Click-click-hum then silence = start device or compressor. Remove the **start relay/PTC**
  from the compressor pins; shake — rattling = cracked; measure (PTC should read a few
  ohms cold).
- Compressor windings: measure common–start, common–run and start–run (start + run ≈
  start–run sum), and each pin to the casing (should be open/very high). Shorted to ground
  or open winding → compressor replacement (sealed-system work).

## 5. Ice maker not making ice (separately)
Water supply valve open, filter not clogged, freezer cold enough (ice makers often
need ≤ −15 °C), shut-off arm down, then the inlet valve coil and fill tube for ice blockage.

## Gotchas
- Don't chip ice off a coil with tools — puncturing an evaporator ends the fridge.
- Bypassing the defrost thermostat to "test" the heater can overheat plastic liners.
- Uncertain: frost-pattern rules are well established heuristics but not definitive; confirm
  sealed-system diagnosis with gauges.

## Verify
- [ ] Temperatures measured with a thermometer, not the dial setting.
- [ ] Condenser clean and fans running during a cooling call.
- [ ] Evaporator frost pattern observed and classified.
- [ ] Defrost heater, thermostat and timer/board tested by measurement.
- [ ] After repair, fridge reaches target temperature within 24 h and survives a defrost cycle.
