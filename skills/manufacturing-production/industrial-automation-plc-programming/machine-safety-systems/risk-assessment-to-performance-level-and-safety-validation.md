---
id: manufacturing-production.industrial-automation-plc-programming.machine-safety-systems.risk-assessment-to-performance-level-and-safety-validation
name: risk-assessment-to-performance-level-and-safety-validation
category: manufacturing-production
field: industrial-automation-plc-programming
product: machine-safety-systems
tags: [machine-safety-systems, machine-safety, functional-safety, iso-12100, iso-13849, iso-13849-1, iso-13849-2, iec-62061, plr, performance-level, pl-d, pl-e, sil, category-3, category-4, mttfd, dcavg, ccf, sistema, safety-plc, safety-relay, guard-interlock, iso-14119, light-curtain, iso-13855, safety-distance, e-stop, iso-13850, stop-category, safe-torque-off, sto, muting, validation, industrial-automation-plc-programming]
level: advanced
status: draft
description: "Engineer machine safety functions from risk to proof: ISO 12100 assessment, PLr from the ISO 13849 risk graph, category/MTTFd/DC design, safety distances, and validation testing."
sources: ["ISO 12100", "ISO 13849-1 and -2", "IEC 62061", "ISO 13855", "ISO 14119", "ISO 13850"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# From risk assessment to performance level and safety validation

**Goal:** each hazard on a machine gets a defined safety function, designed to the
required performance level, and proven by test — leaving a file an inspector (and
your own conscience) can follow.

*Draft: summarises the standard method; it is not a substitute for the standards
themselves or for a competent functional-safety engineer. Requirements differ by
jurisdiction (EU Machinery Regulation, OSHA/ANSI B11, etc.).*

## 1. Risk assessment (ISO 12100)
1. Define limits: intended use, foreseeable misuse, all life phases (setting, cleaning,
   maintenance, jam clearing — where most injuries happen).
2. Identify hazards per task: crushing, shearing, entanglement, stored energy
   (pneumatic, hydraulic, gravity), electrical, thermal.
3. Estimate risk; reduce by the **three-step method**: inherently safe design → guarding
   and safety functions → information/training. A warning sign is the last resort, not
   the fix.

## 2. Required performance level (ISO 13849-1 risk graph)
For each safety function, decide:
- **S** severity: S1 slight (reversible), S2 serious (irreversible, death).
- **F** frequency/exposure: F1 seldom/short, F2 frequent/long.
- **P** possibility of avoidance: P1 possible, P2 scarcely possible.
The graph gives **PLr** a–e. S2/F2/P2 → PLe; typical guard door on a frequently
accessed machine lands at PLd. (IEC 62061 gives SIL instead; SIL 2 ≈ PLd, SIL 3 ≈ PLe
in rough equivalence.)

## 3. Designing to the PL
The achieved **PL** depends on:
- **Category** (B, 1, 2, 3, 4): architecture. Cat 3 = single fault doesn't lose the
  function (dual channel); Cat 4 = also detects accumulated faults.
- **MTTFd** of each channel (from B10d values for electromechanical parts and operations
  per year: `MTTFd = B10d / (0.1 × nop)`).
- **DCavg** (diagnostic coverage): how much of the dangerous failures are detected
  (cross-monitoring, feedback contacts on contactors — "EDM").
- **CCF** score ≥ 65 points for Cat 2–4 (separation, diversity, EMC, environment).
Use **SISTEMA** (free IFA tool) or the vendor's equivalent to calculate PL per function.
Each function: input (interlock/light curtain) → logic (safety relay/safety PLC) →
output (contactors, valve, drive **STO**); the weakest subsystem sets the PL.

## 4. Practical device rules
- **Guard interlocks (ISO 14119):** choose coded devices so they can't be defeated with
  a screwdriver/magnet; fit them where defeating is hard; guard locking if run-down time
  exceeds access time.
- **Light curtains (ISO 13855):** safety distance `S = K × T + C` — K approach speed
  (2000 mm/s, or 1600 mm/s beyond 500 mm), T total stopping time (sensor + logic +
  machine **measured** stop time), C intrusion allowance from resolution. Measure the
  real stopping time with a stop-time meter; it grows as brakes wear.
- **E-stop (ISO 13850):** a complementary measure, not a safeguard; usually stop
  category 0 or 1. Reset must not restart the machine.
- **Stop categories (IEC 60204-1):** 0 remove power; 1 controlled stop then remove power;
  2 controlled stop, power kept (needs standstill monitoring).
- Safety PLC code: separate, version-controlled, password-protected, with a checksum/
  signature recorded at validation.

## 5. Validation (ISO 13849-2)
- Validation plan written *before* testing: every safety function, how it's tested,
  expected result.
- Test each function, including **fault injection** (remove one channel, weld a contact
  in simulation, short a cable) to prove Cat 3/4 behaviour.
- Record safety program checksum, device settings, measured stop times, and sign.
- Re-validate after any change to safety hardware, software or stopping performance.

## Gotchas
- Muting and bypass modes (for material through a light curtain) are where accidents
  live — muting sensors must make it impossible for a person to trigger them.
- Standard PLC logic must never be the only thing stopping a hazard.
- Pneumatics keep pressure after the valve drops — dump valves and gravity holding.

## Verify
- [ ] Every hazard has a safety function with PLr and achieved PL ≥ PLr.
- [ ] Measured stopping times used in all safety distances.
- [ ] Fault-injection tests done and recorded for Cat 3/4 functions.
- [ ] Safety program checksum in the validation record matches the controller.
- [ ] Change control triggers re-validation.

Related: `engineering-technology.industrial-manufacturing-systems-engineering.factory-automation-design.robot-cell-concept-and-safety-design`.
