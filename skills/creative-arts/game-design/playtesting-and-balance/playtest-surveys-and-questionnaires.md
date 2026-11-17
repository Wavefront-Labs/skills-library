---
id: creative-arts.game-design.playtesting-and-balance.playtest-surveys-and-questionnaires
name: playtest-surveys-and-questionnaires
category: creative-arts
field: game-design
product: playtesting-and-balance
tags: [game-design, playtest-survey, game-experience-questionnaire, playtest-analysis, likert-scale, geq, pens, survey-design, questionnaire]
level: practitioner
status: draft
description: "Write playtest surveys that produce usable data: Likert items, avoiding leading and double-barrelled questions, validated scales (GEQ, PENS), and comparing builds."
sources:
  - https://research.tue.nl/en/publications/the-game-experience-questionnaire
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Playtest surveys and questionnaires

**Goal:** post-session questionnaires that measure what you need, are comparable
between builds, and don't put words in players' mouths.

## Question design rules
1. **One concept per question** (no "Was the combat fun and fair?" - double-barrelled).
2. **Neutral wording** ("How would you rate the difficulty?" not "Was it too hard?").
3. **Likert scales** with labelled ends (e.g. 1 Strongly disagree - 5/7 Strongly agree);
   keep the same scale throughout.
4. **Behavioural over hypothetical:** "Which weapon did you use most?" beats "Would you
   buy this?".
5. **Open questions** after scales: "What, if anything, was confusing?" Keep to 2-3.
6. **Order:** general impressions first (before specific questions bias them), then
   specifics, demographics last.
7. **Length:** short enough to finish in ~5-10 minutes.

## Validated instruments
- **Game Experience Questionnaire (GEQ)** (IJsselsteijn, de Kort, Poels; TU Eindhoven):
  components such as competence, immersion, flow, tension, challenge, positive and
  negative affect; also in-game and post-game short forms. Note: later psychometric
  work has questioned parts of its factor structure; use carefully.
- **PENS** (Player Experience of Need Satisfaction; Rigby and Ryan): competence,
  autonomy, relatedness, presence, intuitive controls (commercial licence).
- Others exist (e.g. PXI); validated scales enable comparison but are not tailored.

## Analysis
- Report medians and distributions, not just means, for Likert items.
- Compare builds with the same questions and similar participant profiles.
- Code open answers into themes (affinity mapping) and count frequency.
- Small samples: treat as directional; don't over-interpret small differences.

## Gotchas
- Surveys measure what players say, not what they do; pair with observation and
  telemetry.
- Asking players how to fix problems yields poor designs; ask about experience instead
  (see `creative-arts.game-design.playtesting-and-balance.interpreting-player-feedback`).
- Survey fatigue after long sessions lowers quality; keep it short.

## Verify
- [ ] No leading or double-barrelled questions (peer-reviewed).
- [ ] Same scale and wording across builds.
- [ ] Results reported with distributions and themes from open answers.
