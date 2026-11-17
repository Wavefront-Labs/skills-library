---
id: engineering-technology.marine-naval-engineering.marine-systems.ballast-system-sizing
name: ballast-system-sizing
category: engineering-technology
field: marine-naval-engineering
product: marine-systems
tags: [marine-systems, ballast-system, ballast-pump, piping-design, pipe-sizing, darcy-weisbach, head-loss, npsh, centrifugal-pump, air-pipe, vent-pipe, overflow, bwm-convention, bwms, ballast-water-treatment, d-2-standard, uv-treatment, electrochlorination, solas, class-rules, dnv, abs]
level: practitioner
status: gated
description: "Size a ship ballast system: deballast rate, pump count and head, pipe diameters by velocity, Darcy losses, NPSH, air-pipe area and BWMS rated capacity."
sources:
  - "IMO International Convention for the Control and Management of Ships' Ballast Water and Sediments (BWM Convention), regulation D-2"
  - "IMO BWMS Code (resolution MEPC.300(72))"
  - "Class rules for piping systems (e.g. DNV Rules for Ships Pt.4 Ch.6; ABS Marine Vessel Rules Pt.4 Ch.6)"
  - "Harrington (ed.), Marine Engineering (SNAME)"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Ballast system sizing

**Goal:** size pumps, mains and branches so the ship can ballast and deballast within
the time its cargo operation demands, with adequate suction, safe tank venting and a
treatment system rated for the flow.

## 1. Set the duty
1. Total ballast volume V (m3) from the ballast arrival condition in the stability
   booklet; note the largest single tank.
2. **Required time** t: set by cargo operations, not by rule. Match the deballast
   time to the loading rate (owner's specification governs; no typical duration is claimed here).
3. Total flow Q = V / t. Split over two pumps (redundancy; many class rules let a
   ballast pump stand by for bilge or fire service, check the notation).

## 2. Size the pipes by velocity
d = sqrt(4 Q / (pi v)). Typical design velocities: suction 1.5-2.5 m/s, discharge
2.5-3.5 m/s, a main around 2-3 m/s (gated: unconfirmed, source is paywalled or blocked; confirm against the class rule and pipe maker). Higher velocity raises losses and erosion
(especially in copper-nickel; GRP and steel have their own limits from the maker).

## 3. Head and pump power
1. Static head: from the lowest tank suction to the highest discharge point (overboard
   above the waterline at ballast draft, or the top of the highest tank when filling).
2. Friction: Darcy-Weisbach hf = f (L/d) v^2 / (2g), with f from Colebrook or Moody
   using the pipe roughness (allow for ageing). Fittings: sum K v^2 / (2g)
   (bends, valves, strainers, the BWMS itself, overboard valve).
3. Add the BWMS pressure drop (take the maker's figure; no typical value is claimed here).
4. Pump power P = rho g Q H / eta_pump; motor about 10-15 % above.

## 4. Suction side (NPSH)
NPSHa = (p_atm - pv)/(rho g) + h_static_suction - hf_suction. At the end of
stripping the tank level is at the bellmouth and NPSHa is minimum: require
NPSHa > NPSHr + margin (margin per the pump maker; gated: unconfirmed). Provide a stripping
eductor or vacuum priming; plain centrifugal pumps lose suction when tanks run low.

## 5. Tank venting and overflow
Air pipes must pass air (and overflow) at the filling rate. A common class rule:
the aggregate area of air pipes on a tank is at least 125 % of the effective area of
the filling line, unless an overflow is fitted (gated: unconfirmed, class rule not fetched; check your class rule). Also check
the tank's design pressure against the overflow height and the pump shut-off head.
Load Line rules set air-pipe coaming heights: 760 mm on the freeboard deck and 450 mm on exposed decks lower than two standard superstructure heights in the 1966 Convention wording, but some flag-state rules differ (Canada's Load Line Regulations give 760/600/300 mm), so confirm the flag's current text (gated: unconfirmed, ILLC text itself not fetched).

## 6. Treatment system
Since the BWM Convention D-2 performance standard applies (numeric limits not restated here; read regulation D-2), a type-approved BWMS (under the BWMS
Code) sits in the line. Its **treatment rated capacity** must be at least the ballast
flow through it; size it for both pumps running if that is how the ship operates.
Plan the UV or electrochlorination unit's bypass and sampling points per approval.

## Worked mini-example
(Arithmetic recomputed: d 0.343 m and 0.243 m, P about 55.9 kW.)
V = 12 000 m3, t = 12 h: Q = 1000 m3/h total, two pumps x 500 m3/h.
- Main at 3 m/s: Q = 0.278 m3/s, d = sqrt(4 x 0.278 / (pi x 3)) = 0.343 m: DN350.
- Each pump branch: 0.139 m3/s at 3 m/s, d = 0.243 m: DN250.
- Assume H = 30 m (static plus friction plus BWMS), eta = 0.75:
  P = 1025 x 9.81 x 0.139 x 30 / 0.75 = about 56 kW per pump; fit about a 65 kW motor.
- BWMS treatment rated capacity of at least 1000 m3/h if both pumps run together.

## Gotchas
- Gravity ballasting/deballasting through sea chests can be quicker for upper wing
  tanks, but needs stability checks of each intermediate stage.
- Free-surface during ballast exchange or partial filling can drop GM sharply.
- Fore-peak suction pipes through the collision bulkhead need a screw-down valve
  operable from above the bulkhead deck (SOLAS II-1).
- Ballast lines through cargo tanks (tankers) are restricted; follow the class rule.

## Verify
- [ ] Deballast time with one pump failed is acceptable to the owner.
- [ ] Velocities within design limits; pipe sizes standard DN.
- [ ] Pump head includes BWMS and fittings losses; power checked.
- [ ] NPSHa > NPSHr at low tank level, with stripping arrangement.
- [ ] Air-pipe area and coaming heights checked; tank not over-pressurised.
- [ ] BWMS treatment rated capacity >= design flow through it.
