---
id: creative-arts.design-for-form-and-experience.interaction-design.designing-signifiers-and-affordances
name: designing-signifiers-and-affordances
category: creative-arts
field: design-for-form-and-experience
product: interaction-design
tags: [signifier-design, affordances, signifiers, design-of-everyday-things, norman-principles, discoverability, interaction-design]
level: practitioner
status: draft
description: "Make actions discoverable with perceived affordances and signifiers (Norman): show where to act and how, fix false affordances, and test what users think is clickable."
sources:
  - "Don Norman, The Design of Everyday Things, revised and expanded ed. (Basic Books, 2013), chapter 1"
  - "Nielsen Norman Group - Flat UI Elements Attract Fewer Clicks (nngroup.com/articles/flat-ui-less-attention-cta)"
  - "Nielsen Norman Group - Signifiers topic (nngroup.com/articles/affordances-and-signifiers)"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Signifiers and affordances

**Goal:** a user can tell what can be done and where, without instruction.

## Vocabulary (Norman, 2013 edition)
- **Affordance:** the possible relationship between an object and an actor (a handle affords pulling).
- **Signifier:** the perceivable cue that communicates where the action should take place. Signifiers matter more than affordances in screen design because screen elements afford clicking whether or not they look clickable.
- **Anti-affordance** blocks action; **false affordance** looks actionable but is not (underlined non-link text, a card that looks tappable but is not).

## Practice
1. Inventory the actions on a screen; for each name its signifier (button shape, underline, chevron, cursor change, drag handle, placeholder text).
2. Strong signifiers for primary actions: filled shape, label with a verb, contrast of 3:1 against surroundings. Weak flat signifiers lower click rates, as NN/g eye-tracking shows.
3. Use consistent conventions (blue underlined text is a link; a chevron means drill-in; a handle means draggable). See `creative-arts.design-for-form-and-experience.ux-design.heuristic-evaluation-with-nielsens-ten` for the consistency check.
4. State signifiers: hover, focus, pressed and disabled change appearance; disabled controls explain why when possible.
5. Gestures have no visible affordance, so add a signifier (peek of the next card, drag handle, coach mark) and an alternative control.
6. Test: a 5-second click test or first-click test; ask "what would you tap?" and note false affordances.

## Gotchas
- Minimal and flat styles often delete signifiers; keep at least one cue per action.
- Do not rely on hover; touch has none.

## Verify
- [ ] Every action has a visible signifier; nothing non-interactive looks interactive.
- [ ] Gestures have a visible hint and a fallback.
