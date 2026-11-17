---
id: engineering-technology.technical-drawing-cad.cad-data-management.revision-and-release-control
name: revision-and-release-control
category: engineering-technology
field: technical-drawing-cad
product: cad-data-management
tags: [pdm, plm, cad-data-management, part-numbering, non-significant-part-numbers, intelligent-part-numbers, revision-control, revisions, release-process, lifecycle-states, ecr, eco, ecn, change-management, form-fit-function, interchangeability, effectivity, where-used, bom, ebom, mbom, bom-integrity, metadata, title-block, check-in-check-out, solidworks-pdm, autodesk-vault, windchill, teamcenter, enovia, 3dexperience, onshape, asme-y14.35, asme-y14.100, step-ap242]
level: practitioner
status: draft
description: "Control CAD revisions and releases: intelligent vs non-significant part numbers, rev letters, form-fit-function rule, WIP/released states, ECOs and BOM integrity."
sources: ["ASME Y14.35 and ASME Y14.100 (scope and concepts only)", "Vendor documentation for SOLIDWORKS PDM, Autodesk Vault, PTC Windchill, Siemens Teamcenter, Onshape release management"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Revision and release control for CAD data

**Goal:** at any moment anyone can answer "what is the current released design of
this part, what changed since the last one, and what does it affect?", and nothing
reaches a supplier that wasn't released.

## 1. Part numbers: identity, not description
1. Prefer **non-significant** (sequential) numbers, e.g. `100234`, with the meaning
   held in metadata (description, category, material). Intelligent numbers like
   `BRK-AL-80-03` run out of codes, break when a part changes category, and invite
   people to "fix" the number when the design changes.
2. One number identifies one interchangeable item. Drawing and model share it (or a
   fixed suffix scheme) and share the revision.
3. Inside a PDM, **file name = part number**; title, revision and state are
   properties, not file-name text. `bracket_final_v3_REV-C.sldprt` is a symptom of no
   system.

## 2. Revise or renumber: the form-fit-function rule
Ask: will an existing stock part still work everywhere it is used?
- **Yes, interchangeable** (drawing clarification, tolerance loosened with no
  functional effect, cosmetic change) - **new revision**, same part number.
- **No** (mounting holes moved, material changed in a way that matters, mass or
  strength changed so users must care) - **new part number**. Then walk up the
  where-used list: each parent assembly that is no longer interchangeable also gets a
  new number; stop at the level where interchangeability is restored.
Run **where-used** before deciding; the answer depends on every product using it.

## 3. Revision schemes
A common convention (consistent with ASME Y14.35 practice, check your company
procedure):
- Pre-release / prototype iterations numeric (`01, 02, ...`) or a dash.
- First release **A**, then B, C...; skip letters easily confused with digits
  (I, O, Q, S, X, Z); after Y comes AA.
- PDM **versions** (every check-in) are not **revisions**; only a release bumps the
  revision. Keep that distinction visible to users.

## 4. Lifecycle states and who can do what
Typical workflow:
```
WIP  ->  In Review  ->  Released  ->  (Obsolete)
 ^                          |
 +---- ECO opens new rev ---+
```
- **WIP**: author has write access; check out / check in.
- **In Review**: read-only; checker and approver sign (title-block fields fill from
  the workflow transition).
- **Released**: read-only for everyone; PDF/STEP derivatives generated automatically.
- Changes to released items go through **ECR** (request, why) then **ECO/ECN** (order:
  what changes, affected items, disposition of stock and WIP, effectivity by date,
  lot or serial).
Named systems: SOLIDWORKS PDM, Autodesk Vault, PTC Windchill, Siemens Teamcenter,
3DEXPERIENCE/ENOVIA (maturity states), Onshape release management, Fusion with Fusion
Manage. State names differ; the logic is the same.

## 5. BOM integrity from CAD
1. Every component in the model has a part number, description, quantity and unit;
   bulk items (adhesive, cable, grease) get a BOM line with unit "as required" or a
   length/volume.
2. Exclude reference, envelope and fixture geometry from the BOM (each CAD has a
   "reference" or "exclude from BOM" flag); otherwise the EBOM orders a skeleton part.
3. Map CAD properties to title-block fields so drawings can't disagree with PDM.
4. The engineering BOM (as designed) feeds the manufacturing BOM (as built, with
   phantoms, kits and consumables); changes flow EBOM to MBOM via the ECO, never by
   hand-editing the ERP copy only.

## 6. Release package
Drawing PDF (the contractual document in most shops), neutral 3D (STEP AP242
preserves PMI where AP203/AP214 don't), native files if the supplier needs them, all
at the same revision. Stamp or watermark non-released prints "PRELIMINARY".

## Worked mini-example
Bracket `100234` rev B: a supplier asks to loosen an edge-break tolerance - rev C,
same number. Later, its holes move 5 mm to suit a new motor: old brackets don't fit
the old motor plate, so the bracket becomes `100517` rev A, and its parent assembly
`200045` becomes `200088` because a spare assembly is no longer interchangeable.

## Gotchas
- Pack-and-Go / Save As copies outside the vault create orphan duplicates with the
  same number; ban them or purge them.
- Renaming files outside the CAD/PDM tool breaks assembly references.
- A released drawing whose model has moved on is the most common audit finding;
  release them together.

## Verify
- [ ] Every released item has exactly one part number, one current revision, one state.
- [ ] A changed part's where-used list was checked and interchangeability recorded.
- [ ] Released files are read-only and cannot be overwritten in place.
- [ ] CAD BOM count equals PDM BOM count; reference geometry is excluded.
- [ ] The supplier package files all carry the same revision.
