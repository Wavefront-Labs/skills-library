---
id: transportation-logistics.traffic-transport-signalling.adaptive-signal-systems.timing-plans-coordination-and-detector-faults
name: timing-plans-coordination-and-detector-faults
category: transportation-logistics
field: traffic-transport-signalling
product: adaptive-signal-systems
tags: [traffic-signals, signal-timing, scats, scoot, adaptive-signal-control, fixed-time, actuated-control, cycle-length, splits, offsets, green-wave, coordination, webster-formula, degree-of-saturation, inductive-loop, detector-fault, intergreen, clearance-interval, yellow-change, all-red, pedestrian-timing, time-space-diagram, synchro, linsig]
level: practitioner
status: gated
description: "Building and checking signal timing plans (cycle, splits, offsets, clearances), coordinating corridors, and keeping SCATS/SCOOT adaptive control healthy when detectors fail."
sources: ["https://ops.fhwa.dot.gov/publications/fhwahop08024/chapter5.htm", "https://ops.fhwa.dot.gov/publications/fhwahop08024/index.htm"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Timing plans, coordination and detector faults

**Goal:** run signals that move traffic and pedestrians safely and efficiently, and keep
adaptive systems from quietly degrading to bad fixed timings when detection fails.

## 1. Safety timings first (non-negotiable)
- **Yellow change interval** (ITE kinematic formula): Y = t + v/(2a + 2gG), with
  perception-reaction t ≈ 1 s, deceleration a ≈ 3 m/s² (10 ft/s²), v the approach
  speed (85th percentile or limit). Typically 3–6 s (gated: unconfirmed, source is paywalled or blocked).
- **All-red clearance:** time to clear the intersection: (W + L)/v (W = stop line to
  far conflict point, L ≈ 6 m vehicle). Usually 1–2 s (gated: unconfirmed, source is paywalled or blocked).
- **Pedestrian clearance (flashing don't walk):** crossing distance ÷ walking speed
  (~1.1–1.2 m/s; slower near elderly/school users, per local standard).
- UK and Europe use **intergreen** matrices (conflict-specific) — calculated per
  conflicting movement pair. *Use your jurisdiction's manual (MUTCD/STM in the US,
  DMRB/TSRGD-related guidance in the UK).*

## 2. Fixed-time plan
1. Count critical flows per phase (veh/h) and saturation flows (~1,800–1,900 pcu/h/lane (gated: unconfirmed, source is paywalled or blocked)).
2. Flow ratios y = q/s; sum of critical ratios Y.
3. **Webster optimum cycle:** C₀ = (1.5L + 5)/(1 − Y), L = total lost time per cycle.
   Example: L = 12 s, Y = 0.6 → C₀ = 23/0.4 ≈ 58 s. Keep cycles typically 60–120 s (gated: unconfirmed, source is paywalled or blocked);
   long cycles hurt pedestrians and bus reliability.
4. **Splits:** distribute effective green in proportion to critical y; check minimum
   greens and pedestrian walk + clearance fit.
5. **Degree of saturation** per approach < ~0.9 (practical capacity).
6. Time-of-day plans: AM peak, PM peak, off-peak, night (shorter cycles or free/
   actuated), weekend.

## 3. Coordination (green waves)
- Common cycle length across the corridor (or half/double cycles).
- **Offset** ≈ distance / progression speed (e.g. 400 m at 50 km/h ≈ 29 s), adjusted
  for queue clearance at the downstream stop line.
- Build and check a **time-space diagram** (Synchro, LinSig, TRANSYT, PTV Vistro):
  bandwidth in both directions, not just the peak direction.
- Verify in the field with floating-car runs; count stops.

## 4. Adaptive systems (SCATS, SCOOT)
- **SCATS** adjusts cycle, splits and linking from stop-line detectors using degree
  of saturation; **SCOOT** models upstream-detector flow profiles and makes frequent
  small changes to splits, offsets and cycle.
- Both depend on **detector health**. A failed loop typically substitutes a default
  value — the system keeps running, but badly.
- Daily: check the detector fault list, sites in fallback (fixed-time or isolated),
  and approaches running at max/min green continuously.
- Tuning: set realistic min/max cycle bounds, pedestrian minimums, priority
  (bus/emergency) parameters; review after any geometry change.

## 5. Detector faults: handling
1. Identify: stuck-on (constant call → max greens), stuck-off (approach starved),
   chattering.
2. Apply a fault mode: place a **recall** (min or max recall as appropriate) or
   fallback plan so movements are still served.
3. Raise a repair ticket with location, loop ID and symptom; track to closure.
4. After repair, verify counts against a manual or video count.

## Gotchas
- Shortening yellow or all-red to "fix" capacity is a safety regression.
- Coordinating for the peak direction can starve side streets and cause red-light
  running; check side-street delay.
- Leftover temporary plans after roadworks or events — audit active plans weekly.

## Verify
- [ ] Yellow, all-red and pedestrian clearances meet the local standard.
- [ ] Cycle and splits keep degree of saturation < ~0.9 on critical approaches.
- [ ] Time-space diagram shows two-way bandwidth; field runs confirm.
- [ ] No unacknowledged detector faults; all faulted detectors have a recall/fallback set.

## Checked

Jurisdiction: US practice (FHWA Signal Timing Manual) with UK/Australian SCOOT/SCATS notes. Checked 2026-10-25: FHWA Signal Timing Manual chapter 5 gives the kinematic change-period equation with perception-reaction time 1.0 s, deceleration 10 ft/s2 and vehicle length 20 ft (consistent with the skill form); Webster optimum cycle recomputed ((1.5 x 12 + 5)/(1 - 0.6) = 57.5 s); offset 400 m at 50 km/h = 28.8 s. Typical-range figures not found in the fetched page are marked gated.

Method: documentation only; no commands were run.
