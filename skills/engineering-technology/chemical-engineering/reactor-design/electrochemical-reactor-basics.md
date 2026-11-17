---
id: engineering-technology.chemical-engineering.reactor-design.electrochemical-reactor-basics
name: electrochemical-reactor-basics
category: engineering-technology
field: chemical-engineering
product: reactor-design
tags: [chemical-engineering, reactor-design, rx-special-reactors, electrochemical-reactor-basics, electrochemical-reactor, faraday-law, current-efficiency]
level: practitioner
status: draft
description: "Apply Faraday law and cell voltage balances to design an electrochemical reactor: current, area, efficiency and energy use."
sources:
  - "Fogler Elements of Chemical Reaction Engineering, Levenspiel Chemical Reaction Engineering, Froment Bischoff and De Wilde Chemical Reactor Analysis and Design"
  - "https://www.aiche.org"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Electrochemical reactor basics

**Goal:** Apply Faraday law and cell voltage balances to design an electrochemical reactor: current, area, efficiency and energy use.

## Steps
1. Faraday law: moles reacted = I t / (n F) times the current efficiency; F is about 96,485 C/mol.
2. Required current I = n F (production rate in mol/s) / current efficiency; electrode area = I / current density.
3. Cell voltage = equilibrium voltage + overpotentials + ohmic drop (I R); energy per unit product = n F V / efficiency.
4. Choose the current density as a trade-off between capital (area) and energy (voltage).
5. Check mass-transfer limits (limiting current) and gas evolution effects on resistance.

## Gotchas
- Safety: hydrogen and chlorine evolution need ventilation and electrical area classification.
- Membranes and electrodes have life limits.

## Verify
- [ ] Current multiplied by time agrees with the product amount at the stated efficiency.
- [ ] Operating current density is below the limiting value.
