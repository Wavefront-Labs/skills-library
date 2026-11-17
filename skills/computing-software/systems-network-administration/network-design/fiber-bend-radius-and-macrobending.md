---
id: computing-software.systems-network-administration.network-design.fiber-bend-radius-and-macrobending
name: fiber-bend-radius-and-macrobending
category: computing-software
field: systems-network-administration
product: network-design
tags: [network-design, troubleshooting-physical, bend-radius, macrobending, microbending, fiber-handling, bend-insensitive-fiber]
level: practitioner
status: docs-checked
description: "Prevent and find fibre loss from bends: minimum bend radius rules, macro vs microbending, wavelength-dependent symptoms on OTDR, and bend-insensitive fibre."
sources:
  - https://www.itu.int/rec/T-REC-G.657
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Fibre bend radius and macrobending

## Rules of thumb
- Respect the cable manufacturer's minimum bend radius, which is larger under pulling tension than at
  rest; do not rely on a generic multiple.
- Bend-insensitive single-mode fibre is specified in ITU-T G.657; take the minimum radius from the
  patch cord datasheet.
- Velcro, not tight cable ties (microbends); no kinks at panel entries or behind doors.

## Macro vs microbending
- **Macrobending**: visible tight bend; light escapes the core.
- **Microbending**: tiny deformations from crushing, tight ties, temperature on poorly installed cable.

## Symptoms and diagnosis
- Loss that is higher at the longer test wavelength than at the shorter one is the signature of
  bending (longer wavelengths are more bend-sensitive). Connector/splice problems are roughly
  wavelength-independent.
- OTDR at two wavelengths: a non-reflective event with larger loss at the longer wavelength = bend;
  reflective event = connector or break.
- Visual fault locator (visible red light) shows a glow at tight bends on jacketed patch cords
  (works for short distances).
- Rx power on the optic drops or fluctuates when cables are moved.

## Fix
Re-route with proper radius guides, replace crushed sections, use bend-insensitive patch cords in
dense panels; re-test with OTDR/power meter.

## Verify
- [ ] Insertion loss within budget at both test wavelengths after rework; no non-reflective events with wavelength-dependent loss.

## Checked

2026-10-28: The ITU-T G.657 page returned only the recommendation list (it names bend-insensitive fibre categories but gives no radii). Removed the 10x/20x diameter rule, the 30/10/7.5/5 mm radii per G.657 category, the 1310/1550/1625 nm wavelength figures and the 650 nm VFL figure, none of which a fetched page confirmed.
Method: documentation only; no commands were run.
