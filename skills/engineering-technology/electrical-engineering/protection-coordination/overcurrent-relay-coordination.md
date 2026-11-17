---
id: engineering-technology.electrical-engineering.protection-coordination.overcurrent-relay-coordination
name: overcurrent-relay-coordination
category: engineering-technology
field: electrical-engineering
product: protection-coordination
tags: [protection, coordination, selectivity, overcurrent, ansi-50, ansi-51, ansi-50n, idmt, tcc, time-current-curve, cti, coordination-time-interval, ct-sizing, ct-saturation, c-class, 5p20, ieee-c37-112, iec-60255-151, ieee-c37-110, ieee-c57-13, iec-61869-2, transformer-damage-curve, ieee-c57-109, fuse, breaker, selective-coordination, nec-700-32, etap-star, skm-captor, grading-margin, instantaneous-pickup-setting]
level: advanced
status: gated
description: "Coordinate overcurrent relays, breakers and fuses: CT selection and saturation check, 51/50 settings, IEC/IEEE curves, 0.2-0.4 s CTI."
sources:
  - "IEEE Std 242 (Buff Book), Recommended Practice for Protection and Coordination of Industrial and Commercial Power Systems"
  - "IEEE Std C37.112, Inverse-Time Characteristics Equations for Overcurrent Relays"
  - "IEC 60255-151, Measuring relays and protection equipment - Functional requirements for over/under current protection"
  - "IEEE Std C37.110, Guide for the Application of Current Transformers Used for Protective Relaying Purposes"
  - "IEEE Std C57.109, Guide for Liquid-Immersed Transformers Through-Fault-Current Duration"
  - "Blackburn & Domin, Protective Relaying: Principles and Applications"
  - "GE/Alstom, Network Protection & Automation Guide (NPAG)"
licence: Apache-2.0
version: 4
updated: 2026-11-17
aliases: []
---

# Overcurrent relay coordination — selective, fast, and CTs that don't lie

**Goal:** every fault is cleared by the nearest upstream device, backup operates only
after a defined margin, and all equipment damage curves sit to the right of the
devices protecting them.

## 1. Inputs
One-line with max **and** min fault currents at every bus (three-phase and
earth-fault), full-load and peak load currents, transformer kVA/%Z/inrush, cable
sizes, motor starting currents and times, and the device library (relays, breaker
trip units, fuse curves).

## 2. Select and check the CTs
- Ratio: primary ≥ max continuous load, and fault current ≤ ~20× rated (the accuracy
  limit) — e.g. 20 kA fault on a 600/5 CT is 33× and needs checking.
- Accuracy: IEEE C57.13 **C100/C200/C400/C800** (secondary volts at 20× rated with
  ≤10% error); IEC 61869-2 **5P20/10P20** with a VA burden.
- Saturation check (IEEE C37.110 style): required knee/terminal volts
  `Vs ≥ I_f,sec × (R_ct + R_leads + R_relay) × (1 + X/R)`.
  Meeting the (1+X/R) factor avoids DC-offset saturation entirely; numerical relays
  tolerate partial saturation for overcurrent, much less so for differential.
- Use 1 A secondaries where leads are long (burden falls by 25×).

## 3. Set the time-overcurrent (51) element
- Pickup: phase 1.25–1.5 × maximum load (feeders); transformer primary above
  emergency overload. Must be below minimum end-of-zone fault with margin (≥ 1.5–2×).
- Ground (51N/51G) pickup well below phase — often 10–20% of CT rating on solidly
  grounded systems; on resistance-grounded systems below the resistor let-through.
- Curve (time multiplier M = I / I_pickup):
  - IEC 60255-151 Standard Inverse: `t = TMS · 0.14 / (M^0.02 − 1)`
  - IEEE C37.112 Very Inverse: `t = TD · (19.61 / (M² − 1) + 0.491)` (gated: unconfirmed, source is paywalled or blocked)
  - IEEE Extremely Inverse: `t = TD · (28.2 / (M² − 1) + 0.1217)` (gated: unconfirmed, source is paywalled or blocked). Secondary sources agree on these constants, but the 1996 edition reportedly left coefficients to manufacturers, so use the coefficients in the relay manual.
  Some relays scale TD differently (e.g. older TD 0.5–15 vs 0.5–10 or a /7 factor)
  — check the manual before transferring settings between makes.
- Use extremely inverse downstream of fuses and for feeders with cold-load pickup;
  very inverse where fault current falls off strongly with distance.

## 4. Coordination time interval (CTI)
At the **maximum** fault current seen by both devices, separation between curves (typical practice figures (gated: unconfirmed, source is paywalled or blocked); confirm against IEEE 242 and the relay maker):
- Electromechanical relay–relay: 0.3–0.4 s (breaker ~0.08 s + overtravel ~0.1 s + margin).
- Numerical relay–relay: 0.2–0.25 s.
- Relay over fuse: ~0.2 s plus fuse tolerance; fuse–fuse by manufacturer selectivity
  ratio (often ≥ 2:1 on current-limiting fuses — confirm per fuse family).
- LV breakers: use manufacturer selectivity tables; curves overlapping in the
  instantaneous region may still be selective per tested tables.
Then check the **minimum** fault too: coordination can be lost when currents are low.

## 5. Instantaneous (50)
Set above the maximum through-fault at the next downstream bus (×1.2–1.3) so it
cannot overreach; for transformer primaries also above inrush (≈ 8–12 × FLA for
~0.1 s) (gated: unconfirmed, source is paywalled or blocked). A 50 that can't be set selectively is better disabled than miscoordinated —
unless arc-flash results demand speed, then use ZSI or bus differential instead.

## 6. Damage curves and code
Plot transformer through-fault curves (IEEE C57.109, including the shifted curve for
delta-wye ground faults), cable I²t damage curves and motor thermal limits; devices
must be left/below them. NEC 450.3 limits transformer primary/secondary protection
ratings; NEC 700.32/701.32 (and 517 for healthcare) require *selective* coordination
for emergency and legally required standby systems (section numbers vary by NEC edition; confirm in the adopted edition). Protection settings are safety-critical: have a qualified protection engineer approve them.

```python
def iec_si(I, Is, tms): M = I/Is; return tms*0.14/(M**0.02-1)
up, dn = iec_si(8000, 600, 0.30), iec_si(8000, 300, 0.10)
print(f"CTI = {up-dn:.2f} s")   # target >= 0.2-0.3 s
```

## Verify
- [ ] CTI ≥ 0.2–0.4 s (per technology) at maximum fault for every series pair, and still selective at minimum fault.
- [ ] Every CT passes the saturation voltage check for its relay function.
- [ ] Pickups clear maximum load and motor/transformer inrush without tripping.
- [ ] All devices sit inside cable, transformer and motor damage curves.
- [ ] Settings transferred to relays match the study (check TD scaling per make).
- [ ] Selective coordination demonstrated where NEC 700/701/517 applies.
