---
id: computing-software.cloud-infrastructure-engineering.cloud-architecture.health-model
name: health-model
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-architecture
tags: [cloud-architecture, health-model, health-modelling, slis, slos, traffic-light-dashboard, dependency-rollup]
level: practitioner
status: docs-checked
description: "Build a workload health model: flows and components as entities, Healthy/Degraded/Unhealthy states from SLI signals, dependency roll-up rules and traffic-light views."
sources: ["https://learn.microsoft.com/azure/well-architected/design-guides/health-modeling", "https://learn.microsoft.com/azure/well-architected/reliability/metrics", "https://docs.aws.amazon.com/wellarchitected/latest/reliability-pillar/monitor-workload-resources.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Workload health model

## Steps
1. **Start from user and system flows**, then roll up each flow's health from its components. Components get their state
   from signals. A model has tiers such as application, flows, components and platform resources.
2. **Define three states** (Azure health modelling guide): Healthy (meets quality expectations), Degraded (less than
   healthy, potential problems; still operational) and Unhealthy (critical, needs immediate attention).
3. **Choose signals** that show whether an entity delivers its expected outcome. Start with a few per entity and drop
   those that do not improve the model. Define SLIs and SLOs aligned with the signals; SLIs and SLOs are critical
   health signals. Give each signal Degraded and Unhealthy thresholds based on the workload's nonfunctional requirements.
   Fixed thresholds can fail under changing load, so choose thresholds that reflect the normal pattern.
4. **Roll up** to parents. In Azure Monitor health models, impact settings control how a child affects its parent:
   Standard passes the state unchanged; Limited ignores a Degraded child and passes Unhealthy as Degraded (fits
   a dependency with a fallback); Suppressed passes none. Dependency settings combine children: Worst of, or
   count-based limits for redundant components such as regional deployments.
5. **Redundancy**: for three regions, the Azure guide suggests a flow may be Degraded when one region fails (lost
   redundancy) and Unhealthy when the remaining regions cannot carry the load. For active-passive, track standby
   readiness separately from current availability.
6. **Visualise** as a traffic-light tree: green healthy, amber degraded, red unhealthy, with state names included so
   colour is not the only cue.
7. **Alert** when an entity changes to Degraded or Unhealthy.
8. **Maintain**: manage the model as code, and review signals, thresholds and dependencies when the workload changes.

## Gotchas
- Health depends on context; what is healthy in one scenario may not be in another.
- A dependency with a working fallback (cache to database) should make the parent Degraded, not Unhealthy.
- Monitoring must detect "silent" failures, where functionality is gone but only indirect signs exist (AWS).
- Thresholds that suit steady load fail under daily or seasonal change.

## Verify
- [ ] A failed dependency changes the expected flow state, and alerts fire on the transition.
- [ ] Thresholds and signals are reviewed after incidents and workload changes.

## Checked
2026-11-08. Confirmed against the Azure Well-Architected health modelling guide (states, flows, SLIs and SLOs, threshold
guidance, fallback and redundancy examples, traffic-light visualisation, Azure Monitor health model impact and
dependency settings) and the AWS Reliability pillar monitoring page (silent failures, alerting decoupled from systems).
The Azure reliability targets page (availability objectives, recovery metrics) was read for headings only and supplies
no figure used here. Removed: the invented 0.1% error and 300 ms thresholds, error-budget burn definition, worst-of versus
weighted roll-up rule and the "within minutes" test.
Method: documentation only; no commands were run.
