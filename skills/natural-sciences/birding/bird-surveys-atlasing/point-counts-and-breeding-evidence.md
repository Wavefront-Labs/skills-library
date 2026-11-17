---
id: natural-sciences.birding.bird-surveys-atlasing.point-counts-and-breeding-evidence
name: point-counts-and-breeding-evidence
category: natural-sciences
field: birding
product: bird-surveys-atlasing
tags: [bird-surveys-atlasing, birding, bird-survey, point-count, transect, breeding-bird-atlas, atlasing, breeding-codes, breeding-evidence, christmas-bird-count, breeding-bird-survey, bbs, citizen-science, detectability, double-counting, survey-protocol]
level: practitioner
status: docs-checked
description: "Run volunteer bird surveys properly: follow the scheme protocol, count points without double counting, use the atlas's own breeding-evidence codes, and record effort."
sources: ["https://www.pwrc.usgs.gov/bbs/about/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Point counts and breeding evidence

**Goal:** collect bird counts that can be compared across sites and years, and atlas
records that correctly reflect breeding status. Comparability matters more than finding
the most birds.

## 1. The core principle: follow the protocol exactly
Survey data are only useful if everyone does the same thing. The scheme's written protocol
beats your judgement. If you deviate (started late, skipped a point, weather turned),
record the deviation; do not quietly "improve" the data.

Worked example, the North American Breeding Bird Survey (USGS): routes of about 24.5 miles,
stops ideally 0.5 miles apart, 3 minutes at each stop, every bird seen or heard within a
0.25-mile radius recorded, starting half an hour before local sunrise and taking about 5
hours. Other schemes use different durations and distances: read yours.

## 2. Timed point counts
- Count for the scheme's fixed period and record each individual once, with the distance
  band and detection type (seen, heard, flyover) the scheme asks for.
- Record flyovers as the scheme directs.
- Sketch a map with a mark per bird to avoid double counting singing birds that move.
- Run counts only at the times and in the weather the protocol allows.

## 3. Line transects
Walk the fixed route at a steady pace and record birds by the scheme's distance bands.
Do not stop to chase an unknown bird; note it and move on.

## 4. Breeding evidence codes (atlasing)
Atlases rank evidence in tiers (possible, probable, confirmed), but the code letters,
definitions and safe dates are set by each atlas. Use the atlas's own code list and
date windows, not memory. Migrants singing before the atlas's safe dates are not breeding
evidence. Upgrade a record as better evidence arrives.

## 5. Ethics during atlas work
Never disturb vegetation to search for nests; confirmation by watching adults from a
distance is enough. Specially protected species may need a licence to approach nests.
Report sensitive species through the confidential channel the atlas provides.

## 6. Christmas counts and migration watches
Record effort (hours, distance, party size): effort is what makes counts comparable. For
watch points, keep hourly tallies, direction of travel and weather.

## Verify
- [ ] Count duration, start time, weather and effort recorded for every count.
- [ ] Each individual counted once; flyovers handled as the scheme directs.
- [ ] Breeding codes taken from the atlas's own definitions and dates.
- [ ] No nests disturbed to obtain confirmation.
- [ ] Deviations from protocol written down.

## Checked
2026-11-01. Confirmed on the USGS Breeding Bird Survey "about" page: route length, stop
spacing, 3-minute counts, 0.25-mile radius, start half an hour before sunrise, about 5 hours.
Removed (not stated on a page read): distance-band values, standard wait time, specific
breeding code lists and thresholds, CBC and migration-watch counting conventions. The
eBird atlas code pages were blocked to the fetcher, so no code definitions are kept.
Method: documentation only; no commands were run.
