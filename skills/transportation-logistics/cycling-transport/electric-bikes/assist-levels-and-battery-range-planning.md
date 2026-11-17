---
id: transportation-logistics.cycling-transport.electric-bikes.assist-levels-and-battery-range-planning
name: assist-levels-and-battery-range-planning
category: transportation-logistics
field: cycling-transport
product: electric-bikes
tags: [cycling-transport, electric-bikes, e-bike, ebike, pedelec, s-pedelec, class-1, class-2, class-3, pedal-assist, assist-level, eco-mode, turbo-mode, mid-drive, hub-motor, bosch, shimano-steps, yamaha, bafang, battery, watt-hours, wh, range, range-planning, charging, lithium-ion, battery-care, battery-fire, cadence, gear-shifting, delivery-riding, commuting]
level: intro
status: gated
description: "Plan e-bike range from battery watt-hours, pick assist levels and cadence that stretch it, charge and store lithium batteries safely, and ride a faster, heavier bike."
sources: ["https://uscode.house.gov/view.xhtml?req=granuleid:USC-prelim-title15-section2085&num=0&edition=prelim", "https://eur-lex.europa.eu/eli/reg/2013/168/oj/eng", "https://www.gov.uk/government/publications/european-type-approval-for-certain-electrically-assisted-pedal-cycles-eapc/guidance-on-european-type-approval-for-certain-electrically-assisted-pedal-cycles-eapc"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Assist levels and battery range planning (e-bikes)

**Goal:** never run flat halfway through a shift or commute, keep the battery healthy
for years, and ride a 25 kg bike at 25–45 km/h with matching hazard margins.

> Draft: general pedelec practice. Legal classes differ (EU pedelec: motor of at most 250 W continuous rated power, assist cutting out at 25 km/h, outside type approval under Reg. 168/2013; faster or stronger bikes fall into L1e vehicle categories; US federal low-speed e-bike: motor under 750 W, under 20 mph on motor alone, 15 USC 2085; the Class 1/2/3 limits of 20/20/28 mph are state conventions (gated: unconfirmed, source is paywalled or blocked)).
> Consumption figures are estimates; measure your own.

## 1. Range from watt-hours
- Battery capacity is in **Wh** (e.g. 500 Wh, 625 Wh, 750 Wh).
- Consumption is commonly ~**5–10 Wh/km** on flat ground in low-to-mid assist, up to
  **15–25 Wh/km** in turbo, hills, headwind, heavy loads, or cold (consumption figures are rules of thumb (gated: unconfirmed, source is paywalled or blocked)).
- Range ≈ Wh ÷ Wh/km. Example: 500 Wh at 8 Wh/km ≈ 60 km; in turbo with cargo at
  18 Wh/km ≈ 28 km.
- **Measure yours**: note % used over a known route; most displays (Bosch, Shimano
  STEPS, etc.) also show estimated range per mode — trust the trend, not the number.
- Plan with a **20% reserve** (a rule of thumb (gated: unconfirmed, source is paywalled or blocked)); batteries lose capacity in the cold (below ~5 °C range can
  drop noticeably) and with age.

## 2. Assist strategy
- Use the **lowest assist that keeps you comfortable**; switch to high only for
  climbs, starts with load, or gaps in traffic.
- **Cadence matters** on mid-drive bikes: ~70–90 rpm keeps the motor efficient; grinding
  a high gear at 50 rpm wastes battery and stresses the drivetrain.
- Shift down **before** stopping, and ease pressure when shifting under assist to save
  the chain and cassette (some systems have shift sensors; don't rely on them).
- Delivery shifts: start the day in eco, keep turbo for the last stretch when you know
  what's left.

## 3. Charging and battery care
- Charge with the **original charger**, on a hard, non-flammable surface, in a room with
  a smoke alarm, not blocking an exit, and not unattended overnight if avoidable.
- Daily use: charging to ~80–90% and avoiding running to 0% extends lifespan (if the
  system offers a charge limit, use it).
- Storage over weeks: ~30–60% charge, cool dry place (~10–20 °C) (gated: unconfirmed, source is paywalled or blocked).
- Don't charge a battery that's below freezing — let it warm to room temperature first.
- **Damaged battery** (dropped hard, swollen, smells, hot, hissing): stop using it,
  put it outside away from buildings if safe, and contact the manufacturer. Never use
  uncertified replacement packs or chargers — a leading cause of e-bike fires.
- Delivery riders: a second battery is cheaper than downtime; keep spares charged and
  cool.

## 4. Riding a faster, heavier bike
- Others misjudge your speed: drivers and pedestrians expect "bicycle speed". Assume
  they will pull out.
- Brake earlier: more mass, more speed. Hydraulic discs recommended; pads wear faster.
- Corners: carry less speed in; heavier bikes push wide.
- Starts: hold the brake while clipping in/placing feet — high-torque assist can lurch
  when you push the first pedal, especially in turbo.
- Walk-assist mode for ramps and pushing uphill.

## 5. Maintenance specific to e-bikes
- Chain and cassette wear faster: check chain stretch every ~500–1,000 km.
- Keep contacts clean and dry; don't pressure-wash the motor or battery.
- Firmware updates via the dealer or app (Bosch Flow, Shimano E-Tube).

## Gotchas
- Range estimates jump between modes — the display recalculates; the battery isn't
  draining faster than usual.
- Tampering/"tuning" to remove the speed limit can make the bike illegal and void
  warranties and insurance.
- Batteries are heavy and valuable: remove them when locking in public.

## Verify
- [ ] You know your Wh/km on your regular route in your usual mode.
- [ ] Trip plan includes a 20% battery reserve (more in cold).
- [ ] Charging happens with the original charger in a safe spot with a smoke alarm.
- [ ] Batteries are stored part-charged when unused.
- [ ] You brake earlier and expect others to misjudge your speed.

## Checked

Jurisdiction: EU and US legal definitions. Checked 2026-10-25: 15 USC 2085 (two- or three-wheeled, operable pedals, motor under 750 W, under 20 mph on motor alone at 170 lb rider); Regulation (EU) 168/2013 exclusion of pedal-assisted cycles with auxiliary motor of at most 250 W cutting out by 25 km/h (via search summaries of EUR-Lex and GOV.UK guidance; EUR-Lex itself not fetched). Range arithmetic recomputed (500 Wh at 8 Wh/km is 62 km, at 18 Wh/km is 28 km). Battery and consumption rules of thumb are marked gated.

Method: documentation only; no commands were run.
