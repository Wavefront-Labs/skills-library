---
id: media-communication.persuasive-messaging.message-testing.designing-and-reading-message-tests
name: designing-and-reading-message-tests
category: media-communication
field: persuasive-messaging
product: message-testing
tags: [message-testing, message-polling, survey-experiment, randomized-controlled-trial, rct, a-b-testing, ab-test, focus-groups, dial-testing, persuasion-effect, uplift, control-group, treatment-effect, sample-size, statistical-significance, confidence-interval, backlash, subgroup-analysis, message-research, persuasive-messaging]
level: practitioner
status: draft
description: "Find out which message actually persuades: randomised survey experiments with a control, focus groups for language not verdicts, A/B field trials, and reading effects without fooling yourself."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Designing and reading message tests

**Goal:** evidence about which message changes opinion or behaviour in your target audience
— not which one people *say* they like, and not which one your team likes.

## 1. Pick the right method for the question
| Question | Method |
|---|---|
| What words do people use? What confuses them? | Focus groups / interviews (qualitative) |
| Which of 3–8 messages shifts opinion most? | Randomised survey experiment |
| Which version gets more clicks, sign-ups, donations? | A/B field test on real channels |
| Does it change real-world behaviour (turnout, uptake)? | Field experiment with a holdout |
Qualitative work generates and refines messages; it can't rank them reliably — groups of
8 people, dominant voices, and social desirability make "the room liked B" weak evidence.

## 2. Survey experiments done properly
- **Randomise** respondents into arms: each sees one message (or none).
- **Always include a control** (no message or a neutral placebo text). Without it, you
  only know relative ranking, not whether anything works — or backfires.
- **Measure the outcome after exposure**, with the same question in every arm (e.g.
  support 0–10, likelihood to act). Don't ask "how persuasive was this?" — self-reported
  persuasiveness correlates poorly with measured persuasion.
- **Sample size:** persuasion effects are often small (a few points). Detecting a 3-point
  difference on a 0–100 scale typically needs hundreds to over a thousand respondents per
  arm; do a power calculation rather than guessing. Fewer arms = more power each.
- Use realistic stimuli: the message as it would actually appear (ad, mailer, script),
  not a bullet point.
- Field with a panel that can reach the target segment; check quotas and attention checks.

## 3. Reading results honestly
- Report **treatment minus control** with a confidence interval, not just the top-line.
- If intervals overlap heavily, the messages are statistically indistinguishable — say so.
  Picking the "winner" by 0.8 points is noise.
- **Subgroups:** pre-register which segments you'll look at. Slicing 20 subgroups will find
  a "significant" one by chance (~1 in 20 at p<0.05).
- **Backlash:** check whether any message *lowers* support among a segment (e.g. the base or
  a persuadable group). A message that gains 2 among one group and loses 6 among another
  may be a net loss.
- Persistence: effects measured immediately often decay; if possible re-contact days later.
- Watch for **ceiling effects** (base already at max) and **priming** from earlier questions.

## 4. A/B and field tests
- Split traffic randomly, change one thing at a time, fix the sample size and run length
  *before* starting, and don't stop when it first looks good ("peeking" inflates false
  positives).
- Platform A/B tools optimise for clicks; clicks are not persuasion. Pick the metric that
  matches the goal.
- For behaviour (turnout, vaccination, donations), keep a randomised **holdout** that gets
  nothing so you can measure true lift.

## 5. Focus groups (for what they're good at)
- 6–8 participants, a moderator with a funnel guide (broad → specific), and an observer.
- Recruit from the target segment, screened; run at least two groups per segment.
- Listen for language to steal, confusions, objections and emotional reactions. Report
  quotes and themes, not vote counts (see sales-marketing.market-research-consumer-insights.focus-group-moderation.discussion-guide-and-moderation).

## Gotchas
- Testing messages only among your supporters.
- Letting the creative team write the control so it's weak.
- Treating a click-through win as an opinion shift.
- Over-reading tiny samples or a single test; replicate important findings.

## Verify
- [ ] Method matches the question (qual for language, experiment for ranking).
- [ ] Every experiment has a randomised control arm.
- [ ] Sample size set by a power calculation before fielding.
- [ ] Results shown as effect vs control with intervals; ties called ties.
- [ ] Subgroups pre-specified and backlash checked.
