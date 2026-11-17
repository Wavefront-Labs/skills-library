---
id: computing-software.cloud-infrastructure-engineering.cloud-architecture.chaos-engineering
name: chaos-engineering
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-architecture
tags: [cloud-architecture, resilience-testing, chaos-engineering, fault-injection, aws-fis, azure-chaos-studio, chaos-mesh, steady-state-hypothesis, blast-radius, stop-conditions]
level: advanced
status: docs-checked
description: "Run chaos experiments safely: steady-state hypothesis, realistic faults, AWS FIS stop conditions, Azure Chaos Studio and Chaos Mesh, minimising blast radius."
sources: ["https://principlesofchaos.org/", "https://docs.aws.amazon.com/fis/latest/userguide/what-is.html", "https://learn.microsoft.com/azure/chaos-studio/chaos-studio-overview", "https://chaos-mesh.org/docs/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Chaos engineering experiments

## Experiment design (Principles of Chaos)
1. **Steady state**: build the hypothesis around measurable output (throughput, error rates,
   latency percentiles), not internal attributes.
2. **Vary real-world events**: hardware failures, malformed responses, traffic spikes; rank by likely
   impact or frequency.
3. **Production**: the principles prefer experimenting on production traffic, because usage patterns
   and environments shift. AWS FIS advises a planning phase and a pre-production run first, since it
   performs real actions on real resources.
4. **Minimise blast radius**: accept only short-term, contained customer impact.
5. **Automate** experiments and run them continuously.
6. **Stop conditions**: define abort thresholds before running.

## Tooling
- **AWS Fault Injection Service**: an experiment template holds actions, targets and stop
  conditions. Actions are preconfigured per resource type and run for a set duration, sequentially or
  in parallel. Targets are chosen explicitly or by criteria such as tags or state. A stop condition
  is a CloudWatch alarm; if it fires the experiment is stopped. Single-account experiments target
  resources in the same account; multi-account experiments are supported separately. Charged per
  minute an action runs (see the FIS pricing page).
- **Azure Chaos Studio**: Workspaces and Scenarios (current model, public preview and not for
  production use at the time of reading) simulate outages such as Compute Zone Down or DNS Outage and
  produce a Scenario report. Experiments (classic) support service-direct faults (e.g. VM shutdown,
  SQL Database failover, Redis flush) and agent-based faults (CPU pressure, memory pressure, process
  kills) in steps, branches and actions. Listed uses: incident reproduction, game days against
  preproduction, business continuity testing, CI/CD deployment gates, compliance evidence.
- **Chaos Mesh**: open source, CNCF incubating, Kubernetes custom resources per fault type;
  Dashboard, Controller Manager and a privileged Chaos Daemon DaemonSet; also targets cloud APIs
  (AWS, Azure, GCP) and physical machines.

## Practice
Review recorded results with application monitoring, fix, rerun. Tell on-call before production
experiments.

## Verify
- [ ] Every experiment has a measurable steady-state hypothesis and an abort condition.
- [ ] Findings are tracked to fixes.

## Checked
Confirmed against the four cited pages. Removed as not stated there: specific FIS action ids, the AZ
power interruption scenario, NSG/Cosmos DB/AKS fault examples, LitmusChaos, Envoy fault filter,
the worked numeric hypothesis, and the quarterly cadence.
Method: docs-only read of cited pages, 2026-11-08
