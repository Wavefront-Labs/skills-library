---
id: manufacturing-production.electronics-semiconductor-manufacturing.smt-line-operation.smt-changeover-and-first-article-buy-off
name: smt-changeover-and-first-article-buy-off
category: manufacturing-production
field: electronics-semiconductor-manufacturing
product: smt-line-operation
tags: [smt-line-operation, smt, surface-mount, pcba, changeover, first-article, fai, first-article-inspection, stencil, solder-paste, stencil-printer, dek, mpm, ekra, pick-and-place, fuji, panasonic, asm-siplace, yamaha, mycronic, feeder-setup, feeder-verification, barcode-verification, msd, moisture-sensitive, j-std-033, setup-verification, smed, nozzle, polarity, ems, contract-manufacturing]
level: practitioner
status: draft
description: "Change an SMT line over to a new job and buy off the first board: stencil and paste setup, scan-verified feeder loading, MSD checks, placement first-article and release criteria."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# SMT changeover and first-article buy-off

**Goal:** move a surface-mount line from job A to job B quickly and *without* building
a batch of boards with a wrong part, reversed polarity or bad paste — the three ways a
changeover turns into a scrap or rework pile.

## 1. Before the line stops (external setup)
Do everything that doesn't need the line idle while the last job is still running:
- **Kit check** against the job's setup sheet / BOM-feeder list: every reel present,
  correct manufacturer part number (MPN), enough quantity for the order plus attrition.
- **Pre-load feeders on a spare cart or offline feeder rack** if the line supports
  trolley exchange (Fuji, ASM, Panasonic all have variants). Scan reel + feeder +
  slot as you load — never load "by eye".
- **MSD floor life:** check moisture-sensitive parts (BGAs, QFNs, some LEDs) against
  their MSL label and humidity indicator card. Exposed past floor life → bake per
  J-STD-033 before use. This is the most-skipped check in a rush.
- **Stencil:** pull the correct stencil by ID and revision; inspect apertures under
  light for blockage or damage, check tension if your site measures it.
- Load the placement program and printer program for the new job revision; confirm
  the revision matches the traveller/work order.

## 2. Changeover (internal setup)
1. Clear the line: no boards from job A left in conveyors, buffers or reflow.
2. Swap stencil, supports (tooling pins or magnetic supports placed clear of bottom-side
   components) and squeegees if the job needs a different length.
3. Set conveyor width for the new panel; check it runs a bare board end to end.
4. Paste: correct alloy/type for the job (SAC305 vs leaded vs low-temp is not
   interchangeable). Note paste **open time** and pot life — record when the jar was
   opened and how long it has been on the stencil.
5. Exchange feeder carts, then run the machine's **feeder verification** (scan-based
   setup check). Do not override a mismatch to "save time"; resolve it.
6. Check nozzles assigned for the new part sizes are clean and present.

## 3. First article — print
- Print one board, inspect paste deposits (SPI if fitted, else magnifier) on the finest
  pitch areas: bridging, insufficient, smearing, offset. Fix print before placing.
- Wipe the stencil underside after any misprint; wash a misprinted bare board fully or
  scrap it — a hand-wiped board carries paste balls into reflow.

## 4. First article — placement and reflow
1. Place one board. Before reflow, if practical, stop and check on the board:
   polarity of diodes/ICs/tantalums, BGA/QFN orientation, value of a sample of passives
   (an LCR meter on loose parts from each reel is a common FAI method).
2. Reflow with the job's profile (see reflow-profile skill under
   reflow-wave-soldering).
3. Run AOI, then compare the board against the BOM/centroid and assembly drawing.
   Many sites use an **FAI tester** (camera + LCR) that checks every placement against
   the BOM; if you don't have one, a two-person manual check is the substitute.
4. Record: job, revision, stencil ID, paste lot, feeder setup verification result,
   inspector, time.

## 5. Release
Release to volume only when FAI passes and is signed off (by QA if your process
requires it). Common gotcha: an **engineering change** mid-run — re-do the FAI for
the changed area, not just a feeder swap.

## Gotchas
- **Splicing reels** mid-run must also be scan-verified; mis-splices cause the same
  wrong-part escapes as bad setups.
- A **substitute (alternate) part** approved on the AVL may differ in height or
  polarity marking — teach the vision/package data, don't just accept the reject.
- Tooling pins under BGAs on the bottom side crack parts; check the support map.
- Nozzle pickup errors after changeover usually mean wrong feeder pitch or tape
  cover not peeling, not a "bad nozzle".

## Verify
- [ ] Setup verification passed with zero overrides; any override is logged and approved.
- [ ] MSD parts within floor life (or baked) and recorded.
- [ ] Stencil and program revisions match the work order.
- [ ] First board print inspected before placing; FAI checked polarity and values.
- [ ] FAI record signed before volume release.

*Draft: feeder-cart and verification steps vary by machine vendor and MES; confirm
against your line's work instructions. Uncertain on site-specific QA sign-off rules.*
