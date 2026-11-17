---
id: engineering-technology.chemical-engineering.process-control.split-range-and-override-control
name: split-range-and-override-control
category: engineering-technology
field: chemical-engineering
product: process-control
tags: [chemical-engineering, process-control, pc-advanced-regulatory-control, split-range-and-override-control, split-range-control, override-control, selector, high-select, low-select, constraint-control, valve-sequencing, pressure-control, anti-windup]
level: practitioner
status: draft
description: "Configure split-range control for two valves on one controller and override (selector) control for constraint handling, with sequencing, overlap and windup protection."
sources:
  - "Seborg Edgar Mellichamp and Doyle Process Dynamics and Control, Smith and Corripio Principles and Practice of Automatic Process Control, Luyben Process Modeling Simulation and Control, Skogestad Multivariable Feedback Control, ISA-18.2"
  - "https://www.aiche.org"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Split-range and override control

**Goal:** use one controller output for two actuators, or protect process limits with selector logic.

## Split-range
One controller output 0 to 100% operates two valves in sequence: for example valve A (0 to 50% output opens 0 to 100%) and valve B (50 to 100% output opens 0 to 100%). Typical use: pressure control with a vent and an inert gas make-up; heating and cooling for a temperature loop (cooling valve over 0 to 50%, heating valve over 50 to 100%).
Design notes:
1. Choose a small overlap or a deadband (for example 2 to 5%) to avoid fighting actuators and to compensate valve hysteresis.
2. Match the valve gains (different sizes and characteristics) so that the loop gain does not jump at the transition; use output characterisation (a two-segment curve).
3. Tuning at the transition region is the hardest; tune for the slower/higher-gain side.

## Override (selector) control
Two or more controllers share one final element via a high or low selector. Normal controller holds the primary variable; the override controller takes over when a constraint is approached (for example high pressure override on a feed flow, low suction pressure override on compressor speed).
Rules:
1. Low selector for "do not exceed" constraints that close the valve; high selector for "do not fall below".
2. **The non-selected controller must be protected from windup**: use external reset feedback from the selected output.
3. Set the override controller's setpoint beyond the normal operating point (for example 5% closer to the limit) but inside the protective trip.
4. Document the logic on the P&ID/control narrative; test each constraint.

## Gotchas
- Overrides are not safety systems; independent protective systems must exist for hazards (see the SIL skills).
- Selector with two controllers sharing the same measurement can chatter.

## Verify
- [ ] Simulation or test shows smooth transfer between controllers without windup.
- [ ] Split-range transition region tested for hunting.
