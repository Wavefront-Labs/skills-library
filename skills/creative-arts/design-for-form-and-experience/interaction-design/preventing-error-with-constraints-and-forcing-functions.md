---
id: creative-arts.design-for-form-and-experience.interaction-design.preventing-error-with-constraints-and-forcing-functions
name: preventing-error-with-constraints-and-forcing-functions
category: creative-arts
field: design-for-form-and-experience
product: interaction-design
tags: [forcing-functions, constraints, slips-and-mistakes, human-error, error-prevention, design-of-everyday-things, norman-principles, interaction-design]
level: practitioner
status: draft
description: "Design out human error: distinguish slips from mistakes, apply constraints, defaults, confirmations and forcing functions, and support undo and recovery."
sources:
  - "Don Norman, The Design of Everyday Things, revised ed. (Basic Books, 2013), chapter 5 on human error and design"
  - "James Reason, Human Error (Cambridge University Press, 1990)"
  - "Nielsen Norman Group - Error Prevention (nngroup.com/articles/slips)"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Constraints, forcing functions and error design

**Goal:** make the wrong action hard or impossible and the right one easy, and make remaining errors cheap to fix.

## Classify the error first
- **Slips** (right goal, wrong execution): action-based (hit the adjacent button) or memory-lapse (forgot a step). Fix with design: spacing, constraints, checklists.
- **Mistakes** (wrong goal or plan): rule-based, knowledge-based or memory-based. Fix with better information, feedback and a clearer conceptual model.
- Treat "user error" as a design symptom; ask what in the system caused the action.

## Tactics, from strongest to weakest
1. **Eliminate the error:** remove the option (disable invalid dates, calendar picker instead of free text).
2. **Forcing functions:**
   - **Interlock** (must do A before B: seat belt before ignition, confirm backup before destructive migration).
   - **Lock-in** (keep an operation running: warn before closing an unsaved editor).
   - **Lockout** (block entry: child-safe caps).
3. **Constraints:** physical, logical (only valid transitions), semantic (a postcode matches a country), cultural (conventions). Constrain input type and range.
4. **Defaults and previews:** safe default; show the result before commit (diff, preview).
5. **Confirmation:** reserved for rare, high-cost actions; frequent confirmations are dismissed by reflex. Prefer **undo** (see `creative-arts.design-for-form-and-experience.interaction-design.choosing-undo-over-confirmation`).
6. **Detect and recover:** inline validation, clear messages, easy rollback, an audit trail.

## Gotchas
- Forcing functions can annoy; make them proportionate to the harm and give a justified override path where safe.
- Warnings alone do not stop slips.

## Verify
- [ ] Each known error is classed as slip or mistake with a matching fix.
- [ ] High-cost actions are reversible or gated by a forcing function.
