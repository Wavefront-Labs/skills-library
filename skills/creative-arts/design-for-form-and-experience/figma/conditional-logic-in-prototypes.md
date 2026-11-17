---
id: creative-arts.design-for-form-and-experience.figma.conditional-logic-in-prototypes
name: conditional-logic-in-prototypes
category: creative-arts
field: design-for-form-and-experience
product: figma
tags: [conditional-logic, figma-variables-prototype, prototype-expressions, if-else, set-variable, stateful-prototype, figma-prototyping, figma]
level: practitioner
status: draft
description: "Add conditional logic to Figma prototypes: set variables, if/else branches, expressions, counters, form validation and mode switching for realistic behaviour."
sources:
  - "Figma Help Center - Conditional actions (help.figma.com/hc/en-us/articles/15253220891543)"
  - "Figma Help Center - Use variables in prototypes (help.figma.com/hc/en-us/articles/15343107263511)"
  - "Figma Config 2023 - Advanced prototyping with variables (config.figma.com)"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Conditional logic in Figma prototypes

## Pieces
1. **Variables:** create **boolean, number, string** (and colour) variables in a collection; bind to text content, visibility, fills.
2. **Set variable** action: assign a value or expression (`count + 1`, `isLoggedIn = true`, `email = "ana@example.com"`).
3. **Conditional** action: **if / else if / else** blocks that evaluate expressions, each containing actions (Navigate to, Set variable, Change to, Open overlay, Back).
4. **Expressions:** comparison (`==`, `!=`, `<`, `>`, `<=`, `>=`), logical (`&&`, `||`, `!`), arithmetic (`+ - * /`), string concatenation (`"Total " + total`), grouping with parentheses.

## Common patterns
- **Counter / stepper:** `qty` number variable; plus button sets `qty = qty + 1`; minus button conditional `if qty > 1` then `qty = qty - 1`; bind text to `qty`.
- **Toggle with state:** boolean `isOn`; click sets `isOn = !isOn`; component variant bound to the variable via Change to.
- **Login gate:** `if isLoggedIn == true` navigate to account else to login frame.
- **Form validation:** text input prototype (via **input** plugins or text input component) sets `email`; `if email == "demo@example.com"` navigate to success else show error visibility variable.
- **Cart total:** `total = total + price` on add-to-cart; display with a text bound to a string variable.
- **Mode switching:** **Set variable mode** to toggle Light/Dark across the prototype.
- **Progress:** variable step increments through a wizard; bar width via variable-bound component.

## Workflow
Plan a **state table** first (variable values to screens); build minimal; name variables clearly (`cart/qty`, `ui/isMenuOpen`); reset state on flow start (**On click** of Start, or set variables in a **While loading** trigger after delay on the first frame).

## Gotchas
- Prototype logic is for testing, not production; do not recreate backend behaviour.
- Variables persist during a session; **Restart** the prototype before each test.
- Complexity grows quickly; for deep logic use ProtoPie or code (`creative-arts.design-for-form-and-experience.prototyping.protopie-sensor-and-variable-prototypes`).

## Verify
- [ ] State table matches branches; all paths reachable.
- [ ] Variables reset on restart.
- [ ] Tested through every condition branch.
