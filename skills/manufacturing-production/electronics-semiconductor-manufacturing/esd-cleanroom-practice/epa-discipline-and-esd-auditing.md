---
id: manufacturing-production.electronics-semiconductor-manufacturing.esd-cleanroom-practice.epa-discipline-and-esd-auditing
name: epa-discipline-and-esd-auditing
category: manufacturing-production
field: electronics-semiconductor-manufacturing
product: esd-cleanroom-practice
tags: [esd-cleanroom-practice, esd, electrostatic-discharge, epa, esd-protected-area, ansi-esd-s20-20, iec-61340-5-1, wrist-strap, heel-strap, esd-footwear, ground-point, dissipative-mat, ionizer, ionisation, field-meter, surface-resistance-meter, compliance-verification, esd-audit, esds, esd-sensitive, shielding-bag, insulators, cleanroom, gowning, iso-14644, contamination-control, pcba]
level: practitioner
status: draft
description: "Keep an ESD-protected area honest: daily personnel grounding checks, insulator control, packaging rules, and a periodic audit with field and resistance meters against ANSI/ESD S20.20 or IEC 61340-5-1."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# EPA discipline and ESD auditing

**Goal:** an ESD-protected area (EPA) where sensitive parts never meet an uncontrolled
charge — and evidence, from routine checks and audits, that it stays that way.
ESD damage is often **latent**: the part passes test and fails in the field, so
"we haven't seen failures" proves nothing.

## 1. The three principles
1. **Ground every conductor**, including people — wrist strap at seated stations,
   ESD footwear (heel straps/shoes) on a dissipative floor for standing/walking work.
2. **Remove or neutralise insulators** that can't be grounded — ordinary plastic
   bags, styrofoam cups, packing tape, clipboards, personal phones near product.
   Where a process-essential insulator stays (some plastic parts, tape), use an
   ionizer and keep it away from ESDS items (a common rule is >30 cm; check your
   programme's numbers).
3. **Protect parts outside the EPA** in shielding packaging (metallised static-shielding
   bags, conductive tote with lid). Pink "antistatic" poly is low-charging, not shielding.

The governing programme standard is **ANSI/ESD S20.20** or **IEC 61340-5-1**; your site's
ESD control plan states the actual limits.

## 2. Daily discipline (everyone)
- Test wrist strap and footwear at the **personnel tester** on entry, every shift;
  record the result (many testers log automatically and gate a turnstile).
- Wrist strap snug against skin, cord connected to the bench ground point — not to
  the mat edge, not dangling.
- Coats/smocks fastened and grounded where the plan requires it.
- Nothing personal on the bench. Paperwork in static-safe sleeves.
- Open shielding bags only on a grounded work surface while grounded.

## 3. Periodic audit (ESD coordinator)
Typical compliance-verification measurements (frequency per your plan — often
monthly to quarterly per workstation):
| Item | How | Typical requirement (confirm in your plan) |
|---|---|---|
| Work surface | Surface resistance point-to-ground meter | < 1×10⁹ Ω to ground |
| Wrist-strap cord | Continuity/resistance | ~1 MΩ resistor, < 3.5×10⁷ Ω system |
| Flooring + footwear | Person on floor with footwear to ground | < 3.5×10⁷ Ω, or walking body-voltage test |
| Ionizer | Charged-plate monitor | decay time and offset voltage in spec |
| Insulators | Electrostatic **field meter** | fields near ESDS items under the plan limit |
| Packaging | Surface resistance | per packaging spec |

Record results per station, flag fails, re-check after fix. Trend findings — the same
station failing repeatedly points at training, not equipment.

## 4. Common findings
- Wrist strap tester passes but the operator then unplugs to reach something.
- Dissipative mat contaminated with wax/polish cleaner → resistance climbs out of range.
  Use the mat manufacturer's cleaner.
- Ionizer emitter pins dirty → balance drifts; clean on schedule.
- Carts with plastic wheels or no drag chain carrying product across the EPA.
- Visitors entering without footwear checks.
- Tape dispensers and bubble wrap inside the EPA.

## 5. Cleanroom overlap
In a cleanroom (ISO 14644 classes) the gowning protocol adds particle control —
garments, gloves, gowning order top-down, no cosmetics, sticky mats. Cleanroom
garments are often also ESD garments; the ESD checks still apply.

## Verify
- [ ] Every person entering has a logged personnel test today.
- [ ] Audit results for each workstation within the plan's interval.
- [ ] No unexplained insulators within the plan's distance of ESDS items (field meter).
- [ ] ESDS items leave the EPA only in shielding packaging.

*Draft: limits shown are commonly cited S20.20 values from memory — the site's ESD
control plan is authoritative; verify before using as acceptance criteria.*
