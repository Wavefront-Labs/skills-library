---
id: creative-arts.design-for-form-and-experience.figma.aliasing-variables-in-figma
name: aliasing-variables-in-figma
category: creative-arts
field: design-for-form-and-experience
product: figma
tags: [variable-aliasing, figma-alias-variables, alias-variables, variable-references, figma-variables, token-tiers-in-figma]
level: practitioner
status: draft
description: "Alias Figma variables so semantic variables point at primitives: create an alias, per-mode aliasing, avoiding cycles, and finding or detaching aliases."
sources:
  - "Figma Help Center (help.figma.com)"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Aliasing variables

An alias is a variable whose value is another variable. It implements token tiers (see `...design-systems.tokens-tiers-primitive-semantic-component`): semantic variables alias primitives so changing the primitive updates everything.

## Create an alias
1. In the variables panel, select the value cell of a variable in a given mode.
2. Choose the variable to reference from the picker (colour variables for colour values, number for number, and so on); the cell shows the referenced name.
3. Do this **per mode:** `color/bg/surface` in Light aliases `neutral/0` and in Dark aliases `neutral/900`.
4. Alias across collections as needed (a semantic collection referencing a primitives collection).

## Rules
- Types must match: a colour alias points to a colour variable.
- **Avoid cycles;** Figma stops circular references.
- Only alias downwards: component or semantic to primitive (aliases of aliases are allowed and follow the chain).
- If a library variable is aliased across files, the referenced collection must be accessible through the library.

## Maintain
- Rename freely: aliases update, but code names derived from them may change (see `...design-systems.building-a-token-sync-pipeline`).
- To flatten to a literal, use detach or paste a raw value in the cell (check the exact control in your version).
- Deleting a variable that is aliased prompts about dependents; replace them first.

## Verify
- [ ] No semantic variable holds a raw value that should alias a primitive.
- [ ] Changing a primitive updates all dependent aliases in every mode.
- [ ] No alias chain is deeper than your team can follow.
