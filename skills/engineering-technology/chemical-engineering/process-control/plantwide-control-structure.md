---
id: engineering-technology.chemical-engineering.process-control.plantwide-control-structure
name: plantwide-control-structure
category: engineering-technology
field: chemical-engineering
product: process-control
tags: [chemical-engineering, process-control, pc-multivariable-control, plantwide-control-structure, plantwide-control, luyben, control-structure, degrees-of-freedom, inventory-control, recycle-loop, snowball-effect, production-rate]
level: advanced
status: gated
description: "Design a plantwide control structure with Luyben's nine-step procedure: objectives, degrees of freedom, inventory control, recycle handling and component balances."
sources:
  - "Luyben, W.L., Tyreus, B.D., Luyben, M.L. (1997) Plantwide control design procedure, AIChE Journal 43(12):3161-3174, https://doi.org/10.1002/aic.690431205"
  - "Luyben, Tyreus and Luyben, Plantwide Process Control, McGraw-Hill 1998 (textbook)"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Plantwide control structure design

**Goal:** a consistent plantwide control scheme (inventories, production rate, quality, constraints) before individual loops are tuned.

## Procedure (after Luyben, Tyreus and Luyben, AIChE J. 43(12):3161-3174, 1997; the exact step order and wording is (gated: unconfirmed, source is paywalled or blocked))
1. **Establish control objectives**: safe operation, product rate and quality, environmental limits, economics.
2. **Determine the control degrees of freedom**: number of control valves (and other independent manipulated variables) minus the number of variables that cannot be controlled (for example, valves on level self-regulating).
3. **Establish the energy management system**: handle heat of reaction and keep temperatures bounded (prevent energy accumulation and runaway; control temperature of reactors and place heat integration safeguards, particularly with process-to-process exchange).
4. **Set the production rate**: choose a handle (for example, feed flow to the reactor, a key reactant inlet flow) and the rate of the throughput manipulator.
5. **Control product quality, and handle safety, environmental and operational constraints**: use the available valves; choose the loops that matter most for quality.
6. **Fix a flow in every recycle loop and control inventories** (levels, pressures, with the manipulated variable in the direction of flow or opposite as chosen); a fixed flow in each recycle prevents the "snowball" effect (large recycle flows swinging with small disturbances).
7. **Check component balances**: every component needs a way out (reaction, product, purge); control the amount of each component in recycle loops via make-up or purge.
8. **Control individual unit operations** (columns, reactors, exchangers) using the remaining degrees of freedom.
9. **Optimise economics or improve dynamic controllability** with the remaining degrees of freedom.

## Practice
- Write a control narrative: the scheme, tuning intent, interlocks and alarms.
- Use dynamic simulation (steady-state design first, then dynamic) to test disturbance scenarios (feed rate, composition, loss of a utility).

## Gotchas
- Structures that look fine in steady state may be unstable dynamically with recycles.
- Level controllers in series can create oscillation; use proportional-only for some.

## Verify
- [ ] Degrees of freedom count reconciles with the valve list.
- [ ] Dynamic simulation of a throughput change and a feed composition upset is stable.
