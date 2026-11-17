---
id: creative-arts.animation.editorial.textless-elements
name: textless-elements
category: creative-arts
field: animation
product: editorial
tags: [textless, texted-inserts, localisation, deliverables, picture-lock, netflix-delivery, titles, graphics]
level: practitioner
status: draft
description: "Deliver textless backgrounds and texted inserts so territories can localise titles, signs and on-screen text in an animated show, per platform delivery specs."
sources:
  - https://partnerhelp.netflixstudios.com/hc/en-us
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Textless elements and texted inserts

**Goal:** every shot that carries text (main titles, credits, signs, phone screens, captions burned into the
picture) also exists without the text, so international versions can replace it.

## What counts as text

- Main and end titles, episode title cards, credits.
- Narrative text inside the image: signs, letters, screens, labels. In animation these are often painted into the
  background or texture; plan to render them on a separate layer from layout onwards.
- Burned-in subtitles for foreign-language lines (forced narratives).

## Deliverable shapes

| Element | Contents |
|---|---|
| Texted master | full programme with all text |
| Textless tail | after the programme, each texted shot again without text, with handles, in programme order |
| Textless full | entire programme with no text (some platforms) |
| Texted inserts list | timecode in/out of each texted shot in the master and its textless counterpart |

Netflix asks for textless material in the IMF package or as a textless tail; check the current Netflix partner
spec for whether a separate textless version is required for your title. Typical handle is a few frames each side.

## Animation production rule

Keep text as its own render pass or composite layer: localisation then re-renders only the text layer. Never let
text be painted into a background plate without a clean plate saved.

## Gotchas

- A textless shot must match its texted counterpart frame for frame, including grade.
- Text over moving animation needs a full textless render of the shot, not a freeze.
- Credits over picture need the textless background for the full credits duration.

## Verify

Toggle between texted master and textless tail at each listed timecode: identical picture except the text.
Related: `creative-arts.animation.encode-delivery.netflix-delivery-spec`.
