---
id: engineering-technology.agricultural-and-biosystems-engineering.food-process-engineering.sanitary-pump-selection-and-viscosity-effects
name: sanitary-pump-selection-and-viscosity-effects
category: engineering-technology
field: agricultural-and-biosystems-engineering
product: food-process-engineering
tags: [agricultural-and-biosystems-engineering, food-process-engineering, sanitary-pumps, centrifugal-pump, lobe-pump, progressive-cavity-pump, npsh, pump-shear, hygienic-pump, food-rheology]
level: practitioner
status: draft
description: "Select a sanitary pump for a food: centrifugal, lobe, progressive cavity or piston, viscosity and shear effects, NPSH, speed, seal type and CIP flow."
sources:
  - "Toledo, Fundamentals of Food Process Engineering"
  - "Codex Alimentarius, General Principles of Food Hygiene and HACCP (https://www.codexalimentarius.org)"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Sanitary pump selection

**Goal:** a pump that moves the product with the required flow and head, without damaging it, and that can be cleaned in place.

## Types
- Centrifugal: low viscosity, high flow, simple, cheap; viscosity above about a few hundred mPa.s lowers efficiency and head; high shear for sensitive emulsions.
- Positive displacement: lobe (rotary), progressive cavity, piston and diaphragm; flow is nearly proportional to speed, suited to viscous and particulate products. Lobe pumps are common in dairy and beverages; progressive cavity for pastes and particles; piston pumps for high pressure and homogeniser feed.
- Particulate foods need gentle pumps (large clearance lobes, progressive cavity at low speed, or air-driven diaphragm).

## Selection
1. Flow and pressure from the line calculation (`non-newtonian-pipe-flow-pressure-drop`).
2. Viscosity at product temperature and shear rate; derate centrifugal curves for viscosity (use the maker's correction).
3. NPSH available versus required; PD pumps have different rules; check for cavitation and air entrainment.
4. Speed limits for shear-sensitive products.
5. Seals: single or double mechanical seals with barrier fluid for aseptic or hazardous sites; food-grade lubricants; elastomer compatibility.
6. Relief protection on a PD pump (it will overpressure the line if the outlet is blocked).
7. CIP: ensure the CIP flow velocity is attainable (centrifugal CIP supply pump or bypass for PD pump).

## Hygiene
Hygienic design standards (3-A, EHEDG) set requirements for finish, drainability and seals; the maker's certification helps with audits.

## Verify
- [ ] Measured flow and pressure at the real viscosity compared to the selection.
- [ ] Relief valve tested.
- Unconfirmed: viscosity limits by pump design.
