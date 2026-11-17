---
id: computing-software.cloud-infrastructure-engineering.cloud-architecture.environment-strategy
name: environment-strategy
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-architecture
tags: [cloud-architecture, landing-zone, environment-strategy, environment-separation, dev-test-prod, ephemeral-environments]
level: practitioner
status: draft
description: "Design environment separation: which environments, isolation boundary per environment, data rules, promotion path, and ephemeral preview environments."
sources: ["https://docs.aws.amazon.com/whitepapers/latest/organizing-your-aws-environment/organizing-workload-ous.html", "https://learn.microsoft.com/azure/cloud-adoption-framework/ready/landing-zone/design-area/resource-org-subscriptions", "https://cloud.google.com/architecture/security-foundations/organization-structure"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Environment separation strategy

## Steps
1. **Decide environments** by purpose: sandbox (experiments, no corporate connectivity),
   dev, test/staging (production-like), production; add performance or DR environments only
   when needed. Fewer long-lived environments are cheaper and less drift-prone.
2. **Isolation boundary**: separate account/subscription/project per workload per
   environment so IAM, quotas, network and cost are isolated; production in its own branch
   of the hierarchy with stricter policy.
3. **Network**: production and non-production in separate spokes; no routing between them
   unless explicitly required.
4. **Data rules**: no production personal data in non-production; masked or synthetic data;
   classification policy enforced.
5. **Access**: developers have broad rights in dev, read-only or JIT in production; deploy to
   production only via pipelines.
6. **Promotion**: the same artefact and IaC promoted through environments with
   environment-specific config only.
7. **Ephemeral environments** per pull request for app testing, with automatic teardown and TTL tags.
8. **Cost**: schedule non-production shutdown; budgets per environment.

## Gotchas
- Shared "dev" accounts for all teams become unmanageable and impossible to attribute.
- Staging that differs from production (smaller, different config) hides failures.

## Verify
- [ ] Production isolated by account/subscription with separate policies.
- [ ] Non-production data compliance checked.
