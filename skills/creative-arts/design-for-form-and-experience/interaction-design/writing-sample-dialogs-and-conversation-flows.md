---
id: creative-arts.design-for-form-and-experience.interaction-design.writing-sample-dialogs-and-conversation-flows
name: writing-sample-dialogs-and-conversation-flows
category: creative-arts
field: design-for-form-and-experience
product: interaction-design
tags: [sample-dialogs, conversation-flow, conversational-design, voice-ui, chatbot-design, dialog-flow, vui-design]
level: practitioner
status: draft
description: "Design conversations: write sample dialogs first, read them aloud, then map flows with intents, slots, confirmations and fallbacks before building in a platform."
sources:
  - "Cathy Pearl, Designing Voice User Interfaces (O'Reilly, 2016)"
  - "Google Conversation Design (developers.google.com/assistant/conversation-design/welcome)"
  - "Erika Hall, Conversational Design (A Book Apart, 2018)"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Sample dialogs and conversation flows

**Goal:** a conversation that works for the task, sounds natural, and handles real-world messiness.

## Process
1. **Define the use case:** user, context (hands-free? busy?), tasks the bot owns, and what it will not do. Choose voice, text or both.
2. **Write sample dialogs** (scripts) for the **happy path** first as two-column dialogue (User / System), then variations: multiple ways to ask, partial information, corrections, interruptions, errors. Aim for 10-20 dialogs per major task.
3. **Read them aloud** (or table-read with a partner); fix anything stilted, too long or repetitive. Voice responses should be short (about 1-2 sentences, under about 10 seconds).
4. **Extract the structure:** intents (what the user wants), entities/slots (details needed: date, size), required vs optional slots, and prompts to fill them. Ask for several slots at once only when users commonly provide them together.
5. **Map the flow** in a diagram: states, transitions, **confirmation strategy** (explicit for high-cost actions, implicit for low-risk: "Okay, a large pizza. What toppings?"), and **fallbacks** (no-match, no-input, errors).
6. **Add context handling:** follow-up questions, pronouns ("make it two"), and reset.
7. **Prototype** with Wizard of Oz or a tool (Voiceflow, Dialogflow CX, Botmock-type tools) and test with real users.

## Principles
Cooperative principle (Grice): be brief, relevant, truthful, clear; give the user control (cancel, repeat, human handoff); signal what the bot can do early (capabilities in the welcome).

## Verify
- [ ] Happy and unhappy dialogs written and read aloud.
- [ ] Slots, confirmations and fallbacks mapped.
- [ ] Tested with real users before build.
