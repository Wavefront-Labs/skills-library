---
id: transportation-logistics.railway-signalling.panel-relay-interlockings.nx-route-setting-and-panel-failures
name: nx-route-setting-and-panel-failures
category: transportation-logistics
field: railway-signalling
product: panel-relay-interlockings
tags: [panel-relay-interlockings, nx-panel, entrance-exit, entrance-exit-panel, route-setting, route-relay-interlocking, rri, relay-interlocking, track-circuit, track-circuit-indications, track-occupied, approach-locking, route-locking, sectional-route-release, route-cancel, emergency-replacement, points-indication, points-failure, track-circuit-failure, panel-failure, signaller, signalman, control-panel, mimic-panel]
level: practitioner
status: draft
description: "Operate an entrance-exit (NX) panel and relay interlocking: set and cancel routes, read track-circuit and points indications, understand approach and route locking, and respond to panel failures."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# NX route setting and panel failures

**Goal:** set the right routes at the right time on an entrance-exit panel, know what
every light means, and recognise when the panel is showing a failure rather than a
train.

*Draft: indication colours and button conventions differ (e.g. UK red/white track
lighting, white route lights, flashing for in-progress). Use your panel's legend.*

## 1. Reading the panel
- **Track circuits:** usually unlit/grey = clear, red = occupied. A red that appears
  where no train should be = possible track-circuit failure or an obstruction
  (broken rail, something shorting the rails).
- **Routes set:** a white/yellow line along the route.
- **Points:** normal/reverse indication; *flashing or no indication* = points out of
  correspondence (not detected in either position).
- **Signals:** red/green aspect lamps or "off" indicators per signal.

## 2. Setting a route (NX)
1. Press the **entrance** button (the signal), then the **exit** button (the next
   signal or end point).
2. The interlocking checks the route is free, points can move, and no conflicting
   route is set; it moves points, detects them, then clears the signal.
3. **Confirm:** route lit, points detected, signal shows off. If the signal stays at
   danger, look for the reason (a track circuit occupied, points not detected,
   approach-control conditions, a conflicting route).
4. Set routes in good time but not so early that you lock up other moves you'll need.

## 3. Locking you must understand
- **Approach locking:** once a train is approaching a cleared signal, cancelling the
  route will put the signal to danger but the route stays locked for a timed period
  (often around 2 minutes — *check your interlocking*) so points can't move under
  a train that can't stop.
- **Route locking / sectional route release:** as the train passes, sections of the
  route release behind it. A section that stays locked after the train has clearly
  gone = a track-circuit not clearing.

## 4. Cancelling
- Press the cancel (or entrance + cancel) for the route. Expect the timer if approach
  locked. Never cancel a route in front of a train to "fix" a mistake unless safety
  requires it — the driver may be at the signal; replacement in front of a train is a
  last-resort emergency action and a reportable event.

## 5. Panel failures — recognise them
| What you see | Likely failure | First action |
|---|---|---|
| Track circuit red, no train expected | TC failure or obstruction | Treat as possible obstruction; don't route trains into it without examination/caution authority |
| Points no indication after move | Points failure / obstruction | Try once to swing normal-reverse; then call technicians |
| Whole area dark or frozen | Power/communications failure | Stop trains into the area; follow failure arrangements |
| Signal won't clear, all conditions met | Lamp/signal failure | Report, use degraded working |

For what to do next, see
transportation-logistics.railway-signalling.signalling-degraded-working.authorising-trains-past-failed-signals.

## Gotchas
- A track circuit "dropping" behind a train can mean the train has divided.
- Two-button mis-press: entrance pressed for the wrong signal; check before exit.
- Don't trust a familiar pattern — read the actual indications each time.

## Verify
- [ ] Every route checked lit, points detected, signal off before relying on it.
- [ ] Unexplained track-circuit occupancy treated as a possible obstruction.
- [ ] Failures logged with time, location and actions, and technicians called.
- [ ] No route cancelled in front of a train except in emergency.
