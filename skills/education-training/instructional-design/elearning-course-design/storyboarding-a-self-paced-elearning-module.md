---
id: education-training.instructional-design.elearning-course-design.storyboarding-a-self-paced-elearning-module
name: storyboarding-a-self-paced-elearning-module
category: education-training
field: instructional-design
product: elearning-course-design
tags: [elearning-course-design, elearning, e-learning, online-course, self-paced, asynchronous, storyboard, storyboarding, design-document, prototype, screen-design, interaction-design, knowledge-checks, completion-criteria, navigation, menu, branching-navigation, locked-navigation, accessibility, wcag, sme-review, alpha-beta-review, click-next, microlearning, articulate, captivate, rise, instructional-design]
level: practitioner
status: draft
description: "Design a self-paced e-learning module on paper first: design doc, screen-by-screen storyboard, meaningful interactions, knowledge checks with feedback, completion rules and SME review rounds."
sources:
  - "Clark, R. C. & Mayer, R. E. e-Learning and the Science of Instruction, 4th ed. (2016)"
  - "Moore, C. Map It (2017) — action mapping"
  - "W3C, Web Content Accessibility Guidelines (WCAG) 2.2"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Storyboarding a self-paced e-learning module

**Goal:** a module whose structure, wording, interactions and tracking are fully agreed on
paper before anyone builds it — because changes in a storyboard cost minutes and changes in
an authoring tool cost days.

## 1. Write a one-page design document first
- Audience, prior knowledge, device (desktop / mobile / both), access context (shop floor? 10
  minutes between calls?).
- Terminal objectives (see
  education-training.instructional-design.learning-objective-design.writing-measurable-objectives-and-aligning-a-course).
- Seat time target (e.g. 15–20 minutes), number of sections, assessment approach.
- **Completion rule** (viewed all screens? passed quiz at 80%? both?) and what's reported to the LMS.
- Navigation model: free, locked-until-viewed, or locked-until-passed.
- Look and feel, voiceover yes/no, languages, accessibility standard (typically WCAG 2.1/2.2 AA).
Get sponsor sign-off. Nearly every late dispute traces back to an unstated item here.

## 2. Outline before screens
Section → screens list with one purpose per screen. A typical section pattern: *hook
(scenario or question) → short content → practice interaction → feedback*. If a section is all
content screens in a row, it's a slideshow, not e-learning.

## 3. The storyboard format
A table (Word/Excel/Google Docs) or slide-per-screen template; one row/slide per screen:
| Field | Contents |
|---|---|
| Screen ID | 2.03 — stable IDs make SME comments traceable |
| Title | On-screen title |
| On-screen text | Exact text, final wording |
| Narration / audio | Exact script, if any (don't duplicate on-screen text word-for-word) |
| Visuals | Description or sketch; image source |
| Interaction | What the learner does; every state |
| Feedback | Exact correct/incorrect text per choice |
| Navigation / triggers | What enables Next; where branches go |
| Developer notes | Variables, tracking, alt text |
Write **final wording**, not "explain the policy here". The storyboard is the script.

## 4. Interactions that earn their place
- Prefer interactions that make learners **decide or apply**: choose the next action, spot the
  error, sort cases, answer a scenario question
  (see education-training.instructional-design.scenario-based-learning.writing-branching-scenarios).
- Click-to-reveal tabs and flip cards are presentation, not practice; use sparingly.
- **Knowledge checks:** after each section, 1–3 questions on that section's objective, with
  feedback that explains *why*, not just "Correct!".
- **Final assessment:** a separate question bank aligned to objectives; draw randomly if retakes
  are allowed; define the pass mark and attempt limits.

## 5. Accessibility from the storyboard
Record alt text for every meaningful image, captions/transcripts for audio, keyboard-operable
interactions (drag-and-drop needs an alternative), sufficient colour contrast, and no information
carried by colour alone.

## 6. Review cycle
1. **Storyboard review** by SME (accuracy) and sponsor (scope) — consolidate into one marked-up copy.
2. **Alpha** build: review functionality and visuals.
3. **Beta** (near-final) with 3–5 real learners if possible — watch them, don't just survey.
4. **Gold**: final, tested in the actual LMS.
Agree the number of review rounds in the design doc.

## Gotchas
- **Content dump**: SMEs send 80 slides; the module tries to include all of them. Cut to what the
  objectives need; the rest goes into a downloadable job aid.
- **Locked navigation everywhere** frustrates experienced learners; consider a pre-test that
  lets them skip.
- **Narration that reads the screen** aloud harms learning for most adults (redundancy).
- **Untested tracking**: completion logic that works in preview can fail in the LMS — test early
  (education-training.instructional-design.scorm-and-xapi.packaging-and-debugging-lms-tracking).
- *Unconfirmed:* seat-time-per-screen estimates vary widely (often quoted 1–2 min/screen); time
  a pilot learner instead.

## Verify
- [ ] Design doc signed off, including completion rule and navigation model.
- [ ] Every screen has final text, interaction states, feedback and navigation logic.
- [ ] Each section has at least one apply-level interaction, not just reveals.
- [ ] Alt text, captions and keyboard alternatives are specified.
- [ ] SME and sponsor comments are resolved in one consolidated storyboard before build.
