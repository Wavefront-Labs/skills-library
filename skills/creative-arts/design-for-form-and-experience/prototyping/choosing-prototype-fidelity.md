---
id: creative-arts.design-for-form-and-experience.prototyping.choosing-prototype-fidelity
name: choosing-prototype-fidelity
category: creative-arts
field: design-for-form-and-experience
product: prototyping
tags: [fidelity-selection, prototype-fidelity, low-fidelity, high-fidelity, prototype-planning, prototyping-strategy, research-question-fit]
level: practitioner
status: draft
description: "Choose prototype fidelity for the question: match low, mid or high fidelity in visuals, content, interaction and data to what you need to learn, with a decision table."
sources:
  - "Houde and Hill, What do Prototypes Prototype? (Handbook of Human-Computer Interaction, 1997)"
  - "Nielsen Norman Group - UX Prototypes: Low Fidelity vs. High Fidelity (nngroup.com/articles/ux-prototype-hi-lo-fidelity)"
  - "Rudd, Stern and Isensee, Low vs. High-Fidelity Prototyping Debate (interactions, 1996)"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Choosing prototype fidelity

**Principle (Houde and Hill):** a prototype answers a question about **role** (what it does for people), **look and feel** (sensory), or **implementation** (how it works). Pick fidelity per dimension for the question, not one overall level.

## Dimensions of fidelity (NN/g)
Visual polish, content realism, interactivity, data and functionality, platform/physical form.

## Decision table
| Question to answer | Fidelity needed |
|---|---|
| Is the concept valuable? Which idea? | Storyboards, paper sketches, video prototype, landing page smoke test |
| Does the structure and navigation make sense? | Low-fi wireframes, paper, click-through of grey boxes (`creative-arts.design-for-form-and-experience.prototyping.paper-prototype-testing`) |
| Does the flow work end to end? | Mid-fi clickable prototype, real labels, limited visuals |
| Does the interface wording and layout communicate? | Real content with mid visual fidelity |
| Are visual hierarchy, brand, motion, perception right? | High visual fidelity (static or animated) |
| Are interactions and timing usable (gestures, drag, voice)? | High interactivity (ProtoPie, code, Wizard of Oz) |
| Will it perform with real data? | Coded, working back end |
| Is physical form comfortable? | Foam, 3D print, bucks (`creative-arts.design-for-form-and-experience.concept-design.carving-high-density-foam-form-models`) |

## Heuristics
1. **Start low, rise with certainty:** early questions need speed; later questions need realism. Low-fi finds the same major usability problems as hi-fi when the issues are structural.
2. **Fidelity can mislead:** polished prototypes attract feedback on colours and fonts, and make teams reluctant to change; sketchy ones invite structural critique.
3. **Match the audience:** stakeholders sometimes need hi-fi to see the point; users usually need only enough realism for the task.
4. **Cost the options:** hours to build vs learning value; prefer the cheapest prototype that can disconfirm your riskiest assumption.
5. **Mix** (hybrid): hi-fi where the question lives (a payment screen), low-fi elsewhere.

## Verify
- [ ] The question is written first; fidelity per dimension chosen from it.
- [ ] Riskiest assumption can be falsified with this prototype.
- [ ] Participants briefed on what is real and fake.
