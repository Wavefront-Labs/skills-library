---
id: computing-software.game-programming.game-ai-programming.goal-oriented-behaviour-with-motives
name: goal-oriented-behaviour-with-motives
category: computing-software
field: game-programming
product: game-ai-programming
tags: [game-ai-programming, goal-oriented-behaviour, motives, needs-based-ai, game-programming]
level: practitioner
status: gated
description: "Implement goal-oriented behaviour with motives: insistence values, actions scored by discontentment reduction, time-aware choices and Sims-style needs AI."
sources: ["https://www.gameaipro.com/GameAIPro/GameAIPro_Chapter09_An_Introduction_to_Utility_Theory.pdf", "https://en.wikipedia.org/wiki/The_Sims"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Goal-oriented behaviour with motives

**Goal:** characters that pick actions to satisfy several competing needs (hunger, energy, fun),
(goal-oriented behaviour, GOB; The Sims' hunger stat is the standard example, see Game AI Pro ch. 9).

## Model
- Each **goal/motive** has an insistence value that grows over time (`hunger += rate * dt`).
- Each **action** changes insistences (`eat: hunger -40, takes 30 min`), possibly several at once.
- Choose the action that minimises total **discontentment** after taking it:
```python
def discontentment(goals): return sum(g.value ** 2 for g in goals)   # squaring favours urgent needs
def choose(actions, goals):
    return min(actions, key=lambda a: discontentment([g.after(a) for g in goals]))
```
Squaring (or any convex function) means one very urgent need beats several mild ones.

## Time awareness
Actions take time, during which other needs grow. Include duration: `g.after(a) = g.value +
a.change[g] + g.rate * a.duration`. Long actions that ignore a rising need lose naturally.

## Smart objects (The Sims)
Objects advertise which motives they satisfy and by how much (gated: unconfirmed, source is paywalled or blocked); the agent queries nearby objects,
scores advertisements (adjusted by distance and personality), and picks among the top few with
weighted randomness for variety.

## Relation to other techniques
- Utility AI generalises this with response curves per consideration.
- GOAP adds multi-step planning when actions have preconditions (need money before buying food).

## Pitfalls
- Dithering between two equal actions: commit to an action until done or interrupted by a large
  change.
- Rates and magnitudes need tuning tools; visualise motive bars per agent.

## Verify
- Run a sim for in-game days; motives stay bounded and agents cycle through activities plausibly.

## Checked (2026-10-22)
- Ran the `discontentment` / `choose` code with three motives: choosing between 'eat a lot' (hunger 9 to 5) and 'chores' (-2, -2, -1 on three others) picks eat-a-lot with squared values and chores with a linear sum, which is the 'urgent need beats several mild ones' claim; the time-aware `g.after(a)` formula also runs (with these rates it still picks eat).
- Game AI Pro ch. 9 PDF confirms the Sims hunger-stat example. Removed the claim that the technique 'is' Millington's GOB (book not available) and marked the smart-object advertising description with the gated marker (no free primary source found), so the skill is gated.
