---
id: engineering-technology.agricultural-and-biosystems-engineering.food-process-engineering.ball-formula-method-process-time-calculation
name: ball-formula-method-process-time-calculation
category: engineering-technology
field: agricultural-and-biosystems-engineering
product: food-process-engineering
tags: [agricultural-and-biosystems-engineering, food-process-engineering, formula-method, thermal-processing, canning-process, ball-method, general-method, process-time, stumbo, f0]
level: practitioner
status: verified
description: "Calculate sterilisation process time with the Ball formula method from fh, j, retort temperature, z and target F0, using g-tables or the improved general method for verification."
sources:
  - "Toledo, Fundamentals of Food Process Engineering"
  - "Singh & Heldman, Introduction to Food Engineering"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Formula (Ball) method process-time calculation

**Goal:** the retort time that delivers the target F0 for a specific container and product.

## Method
1. Lethal-rate factor at the retort temperature: `F_i = 10^((121.1 - T_ret)/z)` (minutes at T_ret equivalent to one minute at 121.1 C). Target at retort temperature: `U = F0_target x F_i`.
2. Compute `fh / U`.
3. From Ball or Stumbo tables (or a validated program) find `g` (temperature difference between retort and product at the end of heating) for the value of `fh/U`, z and `jc` (cooling lag).
4. Process time: `B = fh (log(j_ch I_h) - log g)`, where `I_h = T_ret - T_ih`.
5. Ball's convention takes the effective zero time as 58 percent of the come-up time after steam-on, (arithmetic: process time at temperature = B + 0.58 CUT - CUT), so the time from steam-on is `B + 0.58 CUT` and the operator's time counted from when the retort reaches temperature is `B - 0.42 CUT`.
6. Check with the general method: integrate lethal rate from the actual heat penetration data for the proposed time to confirm F0 including cooling contribution.

## When to prefer the general method
Irregular time-temperature curves (broken heating curves, agitated processes) or when cooling is long.

## Gotchas
- Tables for Stumbo vs Ball assume specific conventions; mixing them yields errors.
- Use worst-case initial temperature and worst-case retort temperature (minimum).
- Process authority approval is required for commercial low-acid processes.

## Verify
- [ ] The calculated schedule when integrated on the measured cold-spot data yields F0 at least the target.
