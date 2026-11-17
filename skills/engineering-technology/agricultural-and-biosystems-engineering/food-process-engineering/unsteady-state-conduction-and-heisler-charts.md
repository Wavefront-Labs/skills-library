---
id: engineering-technology.agricultural-and-biosystems-engineering.food-process-engineering.unsteady-state-conduction-and-heisler-charts
name: unsteady-state-conduction-and-heisler-charts
category: engineering-technology
field: agricultural-and-biosystems-engineering
product: food-process-engineering
tags: [agricultural-and-biosystems-engineering, food-process-engineering, heisler-chart, unsteady-conduction, biot-number, fourier-number, lumped-capacitance, gurney-lurie, food-heating-cooling, food-heat-transfer]
level: advanced
status: verified
description: "Predict heating or cooling of solid foods by transient conduction: Biot and Fourier numbers, lumped capacity limit, Heisler or one-term solutions and finite shapes."
sources:
  - "Singh & Heldman, Introduction to Food Engineering"
  - "Toledo, Fundamentals of Food Process Engineering"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Unsteady-state conduction with Heisler charts

**Goal:** time-temperature histories of solid foods during heating, chilling, freezing precooling or thermal processing.

## Dimensionless groups
- Biot Bi = h x L / k, where L is the characteristic length (half-thickness for a slab, radius for a cylinder or sphere), k the thermal conductivity of the food. Bi below about 0.1 means lumped capacitance is acceptable (for a slab at Bi = 0.1, surface-to-centre ratio is cos lambda1 = 0.952, a 5% internal difference, computed): T changes uniformly, with a time constant rho x cp x V / (h x A).
- Fourier Fo = alpha x t / L^2, alpha = k/(rho x cp).

## Solutions
- For Fo above about 0.2, the first term of the series solution is accurate (computed slab, Bi = 1: lambda1 = 0.8603, C1 = 1.1191; centre error vs the full series 1.5% at Fo = 0.2, 4.7% at 0.1, 7.9% at 0.05): (T - Tinf)/(Ti - Tinf) = C1 x exp(-lambda1^2 x Fo) at the centre; C1 and lambda1 depend on Bi and geometry (slab, infinite cylinder, sphere), tabulated in heat transfer texts and plotted on Heisler (Gurney-Lurie) charts.
- Off-centre and mean temperatures use position and average-temperature charts.
- Finite cylinders and bricks (cans, blocks) use the product of the 1-D solutions for each direction.

## Practice
- Use effective h from measurements, not assumed; in air chilling h depends on velocity.
- Use temperature-dependent properties in numerical models (`freezing-time-estimation-plank-equation` for phase change).
- For canned foods in retorts, use measured heat penetration (`heat-penetration-testing-and-fh-j-parameters`) rather than theory, because convection inside cans complicates conduction.

## Verify
- [ ] Bi and Fo ranges checked against the validity limits.
- [ ] Predicted versus thermocouple-measured centre temperatures.
- Unconfirmed: constants C1 and lambda1; use the tables.
