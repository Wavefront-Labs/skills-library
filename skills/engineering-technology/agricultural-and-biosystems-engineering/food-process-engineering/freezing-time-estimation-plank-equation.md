---
id: engineering-technology.agricultural-and-biosystems-engineering.food-process-engineering.freezing-time-estimation-plank-equation
name: freezing-time-estimation-plank-equation
category: engineering-technology
field: agricultural-and-biosystems-engineering
product: food-process-engineering
tags: [agricultural-and-biosystems-engineering, food-process-engineering, plank-equation, food-refrigeration, cold-chain, freezing-time, iqf, blast-freezer, shape-factor]
level: practitioner
status: verified
description: "Estimate food freezing time with Plank's equation for slab, cylinder and sphere shapes, understand its assumptions, and compare freezer types and corrections."
sources:
  - "Singh & Heldman, Introduction to Food Engineering"
  - "Toledo, Fundamentals of Food Process Engineering"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Freezing time with Plank's equation

**Goal:** a first estimate of time to freeze a product from the initial freezing point to the centre temperature.

## Equation
`t_F = (rho L / (T_f - T_a)) x (P a / h + R a^2 / k_f)`

- rho density of the frozen product, L latent heat (kJ/kg, from the water fraction frozen), T_f initial freezing point, T_a freezing medium temperature, h surface heat transfer coefficient, k_f thermal conductivity of frozen product, a characteristic dimension.
- Shape constants: infinite slab (a = thickness) P = 1/2, R = 1/8; infinite cylinder (a = diameter) P = 1/4, R = 1/16; sphere (a = diameter) P = 1/6, R = 1/24.
- The constants follow from the frozen-shell energy balance: slab half-thickness x gives t = (rho L/dT)(x/h + x^2/2k), i.e. P = 1/2, R = 1/8 with a = 2x; the cylinder and sphere forms give 1/4, 1/16 and 1/6, 1/24 with a = diameter.
- Assumptions: freezing at a single temperature, constant properties, product initially at T_f (no precooling). It underestimates time for real foods because freezing occurs over a range and sensible heat above T_f is neglected; use modifications (Pham, Cleland-Earle) for better accuracy.

## Use
1. Estimate h for the freezer: air-blast 15-40 W/m2 K typical depending on velocity (gated: unconfirmed, source is paywalled or blocked); plate freezers have higher effective h through contact; liquid immersion higher still (check maker data).
2. Compute t_F for the thickest piece; add precooling time.
3. Compare freezer options: air-blast tunnel, spiral, IQF fluidised bed, plate, cryogenic.

## Gotchas
- Packaging and air gaps lower h dramatically.
- Fast freezing keeps ice crystals small and reduces drip loss on thaw for many products.

## Verify
- [ ] A thermocouple at the thermal centre of a test product confirms the time within a reasonable tolerance.
