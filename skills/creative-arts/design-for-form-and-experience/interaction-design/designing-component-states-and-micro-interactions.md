---
id: creative-arts.design-for-form-and-experience.interaction-design.designing-component-states-and-micro-interactions
name: designing-component-states-and-micro-interactions
category: creative-arts
field: design-for-form-and-experience
product: interaction-design
tags: [interaction-design, ui-design, ixd, component-states, hover, focus, focus-visible, pressed, active, disabled, loading, error-state, success-state, selected, micro-interactions, feedback, affordance, signifiers, motion-design, ui-motion, easing, duration, transitions, prefers-reduced-motion, accessibility, wcag, contrast, touch-targets, keyboard-navigation, figma-variants, design-handoff]
level: practitioner
status: draft
description: "Design every state of an interactive component (default, hover, focus, pressed, disabled, loading, error, success) and its micro-interactions with sensible timing, easing and accessible contrast."
sources:
  - "Saffer, Microinteractions: Designing with Details (O'Reilly)"
  - "W3C, Web Content Accessibility Guidelines (WCAG) 2.2 — focus visible, contrast, target size"
  - "Material Design 3 and Apple Human Interface Guidelines, sections on states and motion"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Designing component states and micro-interactions

**Goal:** an interface feels solid when every control answers the user — it shows it's
clickable, reacts when touched, tells you it's working, and says clearly whether it
worked. That comes from designing **all the states** of each component and the small
animated transitions between them, not just the static default.

> **Status: draft.** State lists and timing ranges reflect common guidance (Material,
> Apple HIG, Saffer's microinteraction model, WCAG 2.2). Numbers are starting points;
> platform conventions win where they differ.

## 1. The state inventory
For each interactive component (button, input, checkbox, toggle, card, tab), design:

| State | What it communicates | Notes |
|---|---|---|
| Default | "I'm here and usable" | must look interactive (affordance) |
| Hover (pointer only) | "you can act on me" | subtle; never the only cue — touch has no hover |
| **Focus** (keyboard) | "this has focus" | visible ring, ≥3:1 contrast against neighbours (WCAG 2.2 focus appearance guidance) |
| Pressed / active | "I felt that" | immediate, within ~100 ms |
| Selected / checked | "this is on/chosen" | don't rely on colour alone — use icon/weight/shape |
| Disabled | "not available now" | explain why nearby if possible; avoid hiding the reason |
| Loading | "working on it" | spinner or skeleton after ~1 s; progress if longer |
| Error | "it didn't work, here's why" | message near the field, in words, with fix |
| Success | "done" | brief confirmation; then return to a stable state |

For inputs also: **empty**, **filled**, **read-only**, **with helper text**, **character count**.

In Figma, build these as **variants** (state property) of one component so engineers see the full set.

## 2. Micro-interaction anatomy (Saffer)
Every micro-interaction has: **trigger** (user tap, or system event), **rules** (what
happens), **feedback** (what the user sees/hears/feels), **loops & modes** (what changes
over time or on repeat). Write those four lines for anything non-trivial — e.g. a "like"
button: trigger = tap; rules = toggle liked, update count optimistically, revert on
failure; feedback = icon fill + small scale bounce + count change; loop = none.

## 3. Motion that helps
- **Duration:** small UI changes ~100–200 ms; larger panels/screens ~200–400 ms. Longer
  feels sluggish; very short reads as a glitch.
- **Easing:** ease-out (fast start, slow end) for things entering; ease-in for things
  leaving; avoid linear for spatial movement.
- **Purpose:** motion should explain — where something came from, what changed, what to
  look at — not decorate.
- **Respect `prefers-reduced-motion`:** provide fades or instant changes instead of
  movement/parallax for users who request it.
- Feedback must not wait for the animation: the pressed state appears immediately.

## 4. Accessibility checks
- **Contrast:** text ≥4.5:1 (normal), ≥3:1 (large text, UI component boundaries, focus indicators).
- **Touch targets:** at least 24×24 CSS px per WCAG 2.2 (AA), with 44×44 pt (Apple) or
  48×48 dp (Material) recommended for comfort.
- **Not colour alone:** errors with icon and text; selected with checkmark.
- **Keyboard:** every action reachable by Tab/Enter/Space/arrow keys, focus order logical.
- **Screen readers:** states exposed (aria-pressed, aria-expanded, aria-invalid) — annotate in handoff.

## Gotchas
- Removing the focus outline "because it's ugly" — redesign it, don't remove it.
- Disabled buttons with no explanation (users don't know what's missing).
- Hover-only reveals that touch users never see.
- Spinners for 200 ms operations — flicker; delay showing loading until it's actually slow.
- Optimistic UI without designing the rollback/error state.

## Verify
- [ ] Each component has all applicable states designed as variants.
- [ ] Focus states visible with ≥3:1 contrast; tab order annotated.
- [ ] Micro-interactions specified as trigger / rules / feedback / loops.
- [ ] Motion durations and easing specified; reduced-motion alternative defined.
- [ ] Touch targets and colour-independence checked.
