---
id: computing-software.cloud-infrastructure-engineering.site-reliability-engineering.test-and-treat-hypothesis-ordering
name: test-and-treat-hypothesis-ordering
category: computing-software
field: cloud-infrastructure-engineering
product: site-reliability-engineering
tags: [test-and-treat, hypothesis-testing-order, troubleshooting, differential-diagnosis, debugging]
level: practitioner
status: docs-checked
description: "Test troubleshooting hypotheses in a sensible order: likelihood and risk of the test, mutually exclusive outcomes, confounders and side effects, and clear notes of what you ran."
sources: ["https://sre.google/sre-book/effective-troubleshooting/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Test and treat: ordering hypotheses

SRE Book "Effective Troubleshooting", Test and Treat: with a short list of possible causes, use the experimental
method to rule hypotheses in or out. The Book's example: suspect either a network failure between an app server and a
database, or the database refusing connections. Connecting with the same credentials the app uses can refute the
second; pinging the database server may refute the first, depending on topology and firewall rules. Following the code
step by step can also show what is going wrong.

## Considerations when designing tests
1. **Mutually exclusive alternatives**: an ideal test rules one group of hypotheses in and another out. In practice
   this may be hard to achieve.
2. **Consider the obvious first**: run tests in decreasing order of likelihood, considering risk to the system from the
   test. Testing network connectivity between two machines comes before asking whether a recent config change removed a
   user's access.
3. **Confounding factors**: a firewall rule allowing only one source IP can make a ping from your workstation fail even
   though it would succeed from the app server.
4. **Side effects**: active tests can change later results. More CPUs may speed things up but raise the chance of data
   races; verbose logging can worsen a latency problem and confuse the result.
5. **Suggestive, not definitive**: races and deadlocks are hard to reproduce on demand, so you may have to settle for
   weaker evidence.

## Keep notes
Write down what ideas you had, which tests you ran and the results. Particularly in drawn-out cases this stops you
repeating steps. If an active test changed the system, make the changes systematically and document them so you can
return to the pre-test setup rather than an unknown mix of configurations.

## Negative results
The Book says negative results should not be ignored: realising you are wrong has value, and recording what was ruled
out helps others avoid the same dead ends.

## Common pitfalls (Book)
- Wildly improbable theories, or latching onto causes of past problems because it happened once.
- Hunting spurious correlations: coincidences, or events with a shared cause (its example: packet loss and failed hard
  drives in a cluster both caused by a power outage).

## Checked
2026-11-01. Confirmed against the SRE Book chapter "Effective Troubleshooting" (Test and Treat bullets, notes,
Negative Results Are Magic, common pitfalls and correlation text). Removed: the working table with example figures and
commands, the likelihood-over-cost ordering formula, the one-change-at-a-time and staging-confirmation rules and the
verify list; the page does not state them in that form.
Method: documentation only; no commands were run.
