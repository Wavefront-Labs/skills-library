---
id: creative-arts.design-for-form-and-experience.ux-design.writing-microcopy-and-button-labels
name: writing-microcopy-and-button-labels
category: creative-arts
field: design-for-form-and-experience
product: ux-design
tags: [microcopy, ux-writing, content-design, button-labels, interface-copy, call-to-action]
level: practitioner
status: docs-checked
description: "Write short interface copy and link text: important words first, users' own language, sentence case, tone for the moment, and no reliance on colour or position."
sources:
  - https://www.gov.uk/service-manual/design/writing-for-user-interfaces
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Microcopy and button labels

**Goal:** short interface text that tells users what will happen and what to do next.

## Button and link labels
- **Put the important words first** and drop unnecessary ones: people scan rather than read. GOV.UK: say "Total cost", not "This is the total cost"; say "apply", not "apply now" (unless the choice is apply now or later).
- One idea per sentence; keep copy short and direct.
- Use sentence case. Headings and input labels have no full stop; other copy is full sentences with one.
- **Link text must make its purpose clear on its own** (screen-reader users hear lists of links): "click here" is not accessible link text.
- Do not rely on shape, size, colour or location alone ("click the green button").

## Other microcopy
- **Start with less:** add help text only where user research shows it is needed. If you must explain how the interface works, fix the interface instead.
- **Use the same language as your users**, including for the service name.
- **Tone:** approachable and helpful, not overly familiar. No "please" or thank you by default, no "sorry" in validation errors (say sorry when something serious has gone wrong), and avoid humorous error messages.

## Process
1. Cut every word that does not help the user.
2. Review against the voice guide (`creative-arts.design-for-form-and-experience.ux-design.defining-voice-and-tone-guidelines`).
3. Test your words with users for critical flows.

## Verify
- [ ] Important words come first and nothing is said twice.
- [ ] Link text makes sense out of context.
- [ ] Nothing depends on colour, shape or position alone.

## Checked
2026-11-01. Confirmed against GOV.UK Service Manual, Writing for user interfaces: scanning, start with less, short direct copy and important words first, examples, tone and sorry/please/thank-you guidance, accessible link text, colour and position, sentence case and punctuation, user language. Removed (not stated there): verb-plus-object and dialog-button rules, 25-character and 1-3 word limits, primary/secondary label rules, placeholder advice, glossary and translation expansion figures, read-aloud and first-click steps, the Yifrah, Podmajersky and NN/g sources.
Method: documentation only; no commands were run.
