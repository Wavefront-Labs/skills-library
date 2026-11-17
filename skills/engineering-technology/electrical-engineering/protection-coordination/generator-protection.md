---
id: engineering-technology.electrical-engineering.protection-coordination.generator-protection
name: generator-protection
category: engineering-technology
field: electrical-engineering
product: protection-coordination
tags: [24, 32, 40, 64g, electrical-engineering, generator-protection, ieee-c37-102, loss-of-field, protection-coordination, reverse-power-and-overexcitation, stator-ground-fault-protection]
level: advanced
status: draft
description: "Select and set generator protection functions: loss of field, reverse power, overexcitation, stator ground fault and differential."
sources:
  - "https://standards.ieee.org/"
licence: Apache-2.0
version: 2
updated: 2026-11-17
aliases: []
---

# Generator protection

Core functions (ANSI numbers in common use; the IEEE C37.102 guide covers them):
- **87G** differential for stator phase faults.
- **40** loss of field: impedance element (offset mho) or reactive power; typical settings reach about `Xd'/2` offset and `Xd` diameter, from manufacturer data.
- **32** reverse power (anti-motoring): protects turbine; pickup set below the motoring power of the prime mover with a time delay of seconds.
- **24** volts-per-hertz: overexcitation limit close to 1.05 to 1.1 pu with inverse-time curve matched to manufacturer.
- **64G / 59N / 27TN** stator ground: 95 percent stator via neutral overvoltage plus 100 percent stator scheme using third-harmonic undervoltage or low-frequency injection.
- **46** negative sequence (I2^2 t); **51V** voltage-restrained backup overcurrent; **81** frequency; **78** out-of-step.
- Include the grounding method (high-resistance usually) when selecting the ground scheme.

**Verify:** relay settings reviewed against the generator capability curve and excitation limiter coordination.

**Scope note:** Professional guidance only: design, selection, settings and sign-off belong to a qualified engineer or licensed electrician working to the code and standard editions adopted in the project jurisdiction. Standard clause numbers, limits and table values cited from memory are unconfirmed against the paywalled text (gated: unconfirmed, source is paywalled or blocked); worked arithmetic was recomputed.
