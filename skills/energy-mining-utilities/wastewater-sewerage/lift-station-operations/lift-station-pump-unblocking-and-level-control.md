---
id: energy-mining-utilities.wastewater-sewerage.lift-station-operations.lift-station-pump-unblocking-and-level-control
name: lift-station-pump-unblocking-and-level-control
category: energy-mining-utilities
field: wastewater-sewerage
product: lift-station-operations
tags: [wastewater-sewerage, lift-station-operations, lift-station, pumping-station, sewage-pump-station, submersible-pump, ragging, de-ragging, wipes, pump-unblocking, guide-rail, lifting-chain, loto, lockout-tagout, wet-well, wet-well-cleaning, float-switch, ultrasonic-level, duty-assist-standby, pump-down, high-level-alarm, overflow, odour-control, h2s, motor-current, pump-station-operator]
level: practitioner
status: draft
description: "Keep a sewage lift station running: diagnose ragged pumps from current and flow, safely lift and de-rag submersibles, set duty/assist levels and clean the wet well."
sources:
  - "Pump manufacturers' submersible wastewater pump O&M guidance, general practice paraphrased"
  - "WEF/utility pump station operations training, paraphrased"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Lift station pump unblocking and level control

**Goal:** keep sewage moving through a pumping station with no spills, and fix the most
common fault — a pump ragged up with wipes — without hurting anyone.

## 1. Recognise a ragged pump
- Motor **current higher than normal** (partial blockage, heavy load) or **lower** (impeller
  fully clogged or air-locked, pumping little), with reduced flow or longer run times.
- Pump runs, level barely falls; frequent overload/thermal trips; noise and vibration.
- Compare run time per cycle and drawdown rate with the other pump and the history.
Try once: a pump reverse-run/anti-ragging function if fitted (many controllers can run a
short reverse cycle). If it clears, note it; if not, lift the pump.

## 2. Lifting and de-ragging safely
1. **Isolate electrically:** lock out at the panel (personal lock and tag), test for dead,
   and switch the controller so the other pump takes duty. Remember the stand-by may
   start automatically — check which pump you are isolating.
2. Close the pump's discharge isolation valve if you'll disturb the discharge connection.
3. Gas test at the wet-well opening (H2S, LEL, O2); **don't enter the wet well** to do this —
   submersibles on guide rails are lifted from the surface by chain/davit or crane.
4. Lift steadily on the chain; a pump that won't release from the duckfoot may be packed
   with rag — don't overload the davit.
5. Hose down, then clear rag from the impeller and volute with hooks or cutters. **Never
   put hands into the impeller** — wear cut-resistant gloves and use tools; impellers can
   rotate under the weight of rags or stored energy.
6. Inspect impeller wear, wear ring clearance, cable and its entry, seal oil (milky oil =
   seal failure). Reinstall, reconnect, remove locks, test run and record current and
   drawdown.

## 3. Level control setup
Typical sequence from bottom up (check your design):
1. **Pumps off** level — above the pump's minimum submergence so it doesn't draw air or
   overheat (motor cooling on some submersibles needs submergence).
2. **Duty on** level — gives a cycle volume that keeps starts per hour within the motor
   limit.
3. **Assist on** — second pump for peak/storm flows.
4. **High level alarm** — with enough storage time left to respond before **overflow**.
Alternate duty pump each cycle. Vary the stop level occasionally (or use a periodic
"pump-down"/snore cycle) to drag floating fat and scum through, so a fat mat doesn't
form at the normal stop level.
Have a **backup float** independent of the ultrasonic/pressure transducer.

## 4. Wet-well cleaning and odour
Vacuum-tanker the wet well periodically to remove grit, fat and rag. Check odour control
(carbon filters, chemical dosing) works — H2S corrodes concrete and steel and causes
complaints. Check valve chambers for leaking non-return valves (pump backspins at stop).

## Gotchas
- Isolating at the controller "off" switch is not isolation; lock out at the source.
- Non-return valves stuck open let the main drain back — pump cycles endlessly.
- During storms, standby pumps and generator start-up must be tested *before* the event.

## Verify
- [ ] Locked out at source and verified dead before lifting.
- [ ] No entry into the wet well without a confined-space permit.
- [ ] Post-repair current and drawdown match the other pump/history.
- [ ] Level sequence gives submergence, starts/hour limits and alarm-to-overflow time.
- [ ] Backup float and alarm tested.

*Uncertain:* exact levels, start limits and reverse-run features depend on pump and
controller makers.
