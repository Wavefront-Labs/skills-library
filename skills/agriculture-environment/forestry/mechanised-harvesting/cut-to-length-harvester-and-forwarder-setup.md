---
id: agriculture-environment.forestry.mechanised-harvesting.cut-to-length-harvester-and-forwarder-setup
name: cut-to-length-harvester-and-forwarder-setup
category: agriculture-environment
field: forestry
product: mechanised-harvesting
tags: [forestry, mechanised-harvesting, cut-to-length, ctl, harvester, harvester-head, forwarder, skidder, bucking, value-bucking, optimisation, stanford-2010, pin-file, hpr, length-calibration, diameter-calibration, feed-rollers, delimbing-knives, john-deere-timbermatic, ponsse-opti, komatsu-maxixplorer, load-management, forwarder-loading, brash-mat, rutting]
level: practitioner
status: draft
description: "Set up and run cut-to-length harvesting: load product specs/price matrix, calibrate length and diameter measurement, tune head pressures, and load a forwarder for stability and clean sorting."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Cut-to-length harvester and forwarder setup

**Goal:** a harvester that cuts the right products to within tolerance, and a forwarder
that moves them to roadside sorted, stable and without wrecking the ground.

> Draft. Control-system names and menus differ (John Deere TimberMatic H, Ponsse Opti,
> Komatsu MaxiXplorer, etc.) and change by version — the principles below hold; use the
> manufacturer's manual for exact screens. StanForD 2010 is the common data standard.

## 1. Product specifications (bucking instructions)
The mill/customer gives you, per species:
- Assortments: e.g. sawlog 4.9 m, 3.7 m; small sawlog; pulp/chip 3.0 m; firewood.
- Length tolerances (often −0/+10 cm over nominal), minimum top diameter, max butt diameter.
- Quality rules: max sweep, rot, knot size, forks.
- Price or value matrix by length × diameter class.
In StanForD 2010 these travel as a **product instruction file (.pin)** / price matrix,
and production comes back as **.hpr** (harvested production) and **.mom** (operational
monitoring) files. Load them, then check on the screen that every product has the right
length list and diameter limits before the first stem.

## 2. Calibration — do it at the start of every site and weekly
- **Length:** measuring wheel encoder. Cut 10–20 logs, measure with a tape at the
  shortest side, enter the controls into the calibration routine. Target: ≥ 90–95% of
  logs within tolerance. Check after changing wheel or on frozen/very wet bark.
- **Diameter:** the head's delimbing knives/feed rollers measure via potentiometers/
  encoders. Caliper logs at defined points (e.g. 1.3 m from butt and mid), compare with
  the machine's reading, calibrate. Bark thickness tables must match the species and season.
- Keep the calibration log — buyers may audit it.

## 3. Head settings to tune
- **Feed roller pressure:** enough to grip without crushing; high pressure on thin-barked
  species in sap season strips bark and marks sawlogs. Many systems vary pressure by diameter.
- **Delimbing knife pressure:** raise for heavy-branched stems, lower for clean stems to save fuel and bark.
- **Feed speed / acceleration:** too aggressive → wheel slip → length errors.
- **Saw chain/bar:** sharp chain, correct tension and oil; the saw-return sensor must work.
- **Colour marking** (if fitted) per product so forwarder operator can sort.

## 4. Working method (harvester)
- Work from racks (see harvest-coupe-and-extraction-planning); process in front of the
  machine and lay brash on the rack ahead for the machine to drive on.
- Pile each product separately on alternating sides or in distinct heaps, butts aligned,
  at right angles to the rack, within forwarder crane reach.

## 5. Forwarder loading
- One product per load where possible; if mixed, separate with stakes/bunks and record.
- Load evenly, **heaviest logs at the bottom and toward the front bunk**, logs not
  protruding past the load gate/headboard, top below the stake tops.
- Do not exceed rated payload; on slopes, travel loaded downhill, turn on level ground.
- Use bogie tracks on soft ground; reduce tyre pressure if the machine allows.
- At roadside: one product per stack, square faced ends, stacks back from the road edge.

## Gotchas
- A wrong bark-thickness table quietly shifts every log into a lower diameter class.
- After a long shift, compare the machine's volume to tape-measured truckloads; drift shows up there first.
- Rutting stops (usually ~20–30 cm or water in ruts) apply to the forwarder far more
  than the harvester — it makes many more passes.

## Verify
- [ ] Product file loaded and visually checked per species and assortment.
- [ ] Length and diameter calibrated today; ≥ 90% of sample logs in tolerance.
- [ ] Head pressures checked against bark damage on sample logs.
- [ ] Piles single-product, butts aligned, within crane reach; brash on racks.
- [ ] Forwarder loads within payload, below stake tops, stacked by product at roadside.
