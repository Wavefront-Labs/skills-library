---
id: engineering-technology.technical-authentication-testing.failure-analysis.fracture-surface-root-cause-analysis
name: fracture-surface-root-cause-analysis
category: engineering-technology
field: technical-authentication-testing
product: failure-analysis
tags: [failure-analysis, fractography, root-cause-analysis, rca, fracture-surface, beach-marks, fatigue-striations, dimples, cleavage, intergranular, sem, eds, stereo-microscope, ductile-fracture, brittle-fracture, fatigue, fishbone, ishikawa, five-whys, fault-tree-analysis, evidence-preservation, chain-of-custody, asm-handbook-vol-11, metallography, failure-report]
level: advanced
status: draft
description: "Find why a metal part broke: preserve evidence, NDT first, read the fracture (beach marks, striations, dimples, cleavage) with stereo/SEM/EDS, then prove root cause with 5-whys/fault tree."
sources: ["ASM Handbook Vol. 11: Failure Analysis and Prevention", "ASM Handbook Vol. 12: Fractography", "ASTM E2332 Standard Practice for Investigation and Analysis of Physical Component Failures", "ASTM E1188 Standard Practice for Collection and Preservation of Information and Physical Items by a Technical Investigator", "ASTM E3 Preparation of Metallographic Specimens"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Fracture-surface root-cause analysis — from broken part to proven cause

**Goal:** establish the fracture mechanism, the origin, and the root cause (design, material, manufacturing, or service) with evidence that survives peer review, without destroying information along the way.

## 1. Preserve before you look

- Photograph the part in situ, mating halves, surrounding assembly, and all fragments with a scale bar and orientation marks **before** anything is moved.
- Start a chain-of-custody log (ASTM E1188-style): who, when, where stored, every transfer. For contested or insured losses, agree a joint test protocol with all parties before any destructive step.
- **Never fit mating fracture faces back together** — it smears striations and crushes the origin. Do not clean with wire brushes or acids. Protect surfaces with a desiccant bag or a light rust-preventive that is removable with acetone; record what you applied.
- Collect service history, drawing revision, material certs, and other failures from the same lot.

## 2. Non-destructive work first (order matters)

1. Visual and stereo microscope (5-50x): macro features, origin location, colour/oxide tint.
2. Dimensional check against drawing; hardness on a non-critical area.
3. NDT of sister parts and the remaining body: magnetic particle or penetrant for secondary cracks, radiography/CT for internal porosity. See engineering-technology.technical-authentication-testing.nondestructive-testing.ultrasonic-flaw-detection-and-sizing.
4. Replicas (acetate tape with acetone) of the surface if you will cut it.
5. Only then: cleaning (ultrasonic acetone, then replica-stripping; inhibited chemical cleaners only if justified), sectioning, SEM.

## 3. Read the fracture

| Mechanism | Macro | Micro (SEM) |
|---|---|---|
| Ductile overload | Shear lips at 45°, cup-cone, necking, matte grey | Equiaxed dimples (tension), elongated/parabolic dimples (shear/tear) |
| Brittle overload (cleavage) | Flat, bright, chevrons pointing back to origin, no deformation | Cleavage facets, river patterns converging on initiation |
| Intergranular | Flat, granular "rock candy" | Clean grain facets — suspect hydrogen, temper embrittlement, SCC, liquid-metal embrittlement |
| Fatigue | Smooth zone with beach (clamshell) marks, ratchet marks at multiple origins, final rough overload zone | Striations, one per cycle where resolvable, perpendicular to growth |

Interpretation rules of thumb:
- **Size of final overload zone vs. fatigue zone** indicates nominal stress: large overload zone = high stress; small = low stress, long life.
- Many ratchet marks = high stress concentration (multiple origins). Bending gives one-sided (unidirectional) or two-sided (reversed) origins; rotating bending skews the final zone against rotation direction.
- Striation spacing gives a local crack growth rate (da/dN); counting back can estimate cycles, but do not over-claim — striation absence does not rule out fatigue.
- EDS at the origin: look for inclusions (MnS, alumina), corrosion products (Cl, S), or plating residues. EDS is semi-quantitative; light elements (C, N, O) are unreliable — confirm composition with OES or wet chemistry on bulk material.

## 4. Confirm with metallography and testing

Section perpendicular to the fracture through the origin. Check microstructure (decarburisation, untempered martensite, grain size, case depth, porosity, laps/seams), hardness traverse, and chemistry vs. spec. Mechanical tests (tensile, Charpy) on sister material if material deficiency is suspected.

## 5. Root cause, not mechanism

"Fatigue" is a mechanism, not a cause. Drive to the controllable cause:
- **Fishbone (Ishikawa):** Material, Method (manufacturing), Machine, Measurement, Man, Environment, Design — list candidate causes, then mark each supported/refuted by evidence.
- **5-whys:** e.g. fatigue origin -> sharp undercut at fillet -> radius not machined to drawing -> worn insert not detected -> no in-process fillet gauge. The last answer is what you fix.
- **Fault tree (top-down, AND/OR gates)** when multiple contributing conditions must coexist; each basic event gets a status: confirmed, eliminated, or not testable.
Every hypothesis must be tested against all evidence; one contradictory fact kills it.

## 6. Report structure

Summary (conclusion first) / background and service history / items received and custody / examination (visual, NDT, fractography, metallography, chemistry, hardness) with annotated images / analysis and eliminated hypotheses / conclusions with confidence level / recommendations (corrective and preventive) / appendices. 

## Gotchas

- Post-fracture damage (rubbing, oxidation) can erase striations near the origin — look slightly downstream.
- Hydrogen embrittlement fractures can look like overload macroscopically; check plating history and delay between assembly and fracture.
- The first broken part may be the victim, not the culprit — reconstruct the fracture sequence across all fragments.

## Verify

- [ ] Chain of custody and pre-disturbance photos exist for every item.
- [ ] All NDT and replicas were done before any destructive step.
- [ ] Origin is located and the mechanism is supported by both macro and micro evidence.
- [ ] Material chemistry, hardness and microstructure were checked against spec.
- [ ] Root cause is a controllable condition, with all alternative hypotheses explicitly eliminated.
- [ ] Report separates facts from opinions and states confidence.
