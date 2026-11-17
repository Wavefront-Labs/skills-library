---
id: computing-software.cloud-infrastructure-engineering.cloud-architecture.single-point-of-failure
name: single-point-of-failure
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-architecture
tags: [cloud-architecture, reliability-foundations, single-point-of-failure, spof-analysis, dependency-review, shared-fate, hidden-dependencies]
level: practitioner
status: docs-checked
description: "Hunt single points of failure with failure mode analysis: decompose critical flows, classify internal and external dependencies as strong or weak, and plan mitigations."
sources: ["https://learn.microsoft.com/azure/well-architected/reliability/failure-mode-analysis"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Single point of failure analysis

Follows the Azure Well-Architected failure mode analysis (FMA) guidance, recommendation RE:03:
identify potential failures, dependencies and failure points, and develop mitigations. A key tenet
is that failures happen however many layers of resiliency you apply, and more complex
environments are exposed to more types of failures.

## Procedure
1. **Identify and prioritise flows** by criticality first; FMA assumes this is done.
2. **Decompose the workload**: plan for ingress control, networking, compute, data, storage,
   supporting services (authentication, messaging, secret or key management) and egress control.
   Overlay the flows to find the components each flow uses, using the flow's criticality.
3. **Identify dependencies**, including those to third parties:
   - Internal: in the workload scope, for example APIs or secret and key management. Capture
     reliability data such as availability SLAs and scaling limits.
   - External: outside the workload scope, for example another application, authentication
     (Entra ID) or cloud connectivity (ExpressRoute).
4. **Evaluate failure points**. For each component in a critical flow, consider the failure modes
   the page lists: regional outage, availability zone outage, service outage, DDoS or other
   attack, misconfiguration, operator error, planned maintenance and component overload. Treat
   read and write failures separately. Record the effect on the user and on the flow (for
   example, no customer can complete checkout).
5. **Rate likelihood**: for very unlikely modes such as multizone or multiregion outages, the page
   says mitigation planning beyond redundancy is not a good use of time.
6. **Plan mitigations** in two categories: build more resilience (redundancy, isolated
   components) or design for degraded performance (the flow continues without a failed
   component, such as a recommendation service).
7. **Classify dependencies as strong or weak**. Strong dependencies the app cannot run without
   should have availability and recovery targets aligned with the app's own; minimise
   dependencies to keep control of reliability.
8. **Implement failure detection**: monitoring and alerting, automated where possible, with
   redundancy in the operations process so alerts are always caught.
9. **Document and revisit**: record findings, decisions and effects, prioritised by severity and
   likelihood, and review regularly; chaos testing and real incidents refine them.

## Gotchas
- A failure is an unexpected event that needs intervention or specific design; an error is an
  expected part of normal operation handled immediately (the page's distinction).
- Closely coupling the app's lifecycle to a dependency's can limit operational agility,
  particularly for releases.
- An incomplete analysis leaves the workload exposed to unpredicted behaviour and outages.

## Verify
- [ ] Every critical flow has its components and dependencies listed.
- [ ] Each component has a documented effect per failure mode, with a mitigation or accepted risk.
- [ ] Strong dependencies have targets that match the application's.

## Checked
2026-11-08. Confirmed against the Azure Well-Architected "failure mode analysis" page (RE:03,
decomposition, internal and external dependencies, listed failure modes, mitigation categories,
strong vs weak dependencies, detection, documentation and review). Removed the claims not stated
in any readable source: the list of hidden SPOF types (certificates, one-person knowledge,
logging pipelines), 30-day expiry alerts and quarterly review. The AWS reliability pillar index
page (no content on the topic) and the long Google SRE cascading-failures chapter were not relied
on and are dropped from sources.
Method: documentation only; no commands were run.
