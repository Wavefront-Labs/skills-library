---
id: engineering-technology.electrical-engineering.electrical-installation-design.cable-sizing
name: cable-sizing
category: engineering-technology
field: electrical-engineering
product: electrical-installation-design
tags: [cable-sizing, conductor-sizing, ampacity, current-carrying-capacity, derating, grouping-factor, ambient-correction, voltage-drop, nec, nfpa-70, nec-310-16, nec-110-14, continuous-load, bs-7671, iec-60364, iec-60364-5-52, adiabatic-equation, earth-fault-loop-impedance, zs, disconnection-time, mv-a-m, xlpe, pvc, lv-installation, amtech, etap, conductor-derating, fault-withstand-check]
level: practitioner
status: verified
description: "Size LV cables to NEC and BS 7671/IEC 60364: design current, derating, terminal ratings, voltage drop, adiabatic fault check and loop impedance."
sources:
  - "NFPA 70, National Electrical Code (2023 edition), Articles 110, 210, 215, 240, 250, 310"
  - "BS 7671:2018+A2:2022, Requirements for Electrical Installations (IET Wiring Regulations)"
  - "IEC 60364-5-52, Low-voltage electrical installations - Selection and erection - Wiring systems"
  - "IET Guidance Note 1: Selection & Erection"
  - "IET On-Site Guide"
  - "https://electrical.theiet.org/bs-7671/"
  - "https://www.nfpa.org/codes-and-standards/nfpa-70-standard-development/70"
licence: Apache-2.0
version: 5
updated: 2026-11-17
aliases: []
---

# Cable sizing — ampacity, voltage drop and fault withstand, NEC and BS 7671

**Evidence note:** NFPA 70, BS 7671, IEC 60364 and the IET guidance are paywalled, and the NFPA page fetched showed no edition list. The IET BS 7671 page names the 18th Edition (BS 7671:2018) with Amendment 4:2026 as the latest amendment, so a later amendment than the +A2:2022 cited below may now apply. Every clause number, table value and limit below is unconfirmed against the text (gated: unconfirmed, source is paywalled or blocked); the worked example arithmetic was recomputed. Installation work must follow the adopted code and be designed and checked by a qualified electrician or engineer.

**Goal:** choose the smallest conductor that carries the load after derating, keeps
voltage drop acceptable, survives the fault until the protective device clears, and
(IEC/BS) disconnects earth faults in time. All four checks; the largest result wins.

## 1. Design current
- **NEC:** continuous loads (≥ 3 h) at **125%** plus 100% of non-continuous
  (210.19(A), 215.2, 230.42). Motors: 125% of NEC table FLC (430.22), not nameplate.
- **BS 7671:** design current Ib from the load, with diversity where justified; then
  choose device In with **Ib ≤ In ≤ Iz**.

## 2. Ampacity with corrections
**NEC (Table 310.16):**
1. Start from the 90 °C column only for derating if the insulation is 90 °C (THHN/XHHW-2).
2. Apply ambient correction 310.15(B) and bundling adjustment 310.15(C)(1)
   (4–6 current-carrying conductors 80%, 7–9 70%).
3. Final ampacity must not exceed the **terminal** temperature column (110.14(C)):
   60 °C for ≤100 A / 14–1 AWG unless equipment is marked 75 °C; 75 °C above 100 A.
4. Small-conductor limits 240.4(D): Cu 14 AWG 15 A, 12 AWG 20 A, 10 AWG 30 A.
Example: 40 A continuous → 40 × 1.25 = 50 A (computed); Cu 8 AWG at 75 °C = 50 A (Table 310.16, gated: unconfirmed, source is paywalled or blocked) → OK if terminals are 75 °C.

**BS 7671 / IEC 60364-5-52:** required tabulated rating
`It ≥ In / (Ca · Cg · Ci · Cc)` — Ca ambient, Cg grouping (Table 4C1), Ci thermal
insulation, Cc = 0.725 where overload protection is a BS 3036 semi-enclosed fuse
(confirm any other factor in BS 7671 Appendix 4). Read It from the Appendix 4 table for the cable type **and installation
reference method** (A–G); method matters as much as size.

## 3. Voltage drop
`ΔV = k · I · L · (R cos φ + X sin φ)`, k = 2 single-phase, √3 three-phase; R at
operating temperature. BS 7671 tables give mV/A/m directly: ΔV = mV/A/m × Ib × L / 1000.
- **NEC:** informational notes recommend ≤ 3% branch and ≤ 5% feeder + branch — advisory,
  not enforceable, except where a specific article or local amendment says otherwise.
- **BS 7671 Appendix 4:** public LV supply 3% lighting, 5% other uses; private
  supply 6% / 8%. Check motor starting drop separately (often 10–15% at the motor terminals).
- NEC 250.122(B): if you upsize phase conductors for voltage drop, upsize the
  equipment grounding conductor proportionally — easily missed.

## 4. Fault withstand (adiabatic)
`S ≥ √(I² t) / k` (mm²). k ≈ 115 for 70 °C PVC copper, 143 for 90 °C thermosetting
(XLPE) copper (BS 7671 Table 43.1 / IEC 60364-4-43). Use the device's let-through
I²t for current-limiting devices, and the clearing time at minimum and maximum fault.
Check protective conductors the same way (BS 7671 543.1.3).

## 5. Earth-fault disconnection (TN systems, BS 7671/IEC)
Max disconnection (230 V TN): **0.4 s** for final circuits ≤ 63 A with sockets and
≤ 32 A fixed equipment; **5 s** for distribution circuits. Check
`Zs = Ze + (R1 + R2) ≤ Zs(max)` from the BS 7671 tables (Cmin = 0.95 built in).
When comparing a *measured* Zs at ambient temperature, use ~80% of the table value
(rule of thumb from IET guidance) to allow for conductor heating. RCDs cover where Zs fails.

## 6. Gotchas
- Mixing jurisdictions: NEC AWG ampacities and BS/IEC mm² ratings come from different
  thermal assumptions — never cross-use tables.
- Neutral counts as current-carrying with significant triplen harmonics (NEC 310.15(E);
  BS 7671 Appendix 4 harmonic factors).
- Section numbers above are from NEC 2023 and BS 7671:2018+A2; later editions/amendments
  renumber some clauses — check your adopted edition.

## Verify
- [ ] Design current includes NEC 125% continuous factor (or BS diversity justified).
- [ ] Derated ampacity ≥ device rating, and within terminal temperature limits (NEC).
- [ ] Voltage drop within the stated code/spec limit, including motor starting.
- [ ] Adiabatic check passes for line and protective conductors.
- [ ] (BS/IEC) Zs ≤ Zs(max) for the required disconnection time, or RCD provided.
