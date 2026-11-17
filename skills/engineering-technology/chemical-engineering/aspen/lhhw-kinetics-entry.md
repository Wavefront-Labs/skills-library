---
id: engineering-technology.chemical-engineering.aspen.lhhw-kinetics-entry
name: lhhw-kinetics-entry
category: engineering-technology
field: chemical-engineering
product: aspen
tags: [chemical-engineering, aspen, aspen-reactor-blocks, lhhw-kinetics-entry, lhhw, langmuir-hinshelwood, power-law-kinetics, kinetic-factor, driving-force, adsorption-term, aspen-plus]
level: advanced
status: gated
description: "Enter LHHW and power-law kinetics in Aspen Plus: kinetic factor, driving force and adsorption terms, units, reference temperature and a hand check of one rate value."
sources:
  - "Aspen Plus and Aspen HYSYS user guides and help (AspenTech), Seider et al. Product and Process Design Principles"
  - "https://www.aiche.org"
  - "AspenTech Aspen Plus certification study guide AT-05198 (learning objectives, aspentech.com)"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Entering LHHW and power-law kinetics

**Goal:** enter a catalytic or non-elementary rate law so the simulator's rate equals your hand-calculated rate at one test condition.

## Form of the LHHW rate in Aspen Plus
rate = (kinetic factor) x (driving force expression) / (adsorption expression)

- **Kinetic factor:** k = k0 x (T/T0)^n x exp(-E/R x (1/T - 1/T0)) (with T0 optional); E in energy per mole.
- **Driving force:** difference of two terms, forward and reverse, each a product of concentrations to powers; the reverse term uses an equilibrium constant expression.
- **Adsorption:** a sum of terms, each K_i x product of concentration powers, raised to an exponent.
(The Aspen term layout and the ln K coefficient form below are unconfirmed (gated: unconfirmed, source is paywalled or blocked); a numeric check showed the stated kinetic factor equals k0 exactly at T = T0.) Enter each term by listing coefficients (ln K style fits: A + B/T + C ln T + D T) on the corresponding sheets.

## Power-law
rate = k(T) x product C_i^a_i with the same temperature form; set the concentration basis (mole concentration, partial pressure, mole fraction) and reacting phase.

## Procedure
1. Write the rate law in your units on a spreadsheet and compute the rate at one T and composition.
2. Enter the same law in the simulator; run a one-point test (a very small RCSTR volume gives the rate directly from conversion).
3. Match the units for k0 and E (SI or user-chosen set) and the basis of the rate (per catalyst mass, per volume).
4. Compare simulator and spreadsheet; they should agree within a fraction of a percent.

## Gotchas
- Many published LHHW fits have rates per kg catalyst; convert with the bed density.
- Reference-temperature form changes how k0 is interpreted; use one form consistently.
- The reverse reaction is best expressed through thermodynamic K to guarantee equilibrium consistency.

## Verify
- [ ] Spreadsheet and simulator rate agree at two different T values.
- [ ] Equilibrium conversion obtained with kinetics matches the thermodynamic equilibrium at long residence time.
