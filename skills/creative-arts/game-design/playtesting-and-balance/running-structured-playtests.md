---
id: creative-arts.game-design.playtesting-and-balance.running-structured-playtests
name: running-structured-playtests
category: creative-arts
field: game-design
product: playtesting-and-balance
tags: [game-design, playtesting, playtest, user-research, games-user-research, think-aloud, observation, test-plan, questionnaire, telemetry, balance, tuning, win-rate, iteration, facilitation, debrief, board-games, video-games, kleenex-tester, blind-test, feedback]
level: practitioner
status: draft
description: "Run playtests that produce decisions: set one question per session, observe silently, separate what players do from what they say, log issues by severity, then change one thing and retest."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Running structured playtests — evidence, not opinions

**Goal:** each playtest answers a specific design question and ends with a short list
of prioritised changes, instead of a pile of suggestions you can't act on.

## 1. Before: write a test plan (half a page)
- **Question(s):** at most two or three. "Do players understand the crafting screen
  without the tutorial?" "Is the red faction winning too often?"
- **Build/version** under test, and what is known broken (so testers' time isn't spent on it).
- **Tester profile:** fresh ("kleenex" — used once) for learnability and first
  impressions; experienced for balance and depth. Friends and teammates are biased
  and already know too much; use them only for crash-finding.
- **Measures:** what you'll observe or count (time to complete, deaths, win rate,
  times they asked for help) and the 3–5 questions for after.

## 2. During: observe, don't teach
- Brief script: "We're testing the game, not you. Please think aloud. I may not answer
  questions — that helps us." Then stay quiet.
- If they ask how something works, reply "What do you think it does?" and note the
  question. Intervene only if they're fully stuck long enough that the rest of the
  session would be wasted — and log that as a severe issue.
- Note **behaviour** with timestamps: hesitations, wrong clicks, misread rules,
  facial reactions, the moment attention drops (phone out, leaning back).
- Record screen and audio if consented; for tabletop, photograph the board at key moments.

## 3. After: debrief briefly
Ask open questions first, specific ones last:
1. "Tell me about what you just played." (unprompted summary shows what landed)
2. "What was most confusing / frustrating?"
3. "What did you enjoy most?"
4. Your specific questions ("What did the blue bar mean?").
Scale ratings (1–5) are useful only when compared across sessions with the same question.

## 4. Interpreting feedback
- **What players do > what they say.** If they say "it's easy" but died five times, trust the deaths.
- **Problems are data; solutions are suggestions.** "Add a map" usually means "I'm
  lost" — fix the lostness your way.
- **Severity × frequency:** log each issue with how many testers hit it and a
  severity (blocker / major / minor). Fix blockers seen by 2+ testers first.
- One loud tester is one data point.

## 5. Balance tuning
- For competitive balance collect numbers: win rate by faction/character/start
  position, average game length, which options are picked or never picked.
- Expect noise: with a handful of games, a 60/40 win split can easily be chance.
  Treat small-sample win rates as hints and look for consistent patterns or
  supporting observation. (For rigor, a binomial test on the win counts helps; exact
  sample sizes needed depend on effect size.)
- **Change one variable at a time** where possible, and keep a change log so you can
  attribute effects. Big swings first to find the range, then smaller adjustments.
- Watch for **never-picked options** — often more damaging than overpowered ones.

## Gotchas
- **Leading questions** ("Did you like the new combat?") bias answers. Ask neutrally.
- **Designers defending the design** in the room ends honest feedback. Write it down,
  argue later (or never).
- **Testing too late:** paper or greybox prototypes are cheaper to fix. Test the
  first playable.
- **Fresh testers run out.** Budget them for the questions only they can answer.
- These practices follow common games-user-research guidance; sample-size advice is
  deliberately vague because it depends on the decision at stake.

## Verify
- [ ] A written test plan with ≤3 questions exists before the session.
- [ ] The facilitator didn't explain the game during play; questions were logged.
- [ ] Issues logged with frequency and severity, and the top ones assigned to fixes.
- [ ] Balance numbers recorded with sample size noted; one change per iteration logged.
- [ ] The next test re-checks the fixed issues with new testers.
