---
id: defence-public-safety.search-and-rescue.search-management.probability-based-search-planning-and-segmentation
name: probability-based-search-planning-and-segmentation
category: defence-public-safety
field: search-and-rescue
product: search-management
tags: [search-and-rescue, search-management, search-planning, managing-the-lost-person-incident, mlpi, poa, pod, pos, probability-of-area, probability-of-detection, probability-of-success, mattson-consensus, segmentation, sweep-width, coverage, effective-sweep-width, rest-of-world, bayesian-update, sartopo, caltopo, ics, operational-period, iap, debriefing, suspension]
level: advanced
status: docs-checked
description: "Search planning with POA, POD and POS: segmenting the area, consensus probabilities, coverage and sweep width, shifting POA after each period, and running the operational cycle."
sources: ["https://www.dco.uscg.mil/Portals/9/CG-5R/nsarc/Land_SAR_Addendum/Published_Land%20SAR%20Addendum%20(1118111)%20-%20Bookmark.pdf", "https://www.dco.uscg.mil/Portals/9/CG-5R/nsarc/LandSearchMethodsReview.pdf"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Probability-based search planning and segmentation

**Goal:** put searchers where they most raise the chance of finding the subject,
update that picture as areas are searched, and document decisions so that suspension
(if it comes) is defensible. Reference for search managers and planners; the method below follows the US National SAR Supplement land addendum and search theory.

## 1. Define the search area
- Start from the IPP and lost-person behaviour distance rings, then adjust for
  terrain barriers, travel aids (trails, roads, drainages) and investigation.
- Draw a **theoretical** search area (how far could they have gone?) and a
  **statistical** one (where are they likely?). Use the smaller practical area but
  keep the **Rest of World (ROW)** — the probability the subject is outside it.

## 2. Segment
Segments should be searchable by one team in one operational period, bounded by **features searchers can find on the ground** (trails, streams,
ridges, fences) rather than arbitrary grid lines. Number them; record area.

## 3. Assign POA (probability of area)
Use a **consensus** method: several experienced people independently
assign percentages to each segment plus ROW, then average. This avoids one
planner's bias dominating. Total = 100%.

## 4. POD and coverage
- **Effective sweep width (W)** is the detection "width" a searcher covers for a given
  subject/clue type, terrain and vegetation; it is estimated from detection experiments
  or field tables, or approximated in the field with an average maximum detection range
  method.  Sweep width values vary widely, so treat field approximations as rough.
- **Coverage (C)** = W × length of track searched ÷ segment area.
- **POD ≈ 1 − e^(−C)** (exponential detection function). Coverage 1.0 gives about 63% POD; coverage 2 gives about 86.5%.

## 5. POS and updating
- **POS = POA × POD** — the chance that searching the segment found the subject (if
  they were there).
- After a segment is searched without a find, its **POA falls**:
  new POA = old POA × (1 − POD), and all segments (including ROW) are re-normalised —
  probability shifts to unsearched areas. This is the Bayesian update that makes
  multi-period searches rational.
- Allocate the next period's teams to maximise total POS gained per resource, not
  simply to the highest-POA segment.

## 6. The operational cycle
Brief (assignments, maps, subject info, safety, comms) → deploy → search → **debrief**
(track logs, clues, areas not covered, hazards, team's assessment) → update maps and
probabilities → plan the next period. Run it under ICS with a written Incident
Action Plan for each period.

## 7. Suspension
Decisions to scale down are made with the responsible agency, based on cumulative POD,
survivability, weather and resources, and are documented. Families must be informed
with care; investigation often continues.

## Gotchas
- Ignoring ROW makes the search area feel "done" when it may not contain the subject.
- Re-searching the same high-POA segment repeatedly with low-POD methods.
- Debriefs skipped when teams are tired — lost information costs a period.

## Verify
- [ ] Every segment has a ground-identifiable boundary, an area and a POA.
- [ ] POA assigned by consensus and includes ROW.
- [ ] POD recorded per segment and resource; POA updated after each period.
- [ ] Assignments chosen for POS gained, with reasons recorded.
- [ ] Every team debriefed and track logs saved.

## Checked

Checked 2026-10-25. Jurisdiction: United States (National SAR Supplement land addendum); search theory is general. Source versions: US National SAR Committee Land SAR Addendum and its search-theory review (titles confirmed by search; full text not read). Computed by reading: coverage 1.0 gives POD = 1 - e^-1 = 63%, coverage 2.0 gives 86.5%; POS = POA x POD; the posterior POA update (old POA x (1 - POD), then renormalise) is the standard Bayesian step. Removed unconfirmed items: the 4 to 6 hour segment length, the named consensus method, the claim about specific software, the claim that subjective PODs are known to be optimistic, and the drafting note.

Method: documentation only; no commands were run.
