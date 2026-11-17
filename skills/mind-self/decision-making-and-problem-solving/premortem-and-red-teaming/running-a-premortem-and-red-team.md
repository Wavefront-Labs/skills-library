---
id: mind-self.decision-making-and-problem-solving.premortem-and-red-teaming.running-a-premortem-and-red-team
name: running-a-premortem-and-red-team
category: mind-self
field: decision-making-and-problem-solving
product: premortem-and-red-teaming
tags: [decision-making-and-problem-solving, premortem, pre-mortem, prospective-hindsight, gary-klein, red-teaming, red-team, devils-advocate, devils-advocacy, failure-modes, failure-mode-listing, assumption-busting, key-assumptions-check, groupthink, optimism-bias, planning-fallacy, risk-register, kill-criteria, plan-review]
level: practitioner
status: draft
description: "Stress-test a plan before committing: run a premortem, list and test key assumptions, assign a red team or devil's advocate, and turn findings into mitigations and kill criteria."
sources: ["Klein, Performing a project premortem, Harvard Business Review (2007)", "Mitchell, Russo & Pennington, Back to the future: temporal perspective in the explanation of events (1989)", "UK Ministry of Defence, Red Teaming Handbook, 3rd ed. (2021)", "Janis, Groupthink (1982)"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Running a premortem and red team

**Goal:** find the ways a plan will fail while you can still change it — counteracting
the optimism, groupthink and planning fallacy that settle on any team (or individual)
that has just agreed on a plan.

## The premortem (Gary Klein) — 30–45 minutes
Run it after a plan is drafted but before final commitment.
1. **Set the scene:** "It's [date, e.g. a year from now]. We went ahead with this plan,
   and it was a clear failure."
2. **Silent writing (5–10 min):** everyone independently writes every reason it failed.
   Silent and independent is essential — it stops the boss's view or the first speaker
   steering the group.
3. **Round-robin:** go around, one reason per person per turn, until all are listed. The
   leader or plan owner goes last.
4. **Cluster and rate:** group similar reasons; rate each by likelihood and impact.
5. **Act on the top ones:** change the plan, add a mitigation, or add an early-warning
   indicator.
Why it works: imagining failure as **already happened** (prospective hindsight) makes it
easier to generate specific reasons — Mitchell et al. (1989) found it increased the
number of reasons people produced for an outcome. It also gives permission to voice doubts.

Solo version: write the failure story yourself, then ask one sceptical friend to add to it.

## Key-assumptions check
List every assumption the plan depends on ("users will pay £10/month", "the supplier
delivers in 4 weeks", "I'll have evenings free"). For each:
- How confident are we, and on what evidence?
- What happens to the plan if it's false?
- How could we test it cheaply before committing?
Flag the **load-bearing, low-confidence** ones — they are your real risks.

## Red teaming and devil's advocacy
- **Devil's advocate:** one person argues against the plan in a meeting. Rotate the role
  so it isn't personal, and make it explicit that the role is assigned. Research suggests
  token or half-hearted dissent is easy for groups to dismiss — authentic dissent is more
  effective, so give the advocate time to prepare.
- **Red team:** a separate small group (ideally not the plan's authors) tries to break the
  plan — finds weak points, plays a competitor, adversary or sceptical customer.
  Give them the same information and real time. Ask for a written report.
- **Steelman alternatives:** have someone make the best possible case for the option you
  rejected.

## Turn findings into action
For each top risk, decide:
- **Change** the plan to remove it.
- **Mitigate** (backup supplier, buffer time, insurance).
- **Monitor:** an early-warning signal with a named owner.
- **Kill criteria:** conditions under which you'll stop or pivot, written now ("if fewer
  than 50 sign-ups by week 6, we stop"). Deciding in advance protects against sunk-cost
  thinking later.

## Gotchas
- **Ritual without consequence:** if nothing in the plan changes, the exercise was theatre.
- **Seniority suppression:** leaders speaking first or reacting defensively shuts it down.
- **Catastrophising:** a long list of unlikely failures can paralyse; prioritise by
  likelihood × impact.
- **Too late:** after money is spent and people are committed, findings get rationalised away.
- Evidence for premortems specifically is mostly field experience plus the prospective-
  hindsight research; controlled studies of outcomes are limited.

## Verify
- [ ] Failure reasons were written silently and independently before discussion.
- [ ] Load-bearing assumptions are listed with confidence levels and cheap tests.
- [ ] Someone other than the plan's author argued the opposing case.
- [ ] At least one change to the plan resulted.
- [ ] Kill criteria and early-warning signals have owners and dates.
