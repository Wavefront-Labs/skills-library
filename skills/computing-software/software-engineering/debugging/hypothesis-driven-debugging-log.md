---
id: computing-software.software-engineering.debugging.hypothesis-driven-debugging-log
name: hypothesis-driven-debugging-log
category: computing-software
field: software-engineering
product: debugging
tags: [debugging, systematic-debugging, scientific-method, hypothesis-driven-debugging, debugging-log, falsification, rubber-duck, root-cause]
level: practitioner
status: draft
description: "Debug with the scientific method: write hypotheses and predictions in a debugging log, design experiments that falsify, and avoid confirmation bias and random edits."
sources: ["Why Programs Fail, 2nd ed. (Zeller), ch6 Scientific Debugging", "https://www.debuggingbook.org/html/Intro_Debugging.html", "Debugging: The 9 Indispensable Rules (Agans)"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Hypothesis-driven debugging with a log

**Goal:** converge on the root cause in a bounded number of steps instead of changing
things until the symptom disappears.

## The loop (Zeller's scientific debugging)
1. **Observe** the failure precisely (inputs, outputs, environment, exact error).
2. **Hypothesise** a cause consistent with ALL observations so far.
3. **Predict** something that must be true if the hypothesis holds (a value at a
   point, a log line, a behaviour change under an altered input).
4. **Experiment** to test the prediction: debugger, log, altered input, assertion.
5. **Conclude**: confirmed -> refine toward the cause; rejected -> discard it and note why.
Repeat until the hypothesis explains the failure and a fix based on it makes the
failure go away AND you can explain why.

## Keep a debugging log
A text file or ticket comment, one entry per iteration:
```
H3: cache returns stale entry because TTL uses local time
Prediction: entry.expires_at is in the future in UTC but past in local time at 23:30
Experiment: run with TZ=UTC and TZ=Australia/Sydney, same clock
Result: fails only with Sydney -> CONFIRMED (partially: also need DST transition?)
Next: H4 ...
```
Benefits: you stop re-testing discarded ideas, handover to a colleague is instant,
and the postmortem writes itself. It's the cheapest tool with the biggest payoff on
multi-day bugs.

## Experiments that discriminate
- Prefer experiments whose outcome differs between your top two hypotheses.
- Change one variable at a time.
- Make it cheaper: shrink the input (delta debugging), shorten the reproduction,
  bisect the history.
- Strong evidence beats weak: a watchpoint catching the write beats "the log looked fine".

## Biases to fight
- Confirmation bias: try to FALSIFY your favourite hypothesis.
- "It can't be X" (the library, the compiler, the hardware): it's usually your code, but
  verify assumptions instead of trusting them ("check the plug").
- Fixing the symptom where it shows up rather than where the infection started; trace
  the bad value back to its origin.
- Explain the bug out loud (rubber duck) when stuck: forces precise statements.

## Done means
- Root cause identified and explained by a hypothesis consistent with every observation.
- A regression test that failed before the fix and passes after.
- Search for the same defect pattern elsewhere.

## Verify
- [ ] Log contains each hypothesis with its experiment and outcome.
- [ ] The fix is justified by a confirmed hypothesis, not by "it stopped happening".
