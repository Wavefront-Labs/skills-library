---
id: computing-software.qa-testing-engineering.exploratory-testing.exploratory-tours
name: exploratory-tours
category: computing-software
field: qa-testing-engineering
product: exploratory-testing
tags: [exploratory-tours, exploratory-testing, whittaker-tours, test-charters, touring-heuristics]
level: practitioner
status: draft
description: "Structure exploratory sessions with Whittaker's tours (guidebook, money, landmark, FedEx, garbage collector, saboteur, back alley) and turn each into a charter."
sources:
  - https://www.oreilly.com/library/view/exploratory-software-testing/9780321684097/
  - https://www.developsense.com/blog/2009/04/of-testing-tours-and-dashboard-checks/
  - https://www.istqb.org/certifications/test-analyst
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Exploratory tours

**Goal:** give exploratory sessions a theme, so different testers cover different ground. From James Whittaker, *Exploratory Software Testing* (tourist metaphor; districts of the application).

## Tours and what they find
| Tour | Do | Finds |
|---|---|---|
| Guidebook | follow the user manual/help literally | docs vs behaviour mismatches |
| Money | the features sales demos and customers pay for | defects with highest business impact |
| Landmark | hop between key features in varied orders | sequencing and state bugs |
| Intellectual | ask the hardest questions: max inputs, most complex config | limits, performance |
| FedEx | follow one piece of data through every place it is stored/shown | data integrity, transformation errors |
| Garbage collector | visit every screen/menu item systematically, shallowly | broken pages, missing strings |
| Bad neighbourhood | revisit areas with many past bugs | defect clusters, regressions |
| Museum | old/legacy features, untouched code paths | regressions in neglected areas |
| Back alley | least used features | untested code |
| All-nighter | keep the app open and active for a long time | leaks, session/timeouts |
| Saboteur | remove resources: network, disk, permissions, dependencies | error handling |
| Antisocial | always enter the opposite/unexpected input | validation |
| Couch potato | do as little as possible: defaults, empty fields | default handling |
| Obsessive-compulsive | repeat the same action many times | duplicates, races |
| Supermodel | look only at the UI surface: layout, rendering | visual defects |

## Turning a tour into a charter
"Explore **order data** with the **FedEx tour** to discover **where totals or addresses change between basket, invoice email and admin export**." Timebox 60-90 min.

## Planning a set
- Assign different tours to different testers for the same release area.
- Rotate tours across releases to fight the pesticide paradox.
- Combine: money tour first in a release, bad-neighbourhood tour after big refactors.

## Gotchas
- Tours are prompts, not scripts; follow interesting findings even if they leave the tour.
- Without notes and debrief, tours leave no evidence.

## Verify
Each session names its tour in the charter, and coverage notes show which areas each tour visited.
