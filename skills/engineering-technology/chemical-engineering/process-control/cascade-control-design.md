---
id: engineering-technology.chemical-engineering.process-control.cascade-control-design
name: cascade-control-design
category: engineering-technology
field: chemical-engineering
product: process-control
tags: [chemical-engineering, process-control, pc-advanced-regulatory-control, cascade-control-design, cascade-control, primary-controller, secondary-controller, inner-loop, outer-loop, disturbance-rejection, jacket-temperature, flow-cascade]
level: practitioner
status: gated
description: "Design cascade control: choose the secondary variable, tune the inner loop first then the outer loop, check speed ratio and handle windup and tracking."
sources:
  - "Seborg Edgar Mellichamp and Doyle Process Dynamics and Control, Smith and Corripio Principles and Practice of Automatic Process Control, Luyben Process Modeling Simulation and Control, Skogestad Multivariable Feedback Control, ISA-18.2"
  - "https://www.aiche.org"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Cascade control design

**Goal:** a faster rejection of disturbances that enter before the main controlled variable responds.

## When to use
The secondary variable must (1) respond to the manipulated variable faster than the primary, (2) be affected by the main disturbances, and (3) be measurable. Examples: reactor temperature (primary) with jacket temperature (secondary), column temperature with steam flow, temperature controller manipulating a flow controller setpoint (to isolate valve nonlinearity and supply pressure upsets).

## Design
1. Choose the secondary; check that the inner loop dynamics are at least about 3 to 5 times faster than the outer loop (time constant ratio; a rule of thumb (gated: unconfirmed, source is paywalled or blocked)).
2. Tune the **inner loop** first, with the outer controller in manual (or the secondary in local setpoint), using the standard methods (a flow loop is fast and often tuned with a low gain and a short integral time).
3. Put the secondary in remote (cascade) mode; tune the **outer loop** treating the closed inner loop as part of the process (the process seen by the outer controller is faster than the original).
4. Use PI in the secondary (or P-only when small offset is acceptable, since the outer integral will remove the offset); PI or PID in the primary.

## Implementation details
- **Windup**: use external reset (tracking) so that when the secondary saturates the primary stops integrating.
- **Initialisation**: when switching to cascade, the primary output initialises to the secondary measurement.
- Matching ranges and engineering units between primary output and secondary setpoint.

## Gotchas
- A secondary that is not faster than the primary gives nothing and can destabilise.
- Interaction with tight inner loops that saturate valves.
- The inner measurement must be reliable; failure should return the loop to a safe mode.

## Verify
- [ ] Disturbance step in the inner variable is rejected faster than in simple feedback (compare).
- [ ] Windup protection tested.
