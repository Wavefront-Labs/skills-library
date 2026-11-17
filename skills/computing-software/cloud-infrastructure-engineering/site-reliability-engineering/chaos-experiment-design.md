---
id: computing-software.cloud-infrastructure-engineering.site-reliability-engineering.chaos-experiment-design
name: chaos-experiment-design
category: computing-software
field: cloud-infrastructure-engineering
product: site-reliability-engineering
tags: [chaos-experiment-design, chaos-hypothesis, chaos-engineering, chaos-mesh, litmus, fault-injection]
level: advanced
status: docs-checked
description: "Design chaos experiments from the Principles of Chaos: steady-state hypothesis, real-world variables, minimal blast radius, automated abort, with a Chaos Mesh PodChaos example."
sources: ["https://principlesofchaos.org/", "https://chaos-mesh.org/docs/simulate-pod-chaos-on-kubernetes/", "https://sre.google/sre-book/testing-reliability/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Chaos experiment design

Principles of Chaos Engineering: build a hypothesis around steady-state behaviour, vary real-world events,
run experiments in production (the principles prefer production traffic), automate to run continuously,
minimise blast radius.

## Experiment card
```
Steady state:   a measurable output, e.g. checkout success ratio and latency percentiles
Hypothesis:     the steady state continues in control and experiment groups
Variable:       the injected event, e.g. kill one cart-service pod
Blast radius:   as small as possible; widen only after it holds
Abort:          a metric threshold that stops the experiment automatically
Observability:  dashboard link; trace sampling raised during run
Result:         confirmed / refuted, with graphs
```
Refuted hypotheses are the valuable outcome: they reveal a weakness before an outage does.

## Real-world variables to inject (start simple)
The principles suggest hardware failures (servers dying), software failures (malformed responses) and
non-failure events (traffic spike, scaling event). Prioritise by impact or estimated frequency.

## Chaos Mesh example
PodChaos with `action: pod-kill` and `mode: one` kills one selected pod once; `action: pod-failure`
with a `duration` makes pods unavailable for that time. Select targets with `selector.labelSelectors`
and apply with `kubectl apply -f`. Chaos Mesh cannot guarantee recovery when the target is a pod not
managed by a controller (Chaos Mesh PodChaos page).

## Automated abort
Run a watcher that checks the steady-state metric during the experiment and deletes the chaos object
(or stops the run) on breach. Abort must not depend on a person noticing.

## Gotchas
- No steady-state metric, no experiment: you cannot tell whether anything happened.
- Do not run chaos during incidents or with an exhausted error budget.
- Inform on-call; experiments must not page people unexpectedly (or tag alerts).

## Verify
- [ ] Each experiment has a card, abort automation and recorded result.
- [ ] Refuted hypotheses produced tickets that were fixed and re-tested.

## Checked
2026-11-01. Confirmed in the Principles of Chaos Engineering page (steady state, hypothesis, real-world events, production, automation, blast radius) and the Chaos Mesh PodChaos page (`pod-kill`, `pod-failure`, `mode: one`, `duration`, `labelSelectors`, independent-pod caveat). Removed: NetworkChaos manifest values, thresholds and timings, the Prometheus watcher script, and the LitmusChaos, AWS FIS and Azure Chaos Studio statement.
Method: documentation only; no commands were run.
