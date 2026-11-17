---
id: energy-mining-utilities.mineral-mining.continuous-miner-longwall.operating-a-longwall-face-and-continuous-miner
name: operating-a-longwall-face-and-continuous-miner
category: energy-mining-utilities
field: mineral-mining
product: continuous-miner-longwall
tags: [continuous-miner-longwall, longwall, longwall-mining, shearer, shearer-operator, powered-roof-support, chock, shield, leg-pressure, setting-pressure, yield-pressure, afc, armoured-face-conveyor, beam-stage-loader, bsl, face-alignment, horizon-control, tailgate, maingate, goaf, continuous-miner, place-change, bolter-miner, shuttle-car, methane-monitoring, water-sprays, coal-mining]
level: practitioner
status: docs-checked
description: "Operate coal-cutting systems: shearer cutting cycle, powered roof support advance and setting pressure, AFC snaking and alignment, and continuous miner place-change cutting."
sources:
  - "https://www.ecfr.gov/current/title-30/part-75/section-75.202"
  - "https://www.ecfr.gov/current/title-30/part-75/section-75.342"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Operating a longwall face and continuous miner

**Goal:** cut coal steadily while keeping the roof supported, the face straight, and gas
and dust under control.

> Equipment varies greatly (Joy/Komatsu, Caterpillar, Eickhoff and others);
> control systems, setpoints and procedures come from the OEM and your mine's
> procedures. Treat the numbers here as illustrative.

## 1. Longwall: the cutting cycle
- The **shearer** travels along the face on the **armoured face conveyor (AFC)**,
  cutting with two ranging drums. A common pattern is **bi-directional** cutting or
  uni-directional with a cleanup pass; each full pass advances the face by one web.
- The **lead drum** usually cuts the top (roof horizon), trailing drum the bottom.
  **Horizon control:** leave the right amount of coal or cut to the specified roof/floor
  horizon. Cutting into stone wears picks, creates sparks (frictional ignition risk in
  gas) and dilutes product.
- Drum water sprays must be working before cutting — they suppress dust and incendive
  sparking. No water, no cutting.

## 2. Powered roof supports (shields/chocks)
- Behind the shearer, each support is **lowered slightly, advanced** toward the face,
  and **reset** against the roof. Automated systems do this in sequence (shearer-
  initiated); operators monitor and intervene.
- **Setting pressure** is the pressure the legs are set to on the roof; **yield
  pressure** is where the relief valve opens. Supports that don't reach setting
  pressure give poor roof contact and let the roof fracture ahead of them — watch for
  low-pressure legs on the display and fix the cause (leaking hoses, a damaged leg,
  rubbish on top of the canopy).
- Keep the **tip-to-face distance** small; advance supports promptly behind the
  shearer, especially in weak roof. Sprags/face guards swing out to support the face
  where specified.
- The AFC is "**snaked**" over behind the shearer by the support push rams.

## 3. Face alignment and conveyors
- Keep the face straight; a crooked face loads supports unevenly, stretches the AFC
  chain and makes the shearer climb or dive. Modern systems use inertial navigation
  data from the shearer for automated alignment.
- At the **maingate**, the AFC delivers to the **beam stage loader** and crusher, then
  the belt. Watch chain tension and sprocket wear; a stalled AFC under a full load is
  a long delay.

## 4. Gas and the tailgate
Methane comes from the cut coal and the goaf. Monitors on the shearer and at the
tailgate trip power at statutory levels (US coal: 30 CFR 75.342 methane monitors give a warning signal at 1.0% and deenergize at 2.0%; 30 CFR 75.323 sets further action levels). Check the tailgate is ventilated and not
accumulating gas; goaf gas may spill out on barometric pressure drops.

## 5. Continuous miner (development)
- The miner cuts a heading in a **cut sequence** (sump in at the roof, shear down to
  the floor), loading coal via its gathering arms onto a conveyor or **shuttle car**.
- **Place change:** cut the allowed distance, then move the miner to another heading
  while bolting crews support the first. Bolter-miners combine cutting and bolting.
- Nobody works or travels under unsupported roof except as the roof control rules allow (US coal, 30 CFR 75.202(b)); cut no further than the distance in the approved roof control plan, and run the miner on remote control from supported roof where it is fitted. Keep the scrubber and sprays running.

## Gotchas
- Pinch points between supports and the AFC kill people — stay out of the travel path
  during advance; use isolation for work in the face.
- Hydraulic emulsion at high pressure: injection injuries are serious even from small leaks.
- Roof falls often start where support advance lagged after a delay.

## Verify
- [ ] Sprays and gas monitors working before cutting.
- [ ] Supports at or above setting pressure; tip-to-face distance kept small.
- [ ] Horizon and face alignment checked each pass/shift.
- [ ] Tailgate ventilation and gas readings within limits.
- [ ] Miner never cutting beyond supported roof distance limits.

## Checked

Date checked: 2026-10-25. Jurisdiction: United States, underground coal (MSHA, 30 CFR Part 75).

Sources: https://www.ecfr.gov/current/title-30/part-75/section-75.202; https://www.ecfr.gov/current/title-30/part-75/section-75.342 (versions: current eCFR and web pages as read on the date above).

Confirmed: 75.202(a): roof, face and ribs where persons work or travel are supported or otherwise controlled; 75.202(b): no person works or travels under unsupported roof except as the subpart allows. 75.342: methane monitors warn at 1.0% and deenergize at 2.0% (or when not operating properly).

Method: documentation only; no commands were run.
