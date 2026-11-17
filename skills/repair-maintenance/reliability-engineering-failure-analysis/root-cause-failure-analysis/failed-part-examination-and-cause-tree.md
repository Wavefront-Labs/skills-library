---
id: repair-maintenance.reliability-engineering-failure-analysis.root-cause-failure-analysis.failed-part-examination-and-cause-tree
name: failed-part-examination-and-cause-tree
category: repair-maintenance
field: reliability-engineering-failure-analysis
product: root-cause-failure-analysis
tags: [root-cause-failure-analysis, rcfa, rca, failure-analysis, fractography, fracture-surface, fatigue, beach-marks, ratchet-marks, overload, ductile-fracture, brittle-fracture, wear, corrosion, bearing-failure, 5-whys, cause-tree, fault-tree, fishbone, ishikawa, evidence-preservation, physical-roots, human-roots, latent-roots, corrective-action]
level: advanced
status: draft
description: "Investigate an equipment failure to its real cause: preserve evidence, read fracture and wear surfaces, build a verified cause tree to physical/human/latent roots, and prove the fix worked."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Failed-part examination and cause tree

**Goal:** find out why a part failed — the physical mechanism, the human decision
that allowed it, and the system weakness behind that — and fix it so it doesn't
recur. The output is a corrective action that is verified, not a blame report.

> Draft: field-level fractography only. Critical, legal or insurance cases need a
> metallurgical lab (SEM, hardness, chemistry, sectioning).

## 1. Preserve the evidence (first hour matters)
- **Don't clean, fit fracture halves together, or wire-brush** the surfaces — you
  destroy the marks. Don't let it go to scrap.
- Photograph in place before removal: orientation, surrounding damage, fluid
  levels, alignment marks, gauge readings.
- Tag and bag parts; protect fracture faces from corrosion (dry, light oil or
  desiccant bag; don't touch with bare fingers).
- Collect samples: lube oil, filters, debris, grease from bearings.
- Pull data: operating logs, DCS/SCADA trends, vibration history, work order history,
  recent changes (parts, procedures, people, process conditions).
- Interview operators and maintainers early, before stories settle.

## 2. Read the part
**Fractures** (use a 10× loupe and low-angle light):
| Mechanism | What you see |
|---|---|
| **Fatigue** (most common in rotating parts) | flat, smooth zone with **beach marks** curving away from the origin; **ratchet marks** at multiple origins = high stress; a small rough **final overload** zone. Small final zone = low nominal stress (stress raiser); large = high load |
| Ductile overload | rough, dull, fibrous, necking/deformation, 45° shear lips |
| Brittle overload | flat, granular/shiny, chevron marks pointing back to origin, little deformation |
| Torsional fatigue | ~45° spiral to shaft axis |
Look at the **origin**: keyway corner, thread root, sharp fillet, weld toe, corrosion
pit, machining mark — these are the stress raisers to fix.

**Wear and bearings:**
- Spalling/flaking on a raceway = surface fatigue (overload, end of life, or
  contamination dents starting it).
- Fluting (washboard) = electrical discharge through the bearing (VFD currents).
- False brinelling = vibration while stationary; true brinelling = impact overload.
- Discolouration blue/brown = overheating (lube failure, over-greasing, preload).
- Wear path off-centre or skewed = misalignment.
**Corrosion:** pitting, crevice, galvanic couples, stress corrosion cracking
(branched cracks), erosion-corrosion near turbulence.

## 3. Build the cause tree
Start with the failure event at the top; ask "how could this happen?" and list all
**hypotheses** at each level (an OR); only keep branches the evidence supports.
Three levels of root:
1. **Physical root:** the mechanism — "shaft fatigue from a sharp keyway corner under
   cyclic bending".
2. **Human root:** the decision/action — "replacement shaft machined without the
   drawing fillet radius".
3. **Latent root:** the system that allowed it — "no incoming inspection of
   machined spares; drawing not supplied to vendor".

5-Whys is fine for simple events, but forces a single chain — use a tree when there
could be several contributing causes. Ishikawa (fishbone) helps brainstorm
hypotheses: Machine, Method, Material, Man, Measurement, Environment.

**Test every hypothesis** with evidence (measurement, data, a test, a lab result)
and mark it verified/disproved. Unverified hypotheses aren't roots.

## 4. Corrective actions
- At least one action per verified root, latent ones included — physical-only fixes
  ("replace the shaft") guarantee recurrence.
- SMART: specific, owner, due date.
- Prefer elimination (design/spec change) over detection (inspection) over
  procedure/training.

## 5. Verify effectiveness
Define the check before closing: e.g. "no shaft failures over 12 months / next
3 overhauls", "fillet radius checked on next 5 spares", vibration within limit.
Close only when the check passes.

## Gotchas
- Assuming "operator error" ends the investigation; it's where it starts.
- Recent change is the single most productive question.
- A broken part is often a victim — a coupling failure caused by a misaligned motor.
- Cleaning the fracture with a wire brush destroys the most valuable evidence.

## Verify
- [ ] Evidence preserved and photographed before cleaning or reassembly.
- [ ] Failure mechanism identified from the surface, with origin located.
- [ ] Cause tree with each hypothesis marked verified or disproved by evidence.
- [ ] Physical, human and latent roots each have an action and owner.
- [ ] Effectiveness check defined and passed before closure.
