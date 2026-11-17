---
id: creative-arts.design-for-form-and-experience.interaction-design.writing-voice-prompts-and-handling-no-match
name: writing-voice-prompts-and-handling-no-match
category: creative-arts
field: design-for-form-and-experience
product: interaction-design
tags: [voice-prompts, no-match-handling, no-input-handling, reprompts, error-recovery-conversational, ivr, voice-ui]
level: practitioner
status: draft
description: "Write voice prompts that elicit clean answers, and handle no-match and no-input with escalating reprompts, rephrasing, options and graceful handoff."
sources:
  - "Cathy Pearl, Designing Voice User Interfaces (O'Reilly, 2016)"
  - "Google Conversation Design - Error handling and Prompts (developers.google.com/assistant/conversation-design/errors)"
  - "Amazon Alexa Design Guide - Handling errors (developer.amazon.com/en-US/docs/alexa/alexa-design/error-handling.html)"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Voice prompts and no-match / no-input handling

## Writing prompts
- **Short and front-loaded:** the question comes last: "Okay, your order is a large cheese pizza. What size drink?"; avoid long menus (voice is linear and temporary memory is small): at most 3 options spoken.
- **Open vs directed:** open prompts ("How can I help?") for experts or first turns with good NLU; **directed prompts** with examples ("You can say 'track my order' or 'talk to someone'") when recognition is weak.
- Use natural, consistent wording; the user's vocabulary; contractions; vary acknowledgements ("Got it", "Okay") modestly.
- Avoid prompts that mix instructions and questions in the same sentence; avoid "Say or press" overload.
- Use SSML for pacing: pauses (`<break time="300ms"/>`), emphasis, and `say-as` for dates and numbers.

## No-input (silence or timeout)
Reprompt shorter and more helpful than the first prompt; **escalate**: 1) repeat or rephrase briefly, 2) give examples, 3) offer alternative (touch tone, app, agent). Timeout about 5-8 s after prompt; for smart speakers end after 2 reprompts.

## No-match (misrecognised or out of scope)
- Do not blame ("I didn't understand you"); take responsibility: "Sorry, I missed that."
- Escalate: rephrase the question with examples; narrow options; offer help; after 2-3 failures **hand off** to a person or other channel with context transferred.
- Confirm uncertain recognitions ("Did you say Boston?") based on confidence thresholds; log all no-match utterances weekly and add intents or synonyms.
- Maintain a global **escape** commands set: help, repeat, start over, cancel, agent.

## Metrics
Containment rate, task completion, no-match rate per state, repeat rate, transfer reasons.

## Verify
- [ ] Prompts are short with the question last; example prompts for weak recognition.
- [ ] Three-level escalation for no-input and no-match with handoff.
- [ ] Unrecognised utterances logged and reviewed.
