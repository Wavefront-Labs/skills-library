---
id: agriculture-environment.conservation-land-stewardship.wildlife-monitoring.camera-trap-survey-design-and-data
name: camera-trap-survey-design-and-data
category: agriculture-environment
field: conservation-land-stewardship
product: wildlife-monitoring
tags: [wildlife-monitoring, wildlife-survey, camera-trap, camera-trapping, trail-camera, survey-design, occupancy, detection-probability, independent-detections, lure, bait-station, transect, spotlighting, call-survey, acoustic-monitoring, audiomoth, birdnet, sign-survey, scats, tracks, timelapse, camtrap-dp, wildlife-insights, species-records, data-management]
level: practitioner
status: draft
description: "Design a wildlife survey around a management question: camera-trap layout and settings, call and sign surveys, independent-detection rules, tagging and storing data for trends."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Camera-trap survey design and data handling

**Goal:** data that can answer "is it there?", "is it changing?" or "did our
management work?" — not a hard drive of unsorted photos. Decide the question first,
because it sets the design.

## 1. Question → design
| Question | Design |
|---|---|
| What species are here? (inventory) | Many sites, varied habitats, lures OK, effort not standardised strictly |
| Where does species X occur / is occupancy changing? | **Occupancy** design: many independent sites, repeated surveys, same method each season |
| Did fox baiting / fencing change activity? | **Before-after-control-impact (BACI)**: treatment and control sites, surveyed before and after |
| How many individuals? | Only for individually marked animals (spots/stripes) — capture-recapture; specialist |

Keep **the same method, season, effort and equipment** across years, or your
"trend" is a method change.

## 2. Camera traps
**Site layout**
- Occupancy: a grid or stratified random points, spaced so sites are roughly
  independent for the target (often hundreds of metres to a few km apart, depending on
  home range). 20–60+ sites is common for reasonable precision; fewer sites = wide error.
- Deployment: commonly 3–6 weeks per site; long enough to detect, short enough that
  occupancy doesn't change during the survey.

**Setting a camera**
- Height and angle to the target: small mammals ~30–50 cm, foxes/cats ~50–70 cm,
  deer/large animals higher; aim slightly down so the detection zone covers 2–5 m.
- Face south in the southern hemisphere / north in the northern to avoid sun-triggered
  false fires; clear vegetation that will blow in the zone (but minimally).
- Settings (typical starting point): PIR sensitivity high for small animals, 3–5 photo
  burst or short video, trigger interval/quiet period 0–30 s, time and date set and
  checked, infrared (no-glow if theft or animal-wariness is a concern).
- **Walk test** each camera after setting: walk past at target height and check it fires.
- Lures: standardise (same lure, same distance, refreshed on the same schedule) or don't
  use them. Lures change detection and can't be dropped halfway through a programme.
- Label each camera and SD card with site ID; photograph the setup and a card showing
  site ID and date at the start.

## 3. Other methods
- **Call surveys:** passive acoustic recorders (e.g. AudioMoth) scheduled for dusk/dawn
  or bat hours; process with classifiers (BirdNET, bat call software) then **verify a
  sample manually** — automated IDs have false positives.
- **Spotlighting transects:** fixed routes, fixed speed (e.g. walking ~1 km/h or
  vehicle ~10 km/h), same moon phase/weather limits, two observers.
- **Sign surveys:** scats, tracks, diggings on sand pads or fixed plots; good for
  presence; ID confidence varies — record uncertainty.
- Bird counts: fixed-radius point counts, same time after sunrise, fixed duration.

## 4. Processing camera data
1. Download into a fixed folder structure: `survey/<year>/<site>/<deployment>/`. Never
   rename original images; keep a read-only master copy.
2. Remove blanks (AI filters such as MegaDetector-based tools speed this up — check
   a sample of the "blanks").
3. Tag species, count, and confidence. Use Timelapse, Wildlife Insights, Camelot or
   similar; export in a standard format (Camtrap DP is an emerging standard).
4. Define **independent detections** — commonly the same species at the same camera
   ≥ 30 min apart counts as a new event. State the rule in every report.
5. Build a site × survey-occasion detection history for occupancy analysis
   (e.g. R `unmarked` package) — or hand it to someone who does.

## 5. Records and ethics
- Submit records to the regional biodiversity database/atlas; **obscure locations of
  sensitive species** (rare, poached, nesting raptors) in public outputs.
- Images of people: delete or blur per privacy law and landowner agreement.
- Permits may be needed for lures, trapping or working with threatened species.

## Gotchas
- Wrong date/time on a camera ruins activity data — check on deployment and retrieval.
- Batteries die in cold; lithium AA last longer.
- Changing camera models mid-programme changes detection rates; overlap old and new.

## Verify
- [ ] Management question written; design matches it.
- [ ] Every camera walk-tested, labelled, time-set and photographed at deployment.
- [ ] Independent-detection rule stated and applied consistently.
- [ ] Raw images archived unchanged; tagged data exported in a standard format.
- [ ] Sensitive locations obscured in shared outputs.
