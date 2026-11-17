---
id: creative-arts.design-for-form-and-experience.interaction-design.designing-a-bot-persona
name: designing-a-bot-persona
category: creative-arts
field: design-for-form-and-experience
product: interaction-design
tags: [bot-persona, chatbot-persona, conversational-persona, voice-persona, brand-voice, conversational-design, character-design]
level: practitioner
status: draft
description: "Design a bot persona: base it on the brand and user needs, define traits and vocabulary, disclose that it is automated, and apply it consistently without pretending to be human."
sources:
  - "Google Conversation Design - Persona (developers.google.com/assistant/conversation-design/create-a-persona)"
  - "Cathy Pearl, Designing Voice User Interfaces (2016), persona chapter"
  - "Erika Hall, Conversational Design (A Book Apart, 2018)"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Bot persona

**Goal:** a consistent, trustworthy character for an assistant, matched to brand and context.

## Steps
1. **Context first:** who talks to it, when, in what mood (a bank bot for a stressed customer differs from a game guide). The persona serves the task.
2. **Pick 3-5 traits** from the brand voice (`creative-arts.design-for-form-and-experience.ux-design.defining-voice-and-tone-guidelines`): e.g. calm, direct, warm, lightly witty. For each, give a "does / does not" example.
3. **Write a short profile:** name (or none), role ("I'm the virtual assistant for ..."), what it is and is not, attitude (competent helper, not a friend), the vocabulary and sentence style, humour limits.
4. **Be honest it is automated:** disclose in the greeting; never claim to be human; some jurisdictions require disclosure.
5. **Scope voice by situation:** apology and error handling are plain; personality shows in greetings and small talk, never in payments, health or legal topics.
6. **Voice only:** choose TTS voice (gender, accent, speed, pitch) deliberately and check with the target audience; avoid stereotypes (do not default to female for assistants without considering bias).
7. **Small talk and out-of-scope:** define 20-50 canned responses for greetings, thanks, jokes, "are you a robot?", and offensive input, consistent with traits.
8. **Test:** table-read dialogs; run perception tests (trust, competence, warmth ratings) with users; refine.

## Consistency
Maintain a response library with an owner and style rules; review new content against the persona; avoid persona drift across channels.

## Verify
- [ ] Traits tied to brand and task with examples.
- [ ] The bot discloses it is automated; no human impersonation.
- [ ] Tone adapts in serious situations; small talk library exists.
