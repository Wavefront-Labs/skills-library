---
id: energy-mining-utilities.water-treatment-supply.pumping-storage-operations.service-reservoir-level-control-and-pump-scheduling
name: service-reservoir-level-control-and-pump-scheduling
category: energy-mining-utilities
field: water-treatment-supply
product: pumping-storage-operations
tags: [water-treatment-supply, pumping-storage-operations, service-reservoir, water-tower, storage-tank, level-control, pump-scheduling, duty-standby, pump-start-stop, energy-tariff, off-peak-pumping, water-age, turnover, reservoir-mixing, reservoir-inspection, hatch-security, borehole, source-switching, booster-station, pump-cycling, telemetry, water-network-operator]
level: practitioner
status: draft
description: "Run pumps and service reservoirs together: set level bands, schedule pumping to tariffs and demand, keep turnover for water age, and inspect reservoirs hygienically."
sources:
  - "AWWA Manual M42 (Steel Water-Storage Tanks) and M68 (water quality in distribution) storage guidance, paraphrased"
  - "Utility operating practice for service reservoir management as commonly taught, paraphrased"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Service reservoir level control and pump scheduling

**Goal:** keep every customer supplied with enough pressure and a fire reserve, at the
lowest energy cost, without letting water sit long enough to lose its disinfectant.

## 1. The three jobs storage does
1. **Balancing** — pumps run steadily while demand swings through the day.
2. **Emergency/fire reserve** — a bottom slice you never plan to use.
3. **Pressure** — towers and elevated reservoirs set network head.
Write down for each site: total volume, overflow level, fire/emergency reserve level,
low-level alarm, and how many hours of average demand it holds.

## 2. Set level bands
- Pump **start** level above the reserve plus a margin for pump response time.
- Pump **stop** level below overflow with margin for inflow after stop and level sensor error.
- A band too narrow causes frequent starts (motor and contactor wear; commonly keep below
  ~4–6 starts per hour for larger motors — check the motor maker's limit).
- Use duty/standby rotation so run hours balance and the standby is proven to work.

## 3. Schedule for cost and quality
- Fill during off-peak tariff periods, draw down through peak, so the reservoir is low just
  before cheap power returns. Check you can still meet a "worst day" demand profile.
- **Turnover:** a reservoir that only cycles the top 10–20% leaves old water at the bottom.
  Aim to exchange a meaningful fraction daily (many utilities target ≥ 20–30%/day or a
  water-age limit of a few days); deepen the draw if chlorine residual at the outlet falls.
- Seasonal: in winter, demand drops but reservoir bands often stay at summer settings —
  water age climbs. Review bands each season.

## 4. Boreholes and source switching
Start boreholes to waste/run-to-waste until turbidity settles, especially after long
idle periods. Ramp pumps; sudden drawdown can pull sand. Switching between sources with
different chemistry (hardness, pH, chloramine vs chlorine) can cause discolouration and
taste complaints — blend gradually and warn customer service.

## 5. Reservoir hygiene and security
- Weekly/monthly site check: hatches locked and sealed, vents screened and intact,
  overflow flap closed, no animal or bird access, roof membrane intact, no ponding.
- Hatches open only with authorisation, clean clothing/boots, nothing loose that can drop
  in. Any entry follows confined-space rules.
- Periodic internal inspection (drone/ROV or drained), sediment removal, then
  disinfection and a satisfactory bacteriological sample before return to service.

## Gotchas
- A stuck level transducer (ragged, frozen, drifting) makes the reservoir look fine while
  it overflows or empties — compare against a second source (float switch, inlet/outlet
  flow balance) regularly.
- Overflow events often coincide with telemetry communication failure; confirm local
  fail-safe control.
- Inlet and outlet close together → short-circuiting; old water stays put regardless of
  turnover figures.

## Verify
- [ ] Start/stop levels leave the fire/emergency reserve untouched on a worst-case day.
- [ ] Starts per hour within motor limits; duty/standby rotating.
- [ ] Daily turnover and outlet chlorine residual tracked; bands adjusted seasonally.
- [ ] Hatches, vents and overflow screens checked and logged.
- [ ] Level reading cross-checked against an independent signal.

*Uncertain:* turnover and starts-per-hour targets are rules of thumb; confirm against your
utility's water-quality and motor specifications.
