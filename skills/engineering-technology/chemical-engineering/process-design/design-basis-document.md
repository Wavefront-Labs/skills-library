---
id: engineering-technology.chemical-engineering.process-design.design-basis-document
name: design-basis-document
category: engineering-technology
field: chemical-engineering
product: process-design
tags: [chemical-engineering, process-design, pd-design-basis-and-pfd, design-basis-document, design-basis, basis-of-design, process-specification, capacity, turndown, utilities-conditions, front-end-engineering, bod]
level: practitioner
status: draft
description: "Write the process design basis: capacity, feed and product specs, site and utility conditions, codes, margins and open items, so all disciplines design to one set of numbers."
sources:
  - "Towler and Sinnott Chemical Engineering Design, Turton et al. Analysis Synthesis and Design of Chemical Processes, Peters Timmerhaus and West Plant Design and Economics, Douglas Conceptual Design of Chemical Processes, NCEES FE and PE Chemical exam specifications"
  - "https://www.aiche.org"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Writing the design basis document

**Goal:** one controlled document that fixes the inputs to every calculation, issued before detailed design and changed only by formal revision.

## Contents (typical order)
1. **Purpose and scope**: what is designed, battery limits, what is excluded.
2. **Capacity**: nameplate production rate, on-stream hours per year (state yours, 8,000 to 8,400 h/y is typical for continuous plants), turndown (often 50 to 60% of design is asked for), future expansion allowance.
3. **Feedstocks**: composition ranges (normal, worst case), impurities, delivery state and conditions, contract limits.
4. **Products and by-products**: specifications (purity, water, colour, etc.), delivery conditions, storage days.
5. **Site conditions**: ambient dry/wet bulb design temperatures, altitude, seismic and wind zone references, soil, elevation, space.
6. **Utilities**: steam levels (pressure and temperature at battery limit), cooling water supply/return and fouling limits, instrument air dew point, nitrogen purity, power voltages, fuel, water quality.
7. **Effluents and emissions**: limits and the permit basis; name the regulator and the date of the rule used.
8. **Codes and standards**: pressure vessel, piping, electrical area classification, relief; state the jurisdiction and edition used.
9. **Design margins**: sizing allowances on flow, duty, pump head, relief, and who owns each.
10. **Safety philosophy**: inherently safer choices, hazard studies planned, SIL policy.
11. **Open items and assumptions** with owners and due dates.

## Practice
- Give each number a source (client letter, laboratory report, vendor data) and a date.
- Keep one margin per quantity; stacking margins at every step oversizes equipment.
- Review with operations, maintenance, safety and the client before freezing.

## Gotchas
- Cooling-water and steam conditions at the battery limit differ from those at the user; define the allowable drop.
- "Maximum" and "design" are different words: define both.
- Unstated on-stream hours silently change yearly production by 5 to 10%.

## Verify
- [ ] Every sizing calculation cites a design-basis line.
- [ ] Revision, owner and sign-off recorded; changes tracked.
