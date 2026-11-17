---
id: transportation-logistics.rail-operations.mainline-locomotives.locomotive-traction-and-dynamic-braking
name: locomotive-traction-and-dynamic-braking
category: transportation-logistics
field: rail-operations
product: mainline-locomotives
tags: [mainline-locomotives, locomotive, locomotive-engineer, train-driver, freight-train, throttle, notch, notching, traction-control, wheel-slip, sanding, dynamic-brake, dynamic-braking, rheostatic-brake, regenerative-braking, independent-brake, automatic-air-brake, bail-off, amperage, traction-motor, cab-signalling, pre-departure-checks, es44, ac4400, class-66, route-running]
level: advanced
status: draft
description: "Start, run and stop a heavy mainline train: progressive notching, wheel-slip management, dynamic brake setup and blending with air, and the in-cab checks before departure."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Locomotive traction and dynamic braking

**Goal:** get a heavy train moving without slipping or breaking it apart, run it to
the speed profile, and use dynamic brake as the primary retarding force so the air
brake is kept in reserve.

*Draft: this is a generic diesel-electric (and electric) method. Notch counts, amp
limits, wait times between throttle and dynamic and brake-pipe values are locomotive-
and railroad-specific — always use your operating rules, air-brake rules and the
locomotive's operating manual. Nothing here replaces qualification.*

## 1. Before departure (cab)
- Confirm the train consist/paperwork matches the train: tonnage, length, number of
  loads/empties, dangerous goods positions, **tons per operative brake**.
- Brake test completed and recorded by the crew responsible (see
  transportation-logistics.rail-operations.conducting-onboard-operations.train-brake-tests-and-dispatch).
- Cab checks: reverser and controls, horn, headlight, radio, vigilance/alerter, train
  protection (AWS/TPWS, PTC, ETCS — whatever applies) initialised with correct train
  data, sanders working, event recorder on.
- Know the route's first restrictions and gradients before you move.

## 2. Starting a train
1. Release the automatic brake fully; keep the independent brake applied on the
   locomotive while you take up slack, then release it.
2. **Notch progressively** — one notch, wait for amperage/tractive effort to settle,
   then the next. On a stretched train, slack runs in/out over many seconds; jumping
   notches snaps couplers.
3. On a bunched train, gently take slack out from the head end first (low notch until
   the train is moving) before adding power.
4. **Wheel slip:** if the slip indicator lights or amps fluctuate, reduce one notch,
   apply sand ahead of the wheels (not after they're already spinning hard), then
   re-apply. Modern AC units manage creep automatically; older DC units need you.

## 3. Running
- Watch amperage against the locomotive's short-time ratings on DC units; on long
  heavy grades, continuous ratings matter.
- Throttle reductions are progressive too — closing to idle at once causes run-in.
- Anticipate: begin reducing power before the crest of a hill so the train isn't
  pushing slack into the head end on the descent.

## 4. Dynamic brake
1. Transition from power to dynamic: throttle to idle, **wait** the prescribed time
   (commonly several seconds) for slack to adjust, select dynamic, set a low setting
   and let slack bunch gently, then increase.
2. Dynamic brake retards only the locomotives — it bunches the train. Keep it smooth
   and keep track of the in-train force guidance in your rules (e.g. limits on the
   number of dynamic-braking axles at the head end).
3. **Blending with air:** if dynamic alone can't hold speed, make a minimum automatic
   application in addition; many locomotives keep the independent brake bailed off so
   locomotive wheels don't lock or overheat.
4. Dynamic brake capacity falls away at low speed on many units — plan to finish the
   stop on air.

## 5. Stopping
Plan the stop point with margin; a minimum reduction early beats a heavy reduction
late. Know your release rules: some railroads restrict releasing the automatic brake
below certain speeds on heavy trains because the train may not recharge in time.

## Gotchas
- An air-only descent on a long grade depletes brake-pipe/reservoir capacity — that is
  how runaways start. Dynamic first.
- A dynamic brake fault mid-descent: stop safely on air early, don't hope to make it.
- Train data entered wrongly into train protection gives wrong braking curves.

## Verify
- [ ] Consist, tonnage and brake test confirmed before moving.
- [ ] Throttle and dynamic changes were made one step at a time with settle pauses.
- [ ] Descents run primarily on dynamic, air held in reserve.
- [ ] Event recorder shows no unintended emergency or slip-induced surges.
