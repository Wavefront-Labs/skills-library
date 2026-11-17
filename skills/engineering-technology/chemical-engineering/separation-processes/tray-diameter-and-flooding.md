---
id: engineering-technology.chemical-engineering.separation-processes.tray-diameter-and-flooding
name: tray-diameter-and-flooding
category: engineering-technology
field: chemical-engineering
product: separation-processes
tags: [chemical-engineering, separation-processes, sep-column-hydraulics, tray-diameter-and-flooding, tray-column, flooding, column-diameter, souders-brown, fair-correlation, downcomer, tray-spacing, sieve-tray]
level: practitioner
status: verified
description: "Size tray column diameter from a flooding correlation (Fair type): capacity factor, surface tension and design fraction of flood, downcomer area and tray spacing choices."
sources:
  - "Seader Henley and Roper Separation Process Principles, Perry Chemical Engineers Handbook separations sections, Kister Distillation Design, Treybal Mass-Transfer Operations, McCabe Smith and Harriott Unit Operations"
  - "https://www.aiche.org"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Tray column diameter and flooding

**Goal:** a column diameter that runs at a safe fraction of flood across the whole range.

## Method (as in Sinnott/Towler, after Fair)
1. Flooding vapour velocity: u_f = C_F ((sigma/0.02)^0.2) sqrt((rho_L - rho_V)/rho_V), with sigma in N/m and C_F read from the flooding correlation as a function of the flow parameter F_LV = (L_w/V_w) sqrt(rho_V/rho_L) and tray spacing (plate spacing 0.3 to 0.6 m typical (gated: unconfirmed, source is paywalled or blocked)). The correlation is a graph or fitted equation; use a tested implementation.
2. Design velocity: u = 0.8 to 0.85 u_f for normal systems (gated: unconfirmed, source is paywalled or blocked) (lower for foaming).
3. Net area A_n = V/(rho_V u) (volumetric flow over u).
4. Downcomer area fraction: start at about 10 to 12% of the total area (gated: unconfirmed, source is paywalled or blocked) (for the liquid load; check downcomer velocity and residence time). Column area = A_n/(1 - A_d/A_c).
5. Diameter D = sqrt(4 A_c/pi); round up to standard sizes.
6. Check at top and bottom of each section; use the worst case; vary diameter between sections if loads differ by more than about 20% (gated: unconfirmed, source is paywalled or blocked).

## Checks after diameter
Weeping (minimum vapour velocity at turndown), entrainment, downcomer backup, pressure drop (about 0.007 to 0.01 bar per tray typical for sieve trays (gated: unconfirmed, source is paywalled or blocked)), tray liquid gradient.

## Gotchas
- Foaming systems need a derating factor (for example 0.75 or lower (gated: unconfirmed, source is paywalled or blocked)).
- High-pressure operation reduces density difference and capacity.
- Turndown: sieve trays are limited to about 2:1 to 3:1 (gated: unconfirmed, source is paywalled or blocked); valve trays go further.

## Verify
- [ ] Flooding fraction below 85% at maximum rate for each section.
- [ ] Weeping check passes at the minimum rate.
