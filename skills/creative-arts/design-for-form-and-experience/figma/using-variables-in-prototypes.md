---
id: creative-arts.design-for-form-and-experience.figma.using-variables-in-prototypes
name: using-variables-in-prototypes
category: creative-arts
field: design-for-form-and-experience
product: figma
tags: [prototype-variables, figma-prototype-variables, variables-in-prototypes, set-variable, conditional-prototypes, prototyping]
level: practitioner
status: draft
description: "Use variables in Figma prototypes: set and read boolean, number and string variables, drive text and visibility, use expressions and conditions, and reset state."
sources:
  - "Figma Help Center (help.figma.com)"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Variables in prototypes

Variables let a prototype hold state, such as a counter, a toggle or an entered name, and react to it. They complement conditional logic (see `...figma.conditional-logic-in-prototypes`).

## Set up
1. Create variables (a boolean `isLoggedIn`, a number `cartCount`, a string `username`) in a collection.
2. **Bind** them: a text layer's content can show a string or number variable; layer visibility can bind to a boolean; properties like fill and size can bind to variables.
3. **Add interactions** with the **Set variable** action (on click, on drag, after delay, when key pressed); set to a value, or compute with simple expressions (add one to a number, toggle a boolean).
4. **Add conditions** (if / else) to navigate or set different values depending on variable state.
5. **Reset** state: set variables back on prototype start or by an explicit reset action; variables hold values during a prototype run.

## Examples
- Cart counter: on add-to-cart, set `cartCount = cartCount + 1`; show it in a badge bound to the variable.
- Toggle: set `isDark = not isDark` and use modes to switch themes in the prototype.
- Form: store input in a string variable and show it in the confirmation.

## Limits
Prototype variables run in prototype mode only, with the supported types and expression set; complex logic needs a coded prototype (see `...prototyping.coded-prototypes`). Check the Help Center for the current expression syntax.

## Verify
- [ ] Each variable has an initial value and a reset path.
- [ ] Every conditional branch is covered when testing.
- [ ] State shown on screen updates immediately.
