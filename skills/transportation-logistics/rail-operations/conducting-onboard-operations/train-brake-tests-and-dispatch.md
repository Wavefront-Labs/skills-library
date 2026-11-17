---
id: transportation-logistics.rail-operations.conducting-onboard-operations.train-brake-tests-and-dispatch
name: train-brake-tests-and-dispatch
category: transportation-logistics
field: rail-operations
product: conducting-onboard-operations
tags: [conducting-onboard-operations, conductor, guard, train-manager, brake-test, air-brake-test, class-i-brake-test, continuity-test, brake-continuity, eot, end-of-train-device, flashing-rear-end-device, consist, train-list, wheel-report, train-documents, dangerous-goods, hazmat-paperwork, train-dispatch, right-away, platform-dispatch, door-safety, passenger-safety, onboard-safety, emergency-equipment]
level: practitioner
status: draft
description: "The conductor/guard routine: prepare the train, run and record a brake continuity test, check consist and dangerous-goods paperwork, and dispatch safely from the platform."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Train brake tests and dispatch

**Goal:** the train leaves with a working continuous brake through every vehicle,
paperwork that matches what's actually on the rails, and nobody hurt at the doors.

*Draft: brake-test types and pressures (e.g. North American Class I/IA/III tests,
European continuity tests), dispatch signals and paperwork formats are set by each
railway and regulator. Treat values as illustrative and follow your rulebook.*

## 1. Train preparation
- Walk the train (freight) or check the unit (passenger): couplings made and locked,
  hoses connected and angle cocks open (except the rear), handbrakes released, no
  dragging equipment, doors/ramps closed, lading secure, tail lamp/EOT fitted.
- Passenger: emergency equipment present (detrainment ladder, fire extinguishers,
  first aid, hammer), PA and cab-to-cab working, toilets and accessibility kit OK.

## 2. Brake continuity test (the core idea)
The test proves the brake pipe is continuous from the controlling cab to the rear,
and that brakes apply and release on each vehicle.
1. Charge the brake pipe to the required pressure; check rear pressure (EOT readout or
   rear gauge) is within the allowed difference from the front.
2. Leakage/gradient check if required.
3. **Apply:** the driver makes the prescribed application; you (or a walking
   inspector) confirm brakes applied on each vehicle — pistons out/indicators on.
4. **Release:** confirm every brake releases.
5. **Rear-end check:** the rear pressure falls on application and rises on release —
   this is what proves continuity; a closed angle cock mid-train fails it.
6. Record the test (time, place, who, type) in the train documents.

Re-test after any change in consist (added/removed vehicles) or after the brake pipe
was opened, per the rules for that kind of test.

## 3. Paperwork
- **Consist/train list:** every vehicle number in order, loads/empties, weight, length,
  any restrictions (out-of-gauge, speed-restricted).
- **Dangerous goods:** positions comply with placement rules; emergency response
  info is on board and matches the cars; placards present.
- Calculate/confirm brake force or tons-per-operative-brake against route limits.
- Driver gets a copy and you both agree on length and weight — these drive train
  protection data entry and stopping distances.

## 4. Platform dispatch
1. Check the departure time and the platform starting signal or dispatch authority.
2. Watch the **whole** platform-train interface: last-minute runners, children,
   wheelchair ramps stowed, people leaning on the train.
3. Close doors (or signal for closure) with warning; check for trapped people and
   items — the interlock light alone does not prove this.
4. Give the ready-to-start/"right away" signal only when doors are closed and locked
   *and* the platform is safe.
5. Watch the train out for the first car length (where your role requires) ready to
   stop it.

## 5. Onboard safety
Patrol, deal with alarms promptly (passcomm/emergency handles), know where the train
is when calling emergency services, and know your evacuation procedure (see
transportation-logistics.rail-operations.degraded-working.failed-train-and-evacuation).

## Gotchas
- A brake test done before a car was added is not valid for the train you're taking.
- "Close enough" rear pressure is how a closed angle cock gets missed.
- Dispatch pressure from a late running service — don't let it shorten the PTI check.

## Verify
- [ ] Brake test performed, rear-end pressure change observed, and recorded.
- [ ] Consist matches the train, dangerous goods placed and documented.
- [ ] Driver and guard agree length/weight.
- [ ] Every dispatch: signal checked, doors interlocked, platform observed clear.
