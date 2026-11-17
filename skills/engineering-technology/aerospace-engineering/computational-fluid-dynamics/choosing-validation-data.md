---
id: engineering-technology.aerospace-engineering.computational-fluid-dynamics.choosing-validation-data
name: choosing-validation-data
category: engineering-technology
field: aerospace-engineering
product: computational-fluid-dynamics
tags: [cfd, verification-validation, cfd-uncertainty, validation-data, validation-experiments, unit-problems, benchmark-cases, nasa-crm]
level: practitioner
status: draft
description: "Select aerospace CFD validation data: documented conditions, stated uncertainty, relevance to the target flow, and the hierarchy from unit problems to full configurations."
sources:
  - "AIAA G-077, Guide for the Verification and Validation of CFD Simulations"
  - "Oberkampf and Roy, Verification and Validation in Scientific Computing"
  - "NASA Langley validation case descriptions"
licence: Apache-2.0
version: 2
updated: 2026-11-17
aliases: []
---

# Choosing validation data

**Goal:** data that can actually test the model for your application.

## Criteria
1. **Relevance:** same flow physics (Mach, Reynolds, separation, transition).
2. **Documentation:** geometry, test conditions, tunnel corrections, flow quality (turbulence intensity), model deflections, and measurement uncertainty are available.
3. **Independence:** data not used to tune the model.
4. **Repeatability:** repeated runs or two facilities.

## Hierarchy
Unit problems (flat plate, backward-facing step, airfoil) test model components; benchmark cases (NACA 0012, DLR-F6 and NASA Common Research Model wing-body used by the AIAA Drag Prediction Workshops) test combined physics; the full configuration tests integration. Use the lower levels to explain mismatch at higher levels.

## Practice
- Use published workshop data for the NASA CRM and similar standards for configuration validation; read the workshop's grid guidelines.
- Record tunnel interference, support interference and aeroelastic deformation corrections applied to the data and to the CFD (match the shape under load).

## Gotchas
- Data from unrelated Reynolds number or with unknown trip positions can mislead.
- Aeroelastic deformation unaccounted for gives apparent model error.

## Verify
- [ ] Each validation case lists conditions, data source, uncertainty and the relevance argument.
