---
id: engineering-technology.biomedical-engineering.biomaterials.nitinol-heat-treatment
name: nitinol-heat-treatment
category: engineering-technology
field: biomedical-engineering
product: biomaterials
tags: [nitinol-heat-treatment, shape-setting, nitinol-aging, transformation-temperature, nitinol-processing]
level: advanced
status: draft
description: "Heat treat nitinol: shape setting temperatures and times, ageing effects on Af, solution treatment, oxide control, fixtures and verification by DSC or bend and free recovery."
sources: ["ASTM F2063 Wrought nickel-titanium shape memory alloys for medical devices (confirm edition)", "ASTM F2004 Transformation temperature by DSC and ASTM F2082 Bend and free recovery (confirm editions)", "https://www.astm.org"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Nitinol heat treatment

**Goal:** set the shape and transformation temperatures so the device behaves superelastically at body temperature.

## Principles
- Transformation temperatures (notably the austenite finish, Af; see austenite-finish-temperature) depend on nickel content and thermal history. A small change of nickel content moves them by many degrees.
- **Shape setting:** the device is held in a fixture in its final shape and heated in a furnace or salt bath, typically in the range of roughly 450 to 550 degrees Celsius for minutes, then rapidly quenched. Time and temperature determine the final Af and the plateau stresses.
- **Ageing:** nickel-rich precipitates form and change the matrix nickel content; longer or hotter treatment tends to raise Af in nickel-rich material, so the process must be tuned and held within limits.
- **Solution treatment and cold work:** higher temperature anneals cold work; cold work followed by shape setting controls mechanical properties.
- **Oxide:** heating in air makes a thick titanium oxide layer (heat tint) that is removed by chemical etching, electropolish and passivation (see nickel-release and passivation-astm-f86) because it harms corrosion and fatigue.

## Control and verification
1. Fixture design for repeatable geometry; furnace uniformity surveys; documented time at temperature and quench method.
2. Verify Af on each lot by differential scanning calorimetry (ASTM F2004) or bend and free recovery (ASTM F2082) on finished devices.
3. Mechanical verification: tensile loading and unloading plateaus, and fatigue (see nitinol-fatigue).
4. Process validation per IQ OQ PQ for the heat treatment step.

## Verify
- [ ] Af within specification on every lot.
- [ ] Furnace calibration and thermocouple records current.
- [ ] Oxide removed and surface verified.

> Practice guidance, not regulatory or clinical advice. Confirm current standard editions and rules for your jurisdiction, and defer to qualified regulatory, clinical and engineering judgement.
