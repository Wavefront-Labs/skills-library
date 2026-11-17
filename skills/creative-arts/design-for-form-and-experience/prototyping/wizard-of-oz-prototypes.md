---
id: creative-arts.design-for-form-and-experience.prototyping.wizard-of-oz-prototypes
name: wizard-of-oz-prototypes
category: creative-arts
field: design-for-form-and-experience
product: prototyping
tags: [wizard-of-oz-prototype, wizard-of-oz, woz, simulated-ai, human-in-the-loop-prototype, voice-prototype, conversational-prototype]
level: practitioner
status: draft
description: "Run Wizard of Oz prototypes: a person secretly performs the system's intelligence so you can test AI, voice or complex behaviour before building it."
sources:
  - "J. F. Kelley, An iterative design methodology for user-friendly natural language office information applications (ACM TOIS, 1984)"
  - "Nielsen Norman Group - Wizard of Oz (nngroup.com)"
  - "Google People + AI Guidebook - Wizard of Oz testing (pair.withgoogle.com/guidebook)"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Wizard of Oz prototypes

**Goal:** test user reactions to a capability (voice assistant, recommendations, chatbot, gesture recognition) by simulating it with a hidden human, before it exists.

## When to use
The behaviour is expensive to build (ML, NLU, hardware) and your risks are about **what users say, expect and accept**, not technical feasibility.

## Setup
1. **Define the capability** and its **rules** the wizard must follow (what the system can and cannot do, response style, latency, error rate). Write them as a wizard script and decision table so responses stay consistent.
2. **Build the front end** that looks real (chat UI, voice device shell, Figma/ProtoPie prototype) and a hidden **wizard console**: a chat window, canned responses, a way to trigger prototype screens or audio (Google Sheets, Slack, a Node server, a second device, Keynote).
3. **Latency:** match realistic response time (a few seconds), not instant, so expectations are not set wrongly.
4. **Include controlled errors** (for example 10-20 percent mis-understandings) to see recovery behaviour.

## Run
- Participant interacts with the "system"; the wizard sits out of view (another room, or behind a screen), listens or reads via video link, responds.
- Facilitator observes, probes expectations and trust, and logs failure moments and wording users use (feeds NLU training data and sample dialogs: `creative-arts.design-for-form-and-experience.interaction-design.writing-sample-dialogs-and-conversation-flows`).
- **Debrief and disclosure:** reveal that a human operated the system at the end (ethical practice, with consent in the briefing in general terms).

## Analyse
Success rate of tasks, vocabulary, turn counts, error recovery, perceived intelligence and trust; compare to the planned machine capability; decide which cases the real system must handle.

## Gotchas
- Wizards drift toward being smarter than the real system; follow the script.
- Train wizards and rehearse; two wizards for voice (one listening, one controlling).

## Verify
- [ ] System rules and error behaviour are scripted.
- [ ] Wizard console and latency realistic; participants debriefed.
- [ ] Findings translated into requirements and data.
