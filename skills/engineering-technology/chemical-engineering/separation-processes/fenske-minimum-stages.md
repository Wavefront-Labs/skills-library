---
id: engineering-technology.chemical-engineering.separation-processes.fenske-minimum-stages
name: fenske-minimum-stages
category: engineering-technology
field: chemical-engineering
product: separation-processes
tags: [chemical-engineering, separation-processes, sep-distillation-shortcuts, fenske-minimum-stages, fenske-equation, minimum-stages, total-reflux, shortcut-distillation, light-key, heavy-key, non-key-distribution, relative-volatility]
level: practitioner
status: verified
description: "Calculate minimum stages at total reflux with the Fenske equation for binary and multicomponent separations, including distribution of non-key components."
sources:
  - "Seader Henley and Roper Separation Process Principles, Perry Chemical Engineers Handbook separations sections, Kister Distillation Design, Treybal Mass-Transfer Operations, McCabe Smith and Harriott Unit Operations"
  - "https://www.aiche.org"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Fenske minimum stages

**Goal:** the theoretical minimum number of stages (at total reflux) for a specified split, the first number in a shortcut design.

## Equation
N_min = ln[ (x_LK/x_HK)_D (x_HK/x_LK)_B ] / ln(alpha_LK,HK)
where the stages include the partial reboiler (N_min counts equilibrium stages including the reboiler) and alpha is the geometric mean of the top and bottom relative volatilities (or evaluate at an average temperature).

## Multicomponent use
1. Choose light key (LK) and heavy key (HK); specify recoveries (for example 99% of LK to the distillate and 99% of HK to the bottoms).
2. Compute N_min from the key recoveries.
3. **Distribution of non-keys**: for each component i, (d_i/b_i) = alpha_i,HK^N_min (d_HK/b_HK), giving the fractions to distillate and bottoms at total reflux.
4. Use the computed distribution as the starting point for the Underwood step (see `engineering-technology.chemical-engineering.separation-processes.underwood-minimum-reflux`).

## Worked example
Benzene/toluene: x_D = 0.99 benzene, x_B = 0.01 benzene, alpha = 2.4. N_min = ln[(0.99/0.01)(0.99/0.01)]/ln 2.4 = ln(9801)/0.8755 = 9.19/0.8755 = 10.5 stages (recomputed: 10.50) including the reboiler.

## Gotchas
- Original paper: Fenske, Ind. Eng. Chem. 24(5):482-485 (1932). A strong variation of alpha through the column makes the geometric mean inaccurate; split into sections.
- Non-key components that are heavier than the heavy key (or lighter than the light key) go almost entirely to one product; the assumption can fail for components near the keys (distributing components).
- Fenske is only valid for total reflux; the actual design uses Gilliland.

## Verify
- [ ] Compare N_min against a rigorous total-reflux simulation within 1 stage (gated: unconfirmed, source is paywalled or blocked).
- [ ] Non-key distribution mass balance closes.
