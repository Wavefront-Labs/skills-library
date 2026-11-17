---
id: creative-arts.animation.production-design.script-asset-breakdown
name: script-asset-breakdown
category: creative-arts
field: animation
product: production-design
tags: [production-design, world-design-language, asset-breakdown, script-breakdown, asset-list, scheduling]
level: practitioner
status: draft
description: "Break a script or boards into a design asset list: sets, set variants, props, costumes, vehicles and FX, with reuse counts, priority and design-build effort."
sources:
  - https://animationguild.org/
  - https://help.autodesk.com/view/SGSUB/ENU/
  - https://en.wikipedia.org/wiki/Script_breakdown
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Asset breakdown from script

Goal: a complete list of everything that must be designed and built, sized for the schedule.

## 1. Read and tag
- Go scene by scene through the script (then again with boards): tag every **set**, **set variant**
  (night, damaged, decorated), **character costume/variant**, **prop** that is handled or featured,
  **vehicle**, **creature**, **FX** and **in-world graphic**.
- Note the scene numbers each item appears in.

## 2. Build the list
| Column | Meaning |
|---|---|
| Asset ID | stable name (`set_kitchen_A`, `prop_lantern_hero`) |
| Type | set / variant / prop / costume / vehicle / FX / graphic |
| Scenes | where it appears; count of shots if boards exist |
| Hero level | hero (close-ups, handled), mid, background |
| Dependencies | what must be designed first (set before its dressing) |
| Effort | S/M/L for design and for build |
| Reuse | existing library asset or variant of one |

## 3. Prioritise
- Design order follows story priority and build lead time: hero sets and hero props first.
- Collapse: can two locations be one set with redressing? Can a background prop be a library asset?

## 4. Keep it synced
- Reissue when the script or boards change; diff against the previous breakdown and flag new or cut items.
- Feed the list into the tracker so design tasks exist before artists are assigned.

## Verify
- [ ] Every scene read for sets, props, costumes, FX, graphics.
- [ ] Hero level and effort assigned.
- [ ] List synced with the latest script/board version.

Related: `creative-arts.animation.pipeline.asset-management`,
`creative-arts.animation.pipeline.production-tracking`,
`creative-arts.animation.production-design.hero-vs-background-props`.
