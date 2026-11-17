---
id: computing-software.devops-ci-cd.ci-pipeline-design.chaos-and-resilience-tests-in-pipeline
name: chaos-and-resilience-tests-in-pipeline
category: computing-software
field: devops-ci-cd
product: ci-pipeline-design
tags: [ci-pipeline-design, chaos-testing, nonfunctional-testing, resilience-testing]
level: advanced
status: docs-checked
description: "Run resilience and chaos experiments in the delivery pipeline with a steady-state hypothesis, limited blast radius and pass criteria; Chaos Mesh PodChaos example."
sources: ["https://principlesofchaos.org/", "https://chaos-mesh.org/docs/", "https://raw.githubusercontent.com/chaos-mesh/website/master/docs/simulate-pod-chaos-on-kubernetes.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Resilience and chaos tests in the pipeline

Chaos engineering is the discipline of experimenting on a system to build confidence in its
ability to withstand turbulent conditions. Systemic weaknesses the Principles of Chaos name
include improper fallback settings when a service is unavailable, retry storms from badly tuned
timeouts, outages when a downstream dependency gets too much traffic, and cascading failures
from a single point of failure.

## Experiment steps (Principles of Chaos)
1. Define "steady state" as a measurable output indicating normal behaviour (throughput,
   error rates, latency percentiles).
2. Hypothesise that steady state continues in both the control and the experimental group.
3. Introduce variables that reflect real-world events: servers that crash, hard drives that
   malfunction, severed network connections, malformed responses, traffic spikes or scaling
   events.
4. Try to disprove the hypothesis by looking for a difference in steady state between the
   groups. The harder it is to disrupt steady state, the more confidence you have.

Advanced principles: focus on measurable system output rather than internals; vary
real-world events and prioritise by impact or frequency; prefer experiments in production
(the principles say so, but a pipeline stage normally runs in a test environment); automate
experiments and run them continuously; **minimise blast radius** and keep fallout contained.

## Chaos Mesh in a pipeline stage
Chaos Mesh is a CNCF incubating, Kubernetes-native chaos platform built on CRDs; experiments
are applied as custom resources (for example with `kubectl apply -f`). A PodChaos experiment
needs `action` (`pod-failure`, `pod-kill` or `container-kill`), `mode`, a `selector` and a
`duration`:
```yaml
apiVersion: chaos-mesh.org/v1alpha1
kind: PodChaos
metadata:
  name: pod-kill-example
  namespace: <namespace>
spec:
  action: pod-kill
  mode: one            # one random pod; also all, fixed, fixed-percent, random-max-percent
  duration: '30s'
  selector:
    namespaces: [<namespace>]
    labelSelectors:
      'app': '<label>'
```
Per the PodChaos reference, `mode: one` selects a random pod, `value` supplies the parameter
for modes such as `fixed-percent`, and `gracePeriod` sets the grace period before deletion
for `pod-kill`. Injecting pod-kill into a standalone pod (not managed by a Deployment,
StatefulSet, DaemonSet or similar controller) gives no guarantee the application recovers.
The `selector` and `duration` fields bound the blast radius.

A pipeline use (judgement, not from the sources): run the experiment while a load test runs,
and pass if the steady-state metrics (for example the load tool's thresholds) hold.

## Rules
- Write the hypothesis and steady-state metric first.
- Bound blast radius (namespace, one pod, short duration) and stop experiments on harm.
- Treat a failed experiment as a resilience bug, not a flaky test.

## Checked
Confirmed 2026-11-09 against principlesofchaos.org (full page) and the Chaos Mesh docs overview (architecture and CRD basis) plus the PodChaos page on GitHub (actions, modes, fields, standalone-pod caveat; keyword search). The corrected example adds the required `duration`, which the draft omitted.
Removed as unconfirmed: Toxiproxy commands and the latency example, LitmusChaos, AWS FIS stop conditions, Azure Chaos Studio, Gremlin, WireMock and Testcontainers fault claims, the "error rate under 1%" target and the three-level table.
Method: docs-checked 2026-11-09 against principlesofchaos.org, chaos-mesh.org/docs and the Chaos Mesh PodChaos documentation source
