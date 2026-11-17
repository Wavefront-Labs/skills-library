---
id: engineering-technology.agricultural-and-biosystems-engineering.controlled-environment-systems.biosecurity-and-air-handling-for-indoor-farms
name: biosecurity-and-air-handling-for-indoor-farms
category: engineering-technology
field: agricultural-and-biosystems-engineering
product: controlled-environment-systems
tags: [agricultural-and-biosystems-engineering, controlled-environment-systems, biosecurity-airflow, positive-pressure, air-filtration, hepa-filter, airlock, gowning, pest-exclusion, hygiene-zoning, vertical-farming]
level: practitioner
status: draft
description: "Plan biosecurity for indoor farms: positive pressure, filtration grades, airlocks and gowning, pest screens, water and seed hygiene, and monitoring."
sources:
  - "ASHRAE Handbook (Fundamentals and Refrigeration volumes) (https://www.ashrae.org)"
  - "Codex Alimentarius, General Principles of Food Hygiene and HACCP (https://www.codexalimentarius.org)"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Biosecurity and air handling

**Goal:** keep pathogens and pests out of the growing rooms and contain any that get in.

## Layers
1. Site and building: sealed envelope, no gaps at services; screened vents; clean external area without standing water or plant waste.
2. Air: fresh air through filters; the filter class depends on risk (from coarse and medium filters, up to higher efficiency filters such as MERV 13 or HEPA in high-risk or propagation rooms; check the rating standards, ASHRAE 52.2 for MERV and EN 1822 or ISO 29463 for HEPA). Maintain the pressure drop across filters and schedule replacements.
3. Pressure cascade: the growing rooms kept at positive pressure relative to the entry areas and the outside (a differential of the order of 10-15 Pa is common in cleanroom practice), so air leaks outward. The pressure sensors and the alarm are part of the system. Positive pressure also depends on a tight room.
4. People and materials: entry through airlocks with a change of footwear or boot wash, hand wash and clean gowns, with one-way flow from the cleanest (propagation, seeding) to the less clean (harvest, packing). Restrict who may enter and keep visit logs. Tools and carts stay inside their zones (`hygienic-zoning-and-plant-layout`).
5. Water and nutrient: treat incoming water and recirculating solutions (`recirculating-solution-disinfection`); keep clean tanks and covered lines.
6. Seeds and media: certified clean seed; sterile substrate; discard diseased plants in sealed containers and out through a defined route.
7. Pest monitoring: sticky traps and scouting; threshold actions; integrated pest management using biological control if allowed.

## Food safety link
Leafy greens are eaten raw: the hygiene, water and worker health controls should also meet the produce safety rules that apply (for example the US FDA Produce Safety Rule and GAP audit schemes); confirm with your auditor.

## Verify
- [ ] Pressure differentials logged and alarms tested.
- [ ] Air and surface swabs for microbes at a set interval.
- Unconfirmed: local regulatory and audit requirements.
