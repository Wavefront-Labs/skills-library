---
id: repair-maintenance.motorcycle-small-engine-repair.small-engine-overhaul.compression-valve-and-governor-diagnosis
name: compression-valve-and-governor-diagnosis
category: repair-maintenance
field: motorcycle-small-engine-repair
product: small-engine-overhaul
tags: [small-engine-overhaul, small-engine, four-stroke, briggs-and-stratton, honda-gx, kohler, tecumseh, ohv, flathead, compression-test, compression-release, leak-down, valve-clearance, valve-lash, valve-lapping, lapping-compound, governor, governor-adjustment, surging, hunting, recoil-starter, pull-cord, flywheel-key, sheared-key, spark-tester]
level: practitioner
status: draft
description: "Diagnose and overhaul four-stroke small engines: spark/fuel/compression triage, compression and leak-down, valve clearance and lapping, static governor setting, flywheel key and recoil starter."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Compression, valves and governor — small four-stroke engines

**Goal:** a mower, tiller or pump engine (Briggs & Stratton, Honda GX/GC, Kohler, Loncin
etc.) that starts in a pull or two and holds governed speed under load.

## 1. Triage: spark, fuel, compression, timing
1. **Spark**: inline spark tester or plug grounded on the head; strong blue spark while
   pulling. No spark → kill switch/wire (often shorted to ground), coil air gap, coil.
2. **Fuel**: fresh fuel? A squirt of fuel into the plug hole — fires briefly then dies =
   carb/fuel delivery problem (see carburettor-fuel-systems).
3. **Compression**: see below.
4. **Timing**: a hard kickback, or spark/fuel/compression all OK but won't run → check for a
   **sheared flywheel key** (often from hitting a stump with a mower blade). Remove the
   flywheel (flywheel puller, not a hammer) and inspect the soft aluminium key.

## 2. Compression test
- Most small engines have an **automatic compression release** (ACR) that holds an
  exhaust valve slightly open at cranking speed — gauge readings by pull-start are low
  (often ~40–90 psi) and the manual's spec matters. Some testers recommend reverse-
  rotating the engine to bypass the ACR; follow the engine maker's method.
- Better: **leak-down test** at top dead centre on compression stroke (both valves
  closed), ~80–100 psi in. Listen: hiss at **exhaust** = exhaust valve; at **carb/intake** =
  intake valve; in the **crankcase breather/oil fill** = rings; a leak between
  head and block = head gasket.
- No compression on an OHV engine often = **valve clearance gone to zero** or a bent push
  rod; flatheads: burnt valve or carbon on the seat.

## 3. Valve clearance (OHV)
1. Engine cold, plug out, piston at **TDC compression** (both rockers loose; watch the
   intake valve close, then bring the piston up).
2. Some makers specify measuring **~6 mm past TDC** to clear the ACR — check the manual.
3. Feeler gauge between rocker and valve stem. Typical: **intake ~0.10–0.15 mm,
   exhaust ~0.15–0.20 mm** (Honda GX ~0.15/0.20 mm; Briggs varies by model).
4. Loosen locknut, adjust pivot nut until the gauge drags slightly, hold and tighten
   locknut, re-measure. New rocker-cover gasket.

## 4. Valve lapping (when seats leak)
1. Remove head (or valve chamber on flatheads); compress springs and remove keepers.
2. Inspect valves: burnt, cupped or thin margins → replace. Seats pitted heavily → recut.
3. Lightly coat the valve face with **fine lapping compound**, use a suction-cup lapping
   stick, rotate back and forth, lift and turn periodically. Stop when a **continuous,
   even grey band** shows on both face and seat.
4. **Clean every trace of compound** (it's abrasive) — solvent, then oil.
5. Reassemble with new valve stem seal (OHV), new head gasket; torque head bolts in
   sequence and stages. Set clearance.

## 5. Governor — surging/hunting or wrong speed
Mechanical governors (flyweights inside the crankcase) or air vanes link to the throttle.
**Surging** is usually a **lean carb** (partly blocked main jet/emulsion tube or an air
leak) — clean the carb first.
Static governor setting (when linkage was disturbed):
1. Engine off. Loosen the governor arm clamp nut.
2. Move the throttle to **wide open** and hold.
3. Rotate the **governor shaft** in the direction the manual specifies (usually the
   direction that also opens the throttle) to its stop. Tighten the clamp.
4. Set top no-load rpm with a tachometer to spec (mowers often ~2,800–3,600 rpm; blade
   tip speed limits apply). **Never bend springs or linkages to raise rpm** — over-speed
   breaks blades and flywheels.

## 6. Recoil starter
Rope won't retract: broken or unhooked spring, or dirt in the pawl area. Rewind with the
pulley tensioned the specified number of turns plus one, rope fully retracted with tension
on it. Wear gloves and eye protection — recoil springs release violently.

## Gotchas
- Oil level too high or a tipped engine → smoke and hydraulic lock; tip mowers carb side up.
- Wrong oil (multigrade spec matters in cold climates) and low oil shutdowns.
- Overtightened plugs strip aluminium heads; torque by hand + ½ turn on a new gasket plug.

## Verify
- [ ] Spark, fuel, compression and flywheel key all confirmed.
- [ ] Leak-down identifies the leak path; valves lapped to a continuous band.
- [ ] Valve clearance set to spec at TDC compression.
- [ ] Governor set statically; top no-load rpm measured with a tach and in spec.
- [ ] No surging under load.
