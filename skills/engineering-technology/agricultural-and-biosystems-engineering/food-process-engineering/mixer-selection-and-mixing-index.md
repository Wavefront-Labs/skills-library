---
id: engineering-technology.agricultural-and-biosystems-engineering.food-process-engineering.mixer-selection-and-mixing-index
name: mixer-selection-and-mixing-index
category: engineering-technology
field: agricultural-and-biosystems-engineering
product: food-process-engineering
tags: [agricultural-and-biosystems-engineering, food-process-engineering, mixing-index, mixer-selection, lacey-index, ribbon-blender, blend-uniformity, coefficient-of-variation, power-number]
level: advanced
status: draft
description: "Select a mixer and prove mixing: powder and liquid mixers, Lacey mixing index, CV from samples, mixing time, power number and sampling pitfalls."
sources:
  - "Toledo, Fundamentals of Food Process Engineering"
  - "Singh & Heldman, Introduction to Food Engineering"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Mixer selection and mixing index

**Goal:** a mixer and mixing time that give a blend or dispersion within the uniformity specification.

## Choose
- Powders and dry blends: ribbon and paddle blenders, V or double-cone tumble blenders, nauta (screw) mixers. Free-flowing, similar-size powders tumble easily; cohesive or segregating powders need positive mixing and careful handling after the mix.
- Doughs and pastes: spiral, planetary and sigma-blade mixers.
- Liquids: impellers in baffled tanks (propeller, turbine, anchor for viscous); in-line static or high-shear mixers.
- Match the mixer to the segregation risk and the batch size (fill level matters: tumble mixers are filled 50-60 percent usually).

## Mixing index
- For a two-component blend, take n samples and compute the variance s^2 of the key component. The completely unmixed variance s0^2 = p(1-p) (p is the overall proportion) and the random mix variance sr^2 = p(1-p)/N (N the number of particles per sample).
- Lacey index M = (s0^2 - s^2) / (s0^2 - sr^2), going from 0 (unmixed) to 1 (random). Coefficient of variation (CV) of sample concentrations is the common spec measure (for example a target CV in the range required by the product or regulation, such as for premixes with micro-ingredients).
- Sample size matters: the samples should be the size of one use (such as a scoop or dose); use a thief carefully, since sampling errors can exceed the mixing variation.

## Mixing time
Plot CV versus time, choose the time where it plateaus; over-mixing can cause segregation or heating. Liquid mixing time from the dimensionless number Nt (agitator speed x time), power from the power number Np = P / (rho x N^3 x D^5) in turbulent flow.

## Verify
- [ ] At least 10 samples per time point for the CV.
- [ ] Discharge and conveying checked for segregation.
- Unconfirmed: CV spec for your product; set by the formulation requirements.
