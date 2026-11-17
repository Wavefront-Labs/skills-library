---
id: agriculture-environment.irrigation-water-management.irrigation-pumps-systems.centrifugal-pump-checks-and-season-startup
name: centrifugal-pump-checks-and-season-startup
category: agriculture-environment
field: irrigation-water-management
product: irrigation-pumps-systems
tags: [irrigation-pumps-systems, irrigation-pump, centrifugal-pump, submersible-pump, turbine-pump, priming, foot-valve, suction-lift, npsh, cavitation, pump-curve, duty-point, pressure-gauge, flow-meter, water-hammer, mechanical-seal, gland-packing, check-valve, air-valve, vfd, variable-speed-drive, pump-efficiency, energy-cost, winterisation, irrigation-controller]
level: practitioner
status: gated
description: "Start up and keep irrigation pumps healthy: priming, NPSH and cavitation signs, duty-point checks with gauges and flow meter, seals, valves and winter lay-up."
sources: ["https://www.hydraulicinstitute.org/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Centrifugal pump checks and season start-up

**Goal:** get the irrigation pump running safely at the start of the season and spot
the slow killers — cavitation, worn impellers, air leaks — before they cost a crop or
a power bill.

## 1. Before first start
1. **Isolate power** (lock-out/tag-out) before touching anything.
2. Inspect suction: intake screen clear and well below the water surface (rule of thumb
   ≥ 3–4 × pipe diameter of submergence (gated: unconfirmed, source is paywalled or blocked) to avoid vortexing), foot valve free, suction
   pipe joints tight. **Any air leak on the suction side** wrecks priming and output.
3. Check the shaft turns freely by hand; check coupling alignment and guard in place.
4. Lubricate bearings per the maker (don't over-grease — that overheats them).
5. Check electrical: motor terminals tight, overloads set to the motor's nameplate
   full-load current, earth connected. Diesel: oil, coolant, fuel filter, belts.

## 2. Priming and starting (surface-mounted, suction lift)
1. Fill pump casing and suction line with water through the priming plug until no air
   bubbles appear (or run the vacuum primer).
2. **Start against a partly closed delivery valve** (for most centrifugal pumps) to
   limit start-up current and water hammer, then open slowly as pressure builds. Never
   run it dry or with the delivery valve shut for more than a minute or two — it heats
   up and wrecks seals.
3. Fill long pipelines slowly to push air out through air valves; a fast fill traps air
   that later causes surges.
4. **Check rotation** on a new or rewired motor (three-phase can be wired backwards —
   pump runs, but at a fraction of output).

## 3. Know your duty point
Fit a **suction gauge** (vacuum/compound) and **delivery pressure gauge** close to the
pump, plus a flow meter on the main. Record a baseline at the start of each season:
flow (L/s), delivery pressure (kPa), suction reading, motor current (A) or diesel rpm.
- Plot flow vs total head on the pump's published curve. You should land near the
  **best efficiency point (BEP)**. Far to the right (high flow, low head) overloads the
  motor; far to the left wastes energy and stresses bearings.
- **Total head** ≈ delivery pressure (in metres; 1 bar ≈ 10.2 m) + suction lift +
  friction. A 10–15% drop in flow (gated: unconfirmed, source is paywalled or blocked) at the same head versus last year's baseline suggests
  impeller/wear-ring wear.

## 4. Cavitation and NPSH
Cavitation sounds like **gravel rattling** in the pump. Causes: suction lift too high,
suction pipe too small/long, clogged screen, or water too warm. The pump's required
NPSH (from its curve) must be less than the available NPSH. Practical fixes: lower the
pump closer to the water, shorten/enlarge the suction pipe, clean the screen, throttle
flow back. Ongoing cavitation pits the impeller within a season.

## 5. Routine (in season)
- **Weekly:** read gauges, flow and current — compare with baseline; look for leaks,
  unusual noise, vibration or bearing heat (hand on housing: too hot to hold is a fault).
- **Gland packing** should drip slowly (tens of drops per minute) to cool itself — don't
  tighten it dry. **Mechanical seals** should not leak at all.
- Check filters' pressure drop, check valves for slamming (water hammer), air valves
  for sticking.
- **Variable speed drives (VFD):** check the set pressure and that the drive isn't
  sitting at maximum all the time (a sign of a leak or demand increase).
- **Controllers:** confirm the clock, the station run times, rain shut-off and that the
  pump-start relay actually starts the pump on the first station.

## 6. End-of-season lay-up
Drain the pump casing and exposed pipework where freezing occurs (open drain plugs),
leave valves partly open, protect motors from damp and rodents, fog diesel engines per
the maker, and write down any faults while you remember them.

## Gotchas
- A pump that "lost its prime overnight" usually has a leaking foot valve or a suction
  air leak — find it with soapy water or by listening while running.
- Energy is often the biggest pumping cost: a pump test by a qualified tester can show
  if replacing an impeller pays.
- Specific figures (submergence, drip rate) are general rules **not checked against
  any particular pump** — your maker's manual wins.

## Verify
- [ ] Rotation correct; no air bubbles in priming; suction leak-free.
- [ ] Baseline flow, head, current recorded and plotted on the pump curve near BEP.
- [ ] No cavitation noise at normal operation.
- [ ] Weekly readings within ~10% of baseline, or the cause investigated.
- [ ] Lay-up checklist done before frosts.

## Checked

- Date: 2026-10-25. Jurisdiction: no regulation involved; follow the pump maker's manual and local electrical rules.
- Confirmed against: the head conversion was recomputed (1 bar = 100 kPa / (1000 kg/m3 x 9.81 m/s2) = 10.2 m of water).
- Not confirmed: the intake submergence rule of thumb and the flow-drop trigger (Hydraulic Institute standards are paywalled).

Method: documentation only; no commands were run.
