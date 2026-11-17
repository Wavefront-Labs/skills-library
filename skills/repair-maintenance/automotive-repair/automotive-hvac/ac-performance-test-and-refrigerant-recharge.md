---
id: repair-maintenance.automotive-repair.automotive-hvac.ac-performance-test-and-refrigerant-recharge
name: ac-performance-test-and-refrigerant-recharge
category: repair-maintenance
field: automotive-repair
product: automotive-hvac
tags: [automotive-repair, automotive-hvac, car-air-conditioning, a-c, r134a, r1234yf, epa-609, f-gas, ac-machine, recovery-recharge, manifold-gauges, vent-temperature, compressor-clutch, pressure-switch, leak-detection, uv-dye, nitrogen-test, expansion-valve, orifice-tube, blend-door, actuator-calibration, cabin-filter, pag-oil, poe-oil]
level: practitioner
status: draft
description: "Diagnose weak car A/C: vent-temperature performance test, gauge readings, leak finding (UV dye, nitrogen), recover/vacuum/recharge by weight with R134a or R1234yf, and blend-door checks."
sources: ["US EPA Section 609 MVAC technician certification requirements", "SAE J2843/J2788 (R1234yf/R134a recovery-recharge equipment)", "EU MAC Directive 2006/40/EC and F-gas regulation (context)"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# A/C performance test and refrigerant recharge

**Goal:** find why the A/C blows warm or weak, fix the cause, and restore the exact
refrigerant charge. **Legal:** US technicians servicing vehicle A/C for pay need EPA
Section 609 certification and approved recovery equipment; in the EU/UK, F-gas/MAC
qualification. Venting refrigerant is illegal. R1234yf is mildly flammable and needs
dedicated equipment.

## 1. Identify the system
Under-bonnet label: refrigerant type (**R134a** or **R1234yf** — different service-port
fittings), **charge mass** (e.g. 480 g ± 20 g) and oil type (PAG 46/100, POE for
electric compressors on hybrids/EVs — **never** put PAG into an electric-compressor system
without the maker's approval; it can breach high-voltage insulation).

## 2. Is it really refrigerant?
- Cabin air filter clogged → weak airflow. Blower speeds all working?
- Temperature selection works? **Blend door** stuck/actuator failed → cold on one side or
  never cold; run the HVAC actuator calibration with a scan tool or the panel's self-test.
- Condenser blocked by debris; **cooling fans** must run when A/C is on.
- Compressor clutch engaging (or electronic variable compressor commanded)? Fuse, relay,
  pressure switch/transducer reading, A/C request in scan data.

## 3. Performance test
- Engine ~ 1,500–2,000 rpm, A/C max, recirculation, doors/windows closed, blower high,
  5–10 min to stabilise.
- **Centre vent temperature:** typically ~ 3–8 °C (38–46 °F) at moderate ambient
  (~ 25 °C) and humidity; compare against the manufacturer's performance chart (depends
  on ambient and humidity).
- Gauges (on the A/C machine or manifold set): rough guide at ~ 25–30 °C ambient,
  low side ~ 25–45 psi (1.7–3 bar), high side ~ 2–2.5× ambient °F in psi (rule of thumb).
  - Both low → undercharged (leak).
  - Both high → overcharged, or poor condenser airflow.
  - Low side high, high side low → compressor not pumping (or variable control valve).
  - Low side very low/vacuum, high side normal-low → restriction (expansion valve, orifice
    tube, blocked drier) — look for frost at the restriction.

## 4. Find the leak (an empty system has a leak — find it before recharging)
- **UV dye** (often already present: check with a UV lamp and yellow glasses) at
  fittings, compressor shaft seal, condenser (stone damage), evaporator drain.
- **Electronic leak detector** suited to the refrigerant.
- **Nitrogen pressure test** on an empty system (often ~ 10–12 bar / 150–180 psi max for
  the low side — check equipment/vehicle guidance) with soap solution, or forming gas (95 % N2,
  5 % H2) with a hydrogen detector for tiny leaks.
- Evaporator leaks: sniff at the vent or drain with the detector.

## 5. Recover, vacuum, recharge (A/C service machine)
1. Connect the machine's high- and low-side couplers (correct type for the refrigerant).
   Identify refrigerant purity with an **identifier** if contamination is suspected
   (mandatory with R1234yf in many shops) — contaminated refrigerant goes to a separate cylinder.
2. **Recover**; the machine reports the recovered amount and oil removed.
3. Repair the leak; replace O-rings with the correct HNBR type, lubricated with the
   system's oil. Replace the receiver-drier/accumulator if the system was open for long or
   the drier desiccant is saturated.
4. **Vacuum** for ≥ 20–30 min (longer if open a while), then a **vacuum hold** (leak-check)
   ~ 5–10 min with no rise.
5. Inject replacement oil equal to the amount removed (plus component allowances), and dye
   if desired.
6. **Charge by weight** to the label amount. No "top-ups by gauge" — wrong charge damages
   compressors and reduces performance.
7. Re-run the performance test; check for leaks again.

## Gotchas
- Using a DIY can with "stop leak" contaminates machines and blocks valves; ask before connecting.
- Liquid slugging the compressor: charge through the high side with engine off, or vapour on low side as machine directs.
- Uncertain: pressure and temperature figures are rules of thumb; use the vehicle's charts.

## Verify
- [ ] Refrigerant type, charge mass and oil type confirmed from the label.
- [ ] Airflow, blend doors, fans and compressor command checked before refrigerant work.
- [ ] Leak located and repaired; vacuum hold passed.
- [ ] Oil replaced as removed; charge weighed to spec by certified tech.
- [ ] Vent temperature within chart at the measured ambient.
