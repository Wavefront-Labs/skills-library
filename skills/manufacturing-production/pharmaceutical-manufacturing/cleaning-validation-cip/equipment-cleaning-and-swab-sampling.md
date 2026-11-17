---
id: manufacturing-production.pharmaceutical-manufacturing.cleaning-validation-cip.equipment-cleaning-and-swab-sampling
name: equipment-cleaning-and-swab-sampling
category: manufacturing-production
field: pharmaceutical-manufacturing
product: cleaning-validation-cip
tags: [cleaning-validation-cip, cleaning-validation, cip, sip, clean-in-place, steam-in-place, manual-cleaning, changeover-cleaning, swab-sampling, rinse-sampling, toc, total-organic-carbon, conductivity, visual-clean, maco, pde, ade, hbel, dirty-hold-time, clean-hold-time, cross-contamination, product-changeover, sinner-circle, cleaning-agents, cip-100, cip-200, pharmaceutical-manufacturing, gmp]
level: practitioner
status: draft
description: "Clean pharma equipment so it passes: run and verify CIP/SIP, perform manual cleaning to SOP, take swab and rinse samples correctly, respect dirty/clean hold times and prevent cross-contamination."
sources:
  - "https://www.ecfr.gov/current/title-21/part-211/subpart-D/section-211.67"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Equipment cleaning and swab sampling

**Goal:** after cleaning, the next product sees no meaningful residue of the previous
product, cleaning agent or microbes — and you can prove it. Cleaning validation sets the
limits; your execution decides whether every routine clean actually meets them.

## 1. The four levers (Sinner's circle)
Chemistry (agent + concentration), Temperature, Time, Mechanical action. A validated
procedure fixes all four. Cutting one (shorter soak, cooler water, less scrubbing) is a
change to a validated process, not a shortcut.

## 2. CIP/SIP cycles (automated)
Typical CIP: pre-rinse → caustic wash (use the validated agent and concentration) at temperature
→ rinse → acid wash (if validated) → rinse → final rinse with purified water/WFI →
(drain/air blow) → SIP if required.
- **Before starting:** correct circuit selected, spray devices fitted, transfer panels/
  swing bends in the right position, manual valves per the line-up sheet, detergent stock levels.
- **Watch the cycle report:** each step's temperature, flow/supply pressure (spray balls
  need minimum flow to cover), conductivity and time. A step that "passed" with flow below
  minimum didn't clean the top of the tank.
- **SIP:** temperature at the coldest point (usually the drain) must reach the validated temperature for the set time;
  condensate drainage matters — a cold spot from trapped condensate fails the cycle.
- The final rinse conductivity/TOC is often the release check; record it.

## 3. Manual cleaning
- Disassemble to the level the SOP specifies (gaskets, valve seats, feed frames,
  punches, blender seals — residue hides there).
- Use only the listed agents at listed concentration, listed brushes/cloths (non-shedding).
- Rinse to the specified volume/temperature; dry fully (wet equipment grows microbes).
- **Visual inspection:** under good light, with inspection mirror/torch for internals. "Visually
  clean" is usually the first acceptance criterion; anything visible = reclean.

## 4. Swab and rinse sampling
**Swab (for direct surface sampling of hard-to-clean spots):**
1. Use the specified swab (often low-TOC polyester) and wetting solvent.
2. Sample the defined area (with a template) at the
   **predefined location** in the sampling plan — the worst-case spots, not the
   easiest to reach.
3. Stroke pattern per method: e.g. horizontal strokes one side of the swab, then vertical
   strokes with the flipped side, overlapping, with firm pressure.
4. Put the head in the labelled vial, cut/snap the handle without touching the head.
5. Record location, area, time; deliver to lab within the sample hold time.
6. Take a **field blank** if the method requires one.

**Rinse samples** cover large or inaccessible surfaces: collect the specified volume at the
specified point in the final rinse.

Lab tests may be product-specific or non-specific plus
bioburden/endotoxin where relevant. Limits are set by the validation team, not by you; follow the method.

## 5. Hold times and status
- **Dirty hold time:** max time between end of use and start of cleaning — residues
  dry and harden.
- **Clean hold time:** max time clean equipment can wait before reuse (or re-clean).
- Status labels (Dirty / Clean, with date, time, by whom, expiry) on every item. An item
  without a status label is dirty.

## Gotchas
- Swabbing "the bit you can reach" instead of the mapped worst-case location.
- Touching the swab head or vial inside with gloves.
- A rinse sample taken from a tap that wasn't flushed.
- CIP returning "complete" after a manual override of a low-flow alarm.
- Mixing up dedicated vs shared parts (e.g. highly potent product tooling).

## Verify
- [ ] CIP/SIP report: every step at required temperature, flow and time; final rinse in spec.
- [ ] Manual clean: SOP disassembly done, visual inspection passed and signed.
- [ ] Swabs from the mapped locations, correct area, blank taken, within sample hold time.
- [ ] Dirty and clean hold times respected; status labels correct and dated.

## Checked

Date: 2026-10-25. Jurisdiction: United States (FDA 21 CFR 211.67, eCFR current text).

Confirmed: 211.67(c) requires records of maintenance, cleaning, sanitising and inspection as specified in 211.180 and 211.182, consistent with the status-label and record steps here. Removed as unconfirmed: SIP 121 °C, detergent concentrations and trade names, swab areas and the PDE/ADE statement. The rest is procedure and craft that was not tied to a primary source, so the skill stays draft.

Method: documentation only; no commands were run.
