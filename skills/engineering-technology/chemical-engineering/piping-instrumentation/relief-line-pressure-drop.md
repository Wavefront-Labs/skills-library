---
id: engineering-technology.chemical-engineering.piping-instrumentation.relief-line-pressure-drop
name: relief-line-pressure-drop
category: engineering-technology
field: chemical-engineering
product: piping-instrumentation
tags: [chemical-engineering, piping-instrumentation, pi-layout-and-steam-systems, relief-line-pressure-drop, relief-line, inlet-pressure-drop, back-pressure]
level: practitioner
status: gated
description: "Check pressure drop in relief valve inlet and outlet lines: the inlet loss limit and built-up back pressure against valve type limits."
sources:
  - "Crane Technical Paper 410, Perry Chemical Engineers Handbook, ASME B31.3, ISA-5.1, Darby Chemical Engineering Fluid Mechanics, Karassik Pump Handbook"
  - "https://www.isa.org"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Relief line pressure drop

**Goal:** Check pressure drop in relief valve inlet and outlet lines: the inlet loss limit and built-up back pressure against valve type limits.

## Steps
1. Inlet line loss at rated flow should not exceed a limit commonly stated as 3 percent of the set pressure for conventional spring valves (API 520 Part II guidance (gated: unconfirmed, source is paywalled or blocked); recent editions allow exceeding it only by engineering analysis, so confirm the edition and any local rule).
2. Calculate the inlet loss at the rated capacity, not the required flow, unless company practice states otherwise.
3. Outlet line: calculate the built-up back pressure with the tail pipe and header at the maximum simultaneous flow; compare with the limit for the valve type (conventional, balanced bellows or pilot operated).
4. Reduce the losses by shortening the inlet pipe, increasing the diameter, or using a balanced or pilot valve for high back pressure.
5. Check the reaction forces and the support for the discharge line.

## Gotchas
- Chatter occurs with excessive inlet loss.
- Back pressure limits vary by valve type; check the vendor and the standard.

## Verify
- [ ] Inlet loss is below the limit used.
- [ ] Back pressure is below the valve limit for all scenarios.
