---
id: creative-arts.graphic-design.editorial-layout.contract-proofs-and-press-checks
name: contract-proofs-and-press-checks
category: creative-arts
field: graphic-design
product: editorial-layout
tags: [graphic-design, editorial-layout, print-colour, iso-12647, contract-proof, press-check, fogra-media-wedge, iso-12647-7, wet-proof, soft-proof, colour-approval, sign-off]
level: advanced
status: draft
description: "Approve colour with contract proofs (ISO 12647-7, Fogra media wedge) and run a press check: what to inspect, measuring against the proof, and signing off sheets."
sources:
  - https://www.iso.org/standard/72052.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Contract proofs and press checks

**Goal:** an agreed colour target before printing, and a printed result that matches it.

## Proof types
| Proof | What it shows | Contractual? |
|---|---|---|
| **Contract proof** (ISO 12647-7) | inkjet proof simulating the press condition, with a control strip | yes - the colour target |
| Digital/laser proof | layout and content, approximate colour | no |
| Soft proof (calibrated monitor) | colour preview | only if agreed (ISO 12646 conditions) |
| Wet proof / press proof | actual inks on actual paper | yes, expensive |

## Valid contract proof checklist
- Printed with the **correct simulation profile** (e.g. FOGRA51 for PSO Coated v3).
- Has a **control strip** (Fogra Media Wedge CMYK v3) and a **label**: file name, simulation profile, date, proofing
  system, measurement results (pass/fail against ISO 12647-7 tolerances, e.g. average delta E).
- Measured and passes - ask the printer for the verification label. A proof without a strip is not a contract proof.

## Viewing and approving
View under **ISO 3664 D50** lighting (see viewing conditions skill), not office light or a window. Mark changes with
clear notes; sign and date the approved proof - it becomes the reference on press.

## Press check (attending the print run)
1. Bring the signed contract proof and the spec (paper, colours, finishes).
2. Check the **make-ready sheet** under the press booth's D50 light: overall colour vs proof, critical colours (brand,
   skin, products), registration (loupe on fine type and rich blacks), ghosting, hickeys (spots), banding, paper is correct.
3. Ask the press operator for densitometer/spectro readings vs targets; adjust ink keys rather than demanding
   impossible matches (a contract proof shows the achievable target).
4. Check both sides and all signatures of a job; trims and folds on a folded dummy if possible.
5. **Sign the approved sheet** (OK sheet); it becomes the run reference.

## Gotchas
- Approving colour from a screen or office printer and then disputing the print - not defensible.
- Paper differs between proof and press (OBA brighteners): judge with the right profile and lighting.

## Verify
- [ ] Contract proof labelled, measured, signed.
- [ ] Press OK sheet signed against the proof under D50 lighting.
