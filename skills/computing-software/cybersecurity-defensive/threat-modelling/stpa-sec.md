---
id: computing-software.cybersecurity-defensive.threat-modelling.stpa-sec
name: stpa-sec
category: computing-software
field: cybersecurity-defensive
product: threat-modelling
tags: [stpa-sec, stpa, systems-theoretic, control-structure, unsafe-control-actions, cyber-physical]
level: advanced
status: draft
description: "Apply STPA-Sec to cyber-physical or complex systems: define losses and hazards, model the control structure, find unsafe or insecure control actions and loss scenarios."
sources: ["STPA Handbook (Leveson and Thomas, MIT Partnership for Systems Approaches to Safety and Security, 2018)", "https://doi.org/10.1145/2556938"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# STPA-Sec

STPA (System-Theoretic Process Analysis, Nancy Leveson, MIT) treats safety as a control problem. STPA-Sec
(Young and Leveson) applies the same analysis to security: losses happen when **control actions** are
provided, withheld, mistimed or wrongly sustained, whether by failure or by an adversary. It works top-down
from mission losses, which suits vehicles, medical devices, ICS and other systems where component-level
STRIDE misses emergent behaviour.

## Step 1: Define the purpose of the analysis
- **Losses** (L): unacceptable outcomes to stakeholders. L-1 loss of life or injury, L-2 loss of mission,
  L-3 disclosure of patient data.
- **System-level hazards / vulnerabilities** (H): system states that lead to a loss in worst-case conditions.
  H-1 infusion pump delivers incorrect dose [L-1].
- **System-level constraints**: the inverse of each hazard ("pump must not deliver a dose outside the
  prescribed range").

## Step 2: Model the control structure
Hierarchical diagram of controllers (humans, software, PLCs), control actions sent down, and feedback sent up.
Each controller has a **process model** (its beliefs about the controlled process).

## Step 3: Identify unsafe/insecure control actions (UCAs)
For every control action, check four ways it can be hazardous:
1. Not provided when needed.
2. Provided when it causes a hazard.
3. Provided too early, too late or out of order.
4. Stopped too soon or applied too long.
Write each UCA with its context: "Controller sends START_INFUSION when the dose parameter has been altered
[H-1]".

## Step 4: Identify loss scenarios
Why could each UCA occur? Consider: spoofed or tampered feedback, corrupted process model, compromised
controller, injected commands on the control path, delayed or blocked actuation. These are the security
scenarios; derive requirements (authenticated commands, plausibility checks on feedback, interlocks
independent of the network).

## Gotchas
- Keep losses few and stakeholder-level; dozens of losses means you are listing hazards.
- The control structure is the main artefact; get domain engineers to validate it.
- STPA-Sec does not enumerate component vulnerabilities; follow up with STRIDE or ICS-specific methods on the
  components implicated by loss scenarios.

## Verify
Every UCA traces to a hazard and a loss, every loss scenario has a constraint or requirement, and the control
structure was reviewed by the system's engineers.
