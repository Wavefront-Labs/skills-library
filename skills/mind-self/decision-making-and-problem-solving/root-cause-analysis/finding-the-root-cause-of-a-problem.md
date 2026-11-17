---
id: mind-self.decision-making-and-problem-solving.root-cause-analysis.finding-the-root-cause-of-a-problem
name: finding-the-root-cause-of-a-problem
category: mind-self
field: decision-making-and-problem-solving
product: root-cause-analysis
tags: [decision-making-and-problem-solving, root-cause-analysis, rca, five-whys, 5-whys, fishbone-diagram, ishikawa, cause-and-effect-diagram, cause-mapping, causal-chain, symptom-vs-cause, correlation-vs-causation, verify-the-cause, corrective-action, toyota, lean, blameless-postmortem, recurring-problems, problem-solving]
level: practitioner
status: draft
description: "Trace a recurring problem past its symptoms: describe it precisely, run a disciplined five-whys or fishbone, test the suspected cause before fixing, and confirm the fix stops recurrence."
sources: ["Ohno, Toyota Production System (1988)", "Ishikawa, Guide to Quality Control (1968)", "Kepner & Tregoe, The New Rational Manager (1981)", "Card, The problem with '5 whys', BMJ Quality & Safety (2017)"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Finding the root cause of a problem

**Goal:** stop a problem coming back by fixing what actually causes it, not the most
visible symptom — in a household, a team process, a small business or a hobby project.
(For engineering failure analysis and formal incident investigation, see the domain
skills under engineering and occupational health.)

## 1. Describe the problem precisely
Write a problem statement covering **what, where, when, how much** — and what it is *not*
(Kepner-Tregoe's "is / is not"):
- Is: "Customer orders shipped late, 14 of 60 in March, all from the weekend batch."
- Is not: "Weekday orders on time; all products affected equally."
The is/is-not contrast is often the biggest clue: what's different about the weekend?

## 2. Contain first if needed
If the problem is causing harm now, apply a temporary fix (a manual check, a workaround)
and label it temporary. Don't let containment become the permanent "solution".

## 3. Five whys — done properly
Ask "why did that happen?" repeatedly, answering with **facts**, not guesses.
1. Why were weekend orders late? → They weren't picked until Monday afternoon.
2. Why? → Monday's picker spent the morning on returns.
3. Why? → Returns are processed first by default.
4. Why? → The task list sorts by date received, and returns arrive Friday.
5. Why? → No one set priorities when the list was set up.
Root cause candidate: no priority rule for picking vs returns.

Rules: "five" is a rough guide, not a target; stop when you reach something you can
change that would prevent recurrence. **Branch** when there's more than one cause — a
single chain often oversimplifies (Card, 2017, criticises five whys for exactly this).

## 4. Fishbone for multiple causes
Draw the problem as the fish's head; bones for categories, e.g. **People, Process,
Equipment/Tools, Materials, Environment, Measurement** (adapt to your situation).
Brainstorm possible causes on each bone with the people involved. Then circle the
candidates that fit the is/is-not facts.

## 5. Verify the cause before fixing
A plausible story is not a cause. Test it:
- **Does it explain every fact** in the is/is-not? If weekend orders are late but the
  cause would also hit Wednesdays, it's wrong or incomplete.
- **Switch it on/off:** change the suspected cause for a week and see if the problem
  follows.
- **Check timing:** did the problem start when the cause appeared?
- **Correlation ≠ causation:** two things rising together may share a third cause.

## 6. Fix and confirm
- Pick a fix that removes or blocks the cause (change the default order, add a rule)
  rather than relying on people to remember.
- Define success up front ("zero late weekend orders for four weeks").
- Monitor; if the problem returns, the root cause was wrong or there were several.

## Gotchas
- **Stopping at "human error".** Ask why the error was easy to make; the fix is usually in
  the system. Blameless reviews surface more truth.
- **Jumping to the first plausible cause** — the most common failure.
- **One root cause** is often a simplification; complex problems have contributing factors.
- **Fixing symptoms repeatedly** feels productive; the recurrence count says otherwise.

## Verify
- [ ] The problem statement has what/where/when/how much and is/is-not.
- [ ] Each "why" answer is backed by a fact you checked.
- [ ] The suspected cause explains all the is/is-not facts.
- [ ] You tested the cause (on/off or timing) before committing to a fix.
- [ ] The problem has not recurred over the agreed monitoring period.
