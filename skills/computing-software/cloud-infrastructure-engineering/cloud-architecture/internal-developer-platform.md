---
id: computing-software.cloud-infrastructure-engineering.cloud-architecture.internal-developer-platform
name: internal-developer-platform
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-architecture
tags: [cloud-architecture, technology-architecture, internal-developer-platform, platform-engineering, backstage, golden-paths, self-service, developer-portal, cncf-platforms]
level: advanced
status: draft
description: "Architect an internal developer platform: golden paths, self-service APIs, portal, orchestration, platform-as-product practices and the metrics that show it helps."
sources: ["https://tag-app-delivery.cncf.io/whitepapers/platforms/", "https://backstage.io/docs/overview/what-is-backstage", "https://internaldeveloperplatform.org/what-is-an-internal-developer-platform/", "https://dora.dev/research/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Internal developer platform architecture

## Layers (CNCF Platforms white paper capabilities)
- **Interfaces**: developer portal (Backstage, Port), CLI, templates, APIs, GitOps repos.
- **Capabilities**: provisioning of infrastructure and environments, CI/CD, observability,
  identity/secrets, data services, messaging, security scanning, artefact storage.
- **Orchestration**: IaC modules + controllers (Crossplane, Terraform automation, Kubernetes
  operators) that turn requests into resources with guardrails.
- **Underlying clouds and clusters**.

## Design steps
1. Interview stream-aligned teams: top time sinks (env creation, pipeline setup, access requests).
2. Define 1-3 **golden paths** end to end (e.g. "new HTTP service on containers with Postgres"):
   template repo, pipeline, infra module, dashboards, alerts, runbook.
3. Expose through self-service with policy built in (tagging, encryption, network) - no tickets.
4. Treat the platform as a product: roadmap, product owner, user research, docs, SLOs.
5. Keep paths optional but attractive; allow escape with documented responsibilities.
6. Measure: DORA four keys for adopting teams, time to first deploy, onboarding NPS, % services on
   golden paths, ticket volume to platform team.

## Gotchas
- Building the portal first; the value is in the automated paths behind it.
- Mandating the platform before it is better than the alternative.
- Thick abstraction that hides cloud features teams genuinely need.

## Verify
- [ ] New service reaches production on the golden path in under a day.
- [ ] Adoption and DORA metrics reported quarterly.
