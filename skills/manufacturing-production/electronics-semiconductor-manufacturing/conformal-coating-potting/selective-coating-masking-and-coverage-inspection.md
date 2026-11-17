---
id: manufacturing-production.electronics-semiconductor-manufacturing.conformal-coating-potting.selective-coating-masking-and-coverage-inspection
name: selective-coating-masking-and-coverage-inspection
category: manufacturing-production
field: electronics-semiconductor-manufacturing
product: conformal-coating-potting
tags: [conformal-coating-potting, conformal-coating, selective-coating, nordson-asymtek, pva, acrylic, ar, silicone, sr, urethane, ur, uv-cure, parylene, masking, keep-out-zones, uv-inspection, uv-tracer, black-light, wet-film-thickness, dry-film-thickness, ipc-cc-830, ipc-a-610, dewetting, bubbles, cleanliness, ionic-contamination, potting, encapsulation, pcba]
level: practitioner
status: draft
description: "Run a selective conformal coating job: board cleanliness, masking keep-outs, robot program and fluid control, cure, and UV-light coverage and thickness inspection with common defect causes."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Selective coating, masking and coverage inspection

**Goal:** coating everywhere the drawing says, nowhere it must not be (connectors,
test points, switches, heat-sink contact areas), at the specified thickness, fully
cured — and proof of that for every board.

## 1. Know the coating and the drawing
- Coating type (IPC-CC-830 / IEC families): **AR** acrylic (easy rework), **UR**
  urethane, **SR** silicone (wide temperature, harder rework), **ER** epoxy, **UV-cure**
  hybrids, **XY** parylene (vapour-deposited, different process entirely).
- The coating drawing defines **must-coat areas, keep-out areas** and thickness range.
  Keep-outs are where field failures and customer rejects come from.

## 2. Board preparation
- Coating seals in whatever is on the board. Flux residue and ionic contamination
  under coating cause dendrites and adhesion failure. If the line uses no-clean flux,
  confirm the product is approved to be coated over it; otherwise clean and verify
  cleanliness (ionic test such as ROSE, or the site's SIR/IC method).
- Dry the board after cleaning; moisture trapped under coating → blistering.
- Handle with gloves from here on; fingerprints show as dewetting.

## 3. Masking
- Selective robots (e.g. Nordson ASYMTEK, PVA) avoid most masking, but tall
  connectors, through-hole openings that wick coating, and some keep-outs still need
  **masking**: boots, caps, dots, tape or peelable liquid mask.
- Mask so the edge is crisp; tape lifted at the edge lets coating creep under.
- Count masks on and masks off — a forgotten mask is a shipped defect.

## 4. Robot program and fluid control
- Spray/film/needle valves per area; edges near keep-outs done with needle or narrow
  film. Confirm program revision matches the board revision.
- Fluid **viscosity** changes with temperature and solvent loss; check it at start
  of shift (cup or inline). Wrong viscosity → bad edge definition and thickness.
- Check pattern width on a test card or bare panel before running product; clogged
  nozzles give stripes and misses.

## 5. Cure
Follow the datasheet: ambient/moisture cure, heat, or UV. UV-cure coatings under
components (shadow areas) need a secondary cure mechanism — confirm the product has
one if parts shadow coating. Undercured coating is soft and tacky and fails
adhesion/insulation.

## 6. Inspection
- Most coatings contain a **UV tracer**: inspect under UV (black) light for coverage,
  voids, bubbles, splash into keep-outs. Use a defined lighting setup and magnification.
- **Thickness**: wet-film gauge during process set-up; dry-film by eddy-current gauge
  on a coupon or flat area, or by sectioning/micrometer per site method. Too thick
  causes cracking (especially silicones and acrylics on thermal cycling).
- Classify per IPC-A-610 coating criteria and the drawing.
- Automated coating inspection (UV AOI) exists on high-volume lines.

## Defect causes
| Defect | Likely cause |
|---|---|
| Dewetting / fisheyes | Contamination (silicone, flux, fingerprints) |
| Bubbles | Too thick, too viscous, trapped air from agitation, fast heat cure |
| Coating in connector | Missing/failed mask, wicking through vias or pins |
| Thin/missed at component edges | Program path, shadowing, tilt angle not used |
| Cracking | Over-thickness, cure too fast, thermal mismatch |

## Potting, briefly
Potting/encapsulation (two-part epoxy, urethane, silicone) uses metered mix
dispensers: watch mix ratio, degassing, pot life and exotherm in large volumes.
Potted assemblies are effectively non-repairable — test before potting.

## Verify
- [ ] Cleanliness confirmed before coating.
- [ ] Every keep-out clean under UV; masks fully removed.
- [ ] Thickness within the drawing range on the defined coupon/location.
- [ ] Cure verified (tack-free, per datasheet schedule).

*Draft: cleanliness test methods and thickness ranges depend on the customer spec;
generalised here.*
