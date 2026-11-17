---
id: natural-sciences.botanical-fungal-identification.inaturalist.making-research-grade-observations
name: making-research-grade-observations
category: natural-sciences
field: botanical-fungal-identification
product: inaturalist
tags: [inaturalist, botanical-fungal-identification, citizen-science, research-grade, observation-quality, computer-vision, cv-suggestions, seek, identification, community-id, data-quality-assessment, projects, bioblitz, city-nature-challenge, geoprivacy, obscured-location, captive-cultivated, gbif, identifying-for-others, plant-id, fungi-id, app]
level: intro
status: docs-checked
description: "Post iNaturalist observations that reach Research Grade: one organism each, diagnostic photos, accurate place and date, critical use of computer-vision suggestions, ID etiquette."
sources: [https://help.inaturalist.org/en/support/solutions/articles/151000169936-what-is-the-data-quality-assessment-and-how-do-observations-qualify-to-become-research-grade-, https://help.inaturalist.org/en/support/solutions/articles/151000169938-what-is-geoprivacy-what-does-it-mean-for-an-observation-to-be-obscured-]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Making Research Grade observations in iNaturalist

**Goal:** observations that the community can identify to species, that reach
**Research Grade**, and so flow into datasets such as GBIF and local recording schemes.

## 1. What Research Grade requires
An observation must first be **Verifiable**: an accurate date, accurate coordinates,
and photos or sounds, and not a captive or cultivated organism or a human. Verifiable
observations are labelled "Needs ID" until they reach Research Grade or are voted Casual.
Research Grade needs more than two-thirds of identifiers agreeing on a taxon at species
level or lower. It can also be reached at genus or any rank below family when the
community agrees on that ID and votes that it is as good as it can be. Observations
that fail the Verifiable conditions, or that the community votes down (for example an
inaccurate date, or an organism that is not wild), become Casual.

## 2. One organism, one observation
- Each observation is **one individual of one species** (or one colony for fungi
  and lichens). Don't combine a flower and the bee on it — make two observations
  using the same photo, ID-ing each separately.
- Multiple photos of the same individual go in one observation.

## 3. Photos that can be identified
- Shoot the features keys use: for plants, flower (front and side), leaves
  (both surfaces), stem, fruit, whole plant; for fungi, cap top, gills/pores,
  stem base, and habitat/substrate; for lichens, a close-up with scale.
- Several photos beat one; include something for scale.
- Focus on the organism, not the background; use the phone's macro mode or a clip-on lens.
- See also natural-sciences.botanical-fungal-identification.specimen-pressing-recording.pressing-plants-and-submitting-biological-records
  for diagnostic photography.

## 4. Location and date accuracy
- Let the app take GPS from the photo or device; check the pin and **accuracy circle**.
  When uploading later from a camera, correct the time zone and pin.
- **Geoprivacy:** the default is open. "Obscured" shows the public a random point in a
  larger cell instead of the true location. "Private" shares no geographic information
  publicly; the help page says to use it sparingly because the community then cannot
  easily identify the observation. Taxon geoprivacy can obscure observations of some
  threatened taxa automatically. Obscuring is not foolproof: photos, descriptions and
  nearby open observations can reveal the location.
- Mark garden plants, street trees, pets and zoo animals as **captive/cultivated**.
  This is not a failure — it keeps wild distribution data clean.

## 5. Using computer-vision suggestions critically
- Suggestions come from a model trained on others' observations. They are
  **hypotheses**.
- Prefer a suggestion at **genus** when the top suggestions are several species in
  one genus; this is often the most honest choice.
- Check the suggestion's taxon page: range map, similar species, and identification
  notes, and ask whether the species is plausible at your place and date.
- Common errors: garden cultivars, look-alike species pairs, and groups needing
  microscopy (many fungi, mosses, small insects).

## 6. Identifying for others and etiquette
- Add IDs only when you can explain them; add a comment naming the feature you used,
  especially when disagreeing.
- If your ID disagrees with the current one, be ready to support it with evidence.
- Don't "agree" just because a respected identifier did, unless you can see it too.
- Thank identifiers; reply to questions; withdraw your ID if persuaded otherwise.

## 7. Projects
Join local projects (for example a bioblitz) to get help from regional experts.

## Verify
- [ ] Each observation is one organism, with multiple diagnostic photos.
- [ ] Date, time zone and location (with accuracy) are correct.
- [ ] Captive/cultivated set for planted or kept organisms.
- [ ] Your ID is no finer than you can defend; disagreements explained.
- [ ] Sensitive locations obscured, not falsified.

## Checked
2026-11-01. Confirmed in the iNaturalist Help pages "What is the Data Quality Assessment
(DQA) and how do observations qualify to become Research Grade?" and "What is geoprivacy?":
Verifiable conditions, Needs ID, Casual, the more-than-two-thirds rule, the genus-level
case, geoprivacy open/obscured/private and automatic taxon obscuring. Removed: the
"at least two agreeing" rule (not stated on the help page), the "seen nearby" filter
wording, and the description of collection and traditional projects. Practice advice
(photo angles, etiquette) is judgement, not a factual claim.
Method: documentation only; no commands were run.
