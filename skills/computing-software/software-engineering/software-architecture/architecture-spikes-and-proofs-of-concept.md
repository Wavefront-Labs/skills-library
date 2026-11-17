---
id: computing-software.software-engineering.software-architecture.architecture-spikes-and-proofs-of-concept
name: architecture-spikes-and-proofs-of-concept
category: computing-software
field: software-engineering
product: software-architecture
tags: [software-architecture, architecture-evaluation, architecture-spike, proof-of-concept, risk-reduction, prototyping]
level: practitioner
status: draft
description: "Retire architectural risk with time-boxed spikes and proofs of concept: frame the question, success criteria, minimal build, measured results, and throwing the code away."
sources: ["https://www.oreilly.com/library/view/fundamentals-of-software/9781492043447/", "http://www.extremeprogramming.org/rules/spike.html", "https://www.scaledagileframework.com/spikes/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Spikes and proofs of concept to retire risk

## Frame the question first
A spike answers one question whose answer changes a decision:
- "Can Postgres logical replication keep up with 5k writes/s to our analytics store with < 30 s lag?"
- "Does vendor X's SDK support our SSO flow without a custom proxy?"
- "Can WASM plug-ins run under 10 ms per call?"
Write: question, why it matters (which decision/ADR), success/fail criteria with numbers, time-box
(1-5 days), and what you'll do in each outcome.

## Build the minimum
- Only the path that tests the risk; fake everything else. No UI, no auth unless that's the risk.
- Use production-like data volumes and infrastructure for performance questions; laptop results
  mislead.
- Measure with the same tools you'll use in production (load generator, profiler).

## Report
One page: question, setup, results (numbers, graphs), answer, confidence, caveats, recommendation,
link to code. Update the ADR. A "no" is a successful spike.

## Throw it away
Spike code is written without tests or error handling; label the repo/branch `spike/` and don't
promote it. If the PoC becomes the product, schedule the rewrite explicitly. A **walking skeleton**
(thin end-to-end production-quality slice) is the alternative when you need to keep the code.

## Pick what to spike
Riskiest assumptions first: novel technology, extreme quality-attribute targets, integrations
with external systems, anything where the team says "should be fine" without evidence.
