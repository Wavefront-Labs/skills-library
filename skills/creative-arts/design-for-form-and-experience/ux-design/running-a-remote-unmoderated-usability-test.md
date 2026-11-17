---
id: creative-arts.design-for-form-and-experience.ux-design.running-a-remote-unmoderated-usability-test
name: running-a-remote-unmoderated-usability-test
category: creative-arts
field: design-for-form-and-experience
product: ux-design
tags: [remote-unmoderated-testing, unmoderated-usability-test, remote-usability-testing, usability-testing, online-testing-tools]
level: practitioner
status: draft
description: "Run a remote unmoderated test: write self-explanatory tasks, set success checks, screen for quality, pilot, and analyse recordings and metrics at scale."
sources:
  - "Nielsen Norman Group topics (nngroup.com/topics)"
  - "Tom Tullis and Bill Albert, Measuring the User Experience, 2nd ed. (Morgan Kaufmann, 2013)"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Remote unmoderated usability tests

Participants complete tasks on their own device with instructions delivered by a tool, which records screens, clicks and sometimes voice and faces. It scales cheaply but gives less ability to probe.

## When to use
- Quantitative measures (success rate, time, SUS) with many users.
- Comparing designs or tracking a benchmark (see `...ux-design.running-a-ux-benchmarking-study`).
- Specific, well-defined tasks. Poor for exploring unclear problems or complex products.

## Set up
1. **Choose a platform** that supports your prototype or live site, screen recording, task success checks and your participant source (own panel or a vendor).
2. **Write tasks** that need no facilitator: clear context, one goal, and an unambiguous end condition (see `...ux-design.writing-task-scenarios`). Include a self-reported success question, a confidence rating, and a follow-up open question.
3. **Add screener and quality checks:** attention questions, minimum time, device and browser requirements, and a way to discard speeders or non-attempters.
4. **Write instructions that explain think-aloud** if you want voice.
5. **Pilot** with a few people and fix confusing tasks.
6. **Launch** with enough participants for the analysis you need; watch early sessions for problems.

## Analyse
- Compute success rate, time on task (median, due to skew), and ratings; review a sample of recordings for the reasons behind failures; cluster open comments.
- Report confidence intervals for key rates.

## Verify
- [ ] Tasks were understood by pilot users without help.
- [ ] Low-quality responses were filtered with stated rules.
- [ ] Failures were explained from recordings, not guessed.
