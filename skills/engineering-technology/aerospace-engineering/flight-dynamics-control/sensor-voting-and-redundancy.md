---
id: engineering-technology.aerospace-engineering.flight-dynamics-control.sensor-voting-and-redundancy
name: sensor-voting-and-redundancy
category: engineering-technology
field: aerospace-engineering
product: flight-dynamics-control
tags: [sensor-voting, redundancy-management, mid-value-select, miscompare, fault-detection, envelope-protection]
level: practitioner
status: verified
description: "Design sensor voting and redundancy management for flight control: mid-value select, miscompare thresholds, persistence, and common-mode risks."
sources:
  - "SAE ARP4754A"
  - "SAE ARP4761"
  - "Stevens and Lewis, Aircraft Control and Simulation"
  - "FAA AC 25.1309-1B (it cancelled AC 25.1309-1A on 2024-08-30, per faa.gov)"
  - "SAE ARP4754B and ARP4761A are later revisions of the ARP documents above (confirm current)"
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# Sensor voting and redundancy

**Goal:** a consolidated sensor value that remains usable, and an accurate alert, after sensor failures.

## Architectures
- **Triplex** (three sensors): mid-value select passes the median and rejects one outlier.
- **Quadruplex**: tolerates two sequential failures with voting plus monitoring.
- **Dual with monitoring**: detects a miscompare but cannot say which sensor is wrong without extra information (a third source or analytic estimate).
- **Analytical redundancy**: compare against a model-based estimate (for example pitch rate from attitude rate or air data from inertial and GPS data).

## Monitor design
1. Compute the difference of each sensor from the consolidated value.
2. Set the miscompare threshold above the worst-case sensor tolerance plus dynamic and lag mismatch plus an allowance (too tight gives nuisance alerts, too loose delays detection).
3. Add persistence: a failure is declared only after the threshold is exceeded for a time (or a number of samples), tuned for the allowed transient from a hard-over failure.
4. Latch failures; allow reset only per procedure.
5. Exchange data across channels; synchronise sample times to avoid false mismatches in dynamic flight.
6. Define what happens at degraded sensor counts (reversion, see control-law-reversion).

## Common-mode risks
- Identical sensors sharing a failure mode (icing of similar pitot probes, blocked static ports, software error).
- Use dissimilar sources where the safety assessment needs it, and analyse common-cause failures per the system safety process.

## Gotchas
- Surviving sensors must still be accurate enough in a failed state: do not let thresholds drift to accommodate errors.
- Mid-value select is vulnerable when two sensors fail together with similar error.

## Verify
- [ ] Hard-over, drift and stuck failure injections in simulation are detected within the allowed time with bounded surface transient.
