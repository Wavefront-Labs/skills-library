---
id: computing-software.cloud-infrastructure-engineering.site-reliability-engineering.effective-troubleshooting-method
name: effective-troubleshooting-method
category: computing-software
field: cloud-infrastructure-engineering
product: site-reliability-engineering
tags: [site-reliability-engineering, sre, troubleshooting, troubleshooting-method, systematic-troubleshooting, debugging-production, hypothetico-deductive, problem-report, triage, examine, diagnose, test-treat, bisection, divide-and-conquer, what-changed, correlation-vs-causation, negative-results, incident-diagnosis, simplify-and-reduce, mitigation-first]
level: advanced
status: docs-checked
description: "Debug production systematically rather than by hunch: the SRE troubleshooting loop (problem report, triage, examine, diagnose, test/treat), what-changed and bisection heuristics."
sources: ["https://sre.google/sre-book/effective-troubleshooting/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Effective troubleshooting

**Goal:** go from "something is wrong" to a mitigated system and a verified cause with
the fewest, most informative steps: a learnable method, not a talent.

## 1. The loop (hypothetico-deductive, SRE Book ch. 12)
Problem report, then Triage, Examine, Diagnose, Test/Treat, Cure; iterate on hypotheses until one holds.
1. **Problem report**: what is wrong, how it differs from expected, scope, and how to reproduce. Everything starts here.
2. **Triage**: match the response to impact (an all-hands emergency for a global outage is right; for one user with a
   workaround it is overkill). In a major outage the book says to ignore the instinct to root-cause first: make the system
   work as well as it can (divert traffic from a broken cluster, drop traffic to prevent a cascading failure, disable
   subsystems to lighten load). Stopping the bleeding is the first priority, while preserving evidence such as logs.
3. **Examine**: use telemetry (graph time series), logs and request tracing to see the current state of each component.
   Text logs help real-time debugging; structured binary logs enable retrospective tools.
4. **Diagnose**: use your knowledge of the design to form plausible hypotheses, helped by generic practices below.
5. **Test/Treat**: rule hypotheses in or out experimentally; see the test design points below.
6. **Cure**: prove the cause if you can. In production you often only find probable causes: systems are complex, several
   factors may act jointly, and reproducing in production may not be acceptable.

## 2. Diagnosis practices (from the book)
- **Simplify and reduce**: components with well-defined interfaces let you inject known test data at each step (black-box
  testing) and check the output. A reproducible test case speeds debugging and may be usable in non-production.
- **Divide and conquer**: work through a layered stack or pipeline from one end to the other; in very large systems use
  **bisection**: split the system in half, check the paths between halves, repeat until one component remains.
- **Ask "what", "where" and "why"**: a malfunctioning system is still doing something; find what, then why, then where
  resources go (the book's example traces high RPC latency to CPU use, then to a backtracking regular expression).
- **What touched it last**: working systems stay in motion until something changes. Log deployments and config changes at
  every layer and annotate graphs with deployment start and end times.

## 3. Designing tests
- Prefer tests with mutually exclusive alternatives so they rule one group of hypotheses in and another out.
- Test the obvious first, in decreasing order of likelihood, weighing the risk each test poses to the system.
- Watch for confounders (a firewall that blocks your workstation but not the app server) and side effects (verbose
  logging or extra CPUs can change the behaviour you are measuring).
- Some tests are only suggestive (races, deadlocks).
- Keep clear notes of ideas, tests and results, and make changes systematically so you can restore the pre-test setup.

## 4. Pitfalls named by the book
| Pitfall | Meaning |
|---|---|
| Looking at irrelevant symptoms | chasing what is not related to the failure |
| Misunderstanding how to change the system or its inputs safely | tests that do not test the hypothesis |
| Wildly improbable theories | skipping simpler explanations |
| Spurious correlations | coincidence, or events with a shared cause (the book's example: packet loss and disk failures from a power outage) |

Correlation is not causation, and with more metrics some will correlate by pure chance.

## 5. Negative results
The book's "Negative Results Are Magic" sidebar: an experiment that does not show the expected effect is conclusive
about production or the design space, and should be recorded and published so others do not repeat it.

## Gotchas
- Diagnosing while the site is down: mitigate first where a safe mitigation exists, keep the evidence.
- A reproducible test case beats theorising; make one before arguing about causes.

## Verify
- [ ] Your last three incident records show explicit hypotheses, the test for each, and the result, not just actions.
- [ ] Mitigation preceded diagnosis in the last major outage, and logs were preserved for root-cause work.

## Checked
2026-11-01. Confirmed against the SRE Book chapter "Effective Troubleshooting" (the loop and its steps, triage and
stopping the bleeding, simplify and reduce, divide and conquer and bisection, what touched it last, test design cautions,
cure caveats, pitfalls, correlation vs causation, negative results). Removed: the golden-signal and tool-by-question
sections (kubectl, ss, strace and profiler commands), the 24 hour change-log window, the 20 minute onboarding exercise,
the percentile example and sources not read in this review.
Method: documentation only; no commands were run.
