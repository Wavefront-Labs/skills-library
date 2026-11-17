---
id: computing-software.cloud-infrastructure-engineering.cloud-architecture.service-model-selection
name: service-model-selection
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-architecture
tags: [cloud-architecture, service-models, iaas-paas-saas, service-model-selection, nist-sp-800-145, platform-selection, control-vs-responsibility, buy-vs-build]
level: practitioner
status: draft
description: "Choose IaaS, CaaS, PaaS, FaaS or SaaS per workload: decision criteria (control, ops burden, portability, compliance, cost shape, skills) and a scored comparison you can defend."
sources: ["https://csrc.nist.gov/pubs/sp/800/145/final", "https://learn.microsoft.com/azure/architecture/guide/technology-choices/compute-decision-tree", "https://cloud.google.com/architecture/framework"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Choosing the service model per workload

NIST SP 800-145 defines SaaS, PaaS and IaaS by **what the consumer controls**. Containers (CaaS)
and functions (FaaS) sit between IaaS and PaaS in practice.

## Default ladder (stop at the first that fits)
1. **SaaS** — is this a commodity capability (email, CRM, ticketing, identity)? Buy it.
2. **FaaS / serverless PaaS** — event-driven or spiky, short-running, stateless.
3. **PaaS / managed containers** (App Service, Cloud Run, Container Apps, ECS Fargate, Elastic Beanstalk) —
   standard web/API/worker apps.
4. **Managed Kubernetes (CaaS)** — many services, platform team exists, need for portability/ecosystem.
5. **IaaS VMs** — legacy/COTS needing OS control, special licensing, kernel/agent requirements.

## Criteria to score (1-5 each, weight per context)
- Control needed (OS, network, runtime versions)
- Operational burden the team can carry (patching, scaling, HA)
- Time to market
- Portability / lock-in tolerance
- Compliance constraints (data location, certifications of the service)
- Cost shape (steady vs spiky; per-request vs per-hour)
- Skills available
- Limits (timeouts, payload sizes, cold starts, max instances)

## Steps
1. Write the workload profile (traffic pattern, state, runtime, dependencies, SLO).
2. Score 2-3 candidate models; record in an ADR with the rejected options and why.
3. Validate limits with a spike/prototype before committing.

## Gotchas
- Choosing Kubernetes by default for one small app — platform cost dominates.
- PaaS hard limits discovered late (request timeouts, max memory, outbound IP restrictions).

## Verify
- [ ] ADR exists with scored criteria and limits checked.
