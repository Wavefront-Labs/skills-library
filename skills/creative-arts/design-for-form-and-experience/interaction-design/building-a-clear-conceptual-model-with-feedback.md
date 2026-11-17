---
id: creative-arts.design-for-form-and-experience.interaction-design.building-a-clear-conceptual-model-with-feedback
name: building-a-clear-conceptual-model-with-feedback
category: creative-arts
field: design-for-form-and-experience
product: interaction-design
tags: [conceptual-model, mental-model, feedback, system-image, design-of-everyday-things, norman-principles, interaction-design]
level: practitioner
status: draft
description: "Give users an accurate conceptual model: align designer, system image and user model, and provide immediate, informative feedback on every action."
sources:
  - "Don Norman, The Design of Everyday Things, revised ed. (Basic Books, 2013), chapter 2 and 3"
  - "Nielsen Norman Group - Mental Models (nngroup.com/articles/mental-models)"
  - "Nielsen Norman Group - Visibility of System Status (nngroup.com/articles/visibility-system-status)"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Conceptual models and feedback

**Goal:** users form a correct mental picture of how the thing works, so they predict outcomes and recover from problems.

## The three models
- **Design model** (what the designer intends), **user's model** (what they believe), **system image** (what the product shows: UI, labels, behaviour, docs). Designers talk to users only through the system image, so mismatches between the user's model and the design model are fixed there.

## Steps
1. **Elicit user models:** ask people to draw or explain how they think the thing works (a file sync, a shared cart); note the metaphors they use.
2. **Choose one simple model** and its metaphor (folders, a shopping cart, a conversation). Name things with the user's vocabulary.
3. **Make state visible:** show what is synced, saved, selected, on or off, and what will happen next.
4. **Give feedback within about 0.1 s** for direct manipulation, with a progress or busy cue when work takes over about 1 s (see Doherty and response-time guidance), and a confirmation when it finishes.
5. **Make feedback informative and proportionate:** say what changed ("Saved to Drafts at 14:02") not just "Success". No feedback is worse than too much; too much trains users to ignore it.
6. **Check the model by prediction test:** show a screen and ask what will happen if they press X; wrong answers expose the gap.

## Gotchas
- Inconsistent behaviour across similar features breaks the model (autosave in one place, manual in another).
- Feedback that arrives without a cause (a random toast) confuses attribution.

## Verify
- [ ] Users' own words appear in labels; one metaphor, used consistently.
- [ ] Every action has visible, informative feedback; system state is visible.
