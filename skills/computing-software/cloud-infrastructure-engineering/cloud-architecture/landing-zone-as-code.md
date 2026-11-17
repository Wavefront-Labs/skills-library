---
id: computing-software.cloud-infrastructure-engineering.cloud-architecture.landing-zone-as-code
name: landing-zone-as-code
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-architecture
tags: [cloud-architecture, landing-zone, landing-zone-as-code, platform-automation, control-tower, terraform-landing-zone, alz]
level: advanced
status: draft
description: "Build and run the landing zone as code: accelerator choice, repository layout, pipelines with plan review, state, drift detection and safe upgrades."
sources: ["https://docs.aws.amazon.com/controltower/latest/userguide/aft-overview.html", "https://aka.ms/alz", "https://cloud.google.com/architecture/security-foundations", "https://docs.aws.amazon.com/solutions/latest/landing-zone-accelerator-on-aws/solution-overview.html"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Platform automation and landing-zone as code

## Accelerators
- AWS: Control Tower plus Account Factory for Terraform (AFT) or Customizations for Control
  Tower; Landing Zone Accelerator on AWS for regulated environments.
- Azure: Azure Landing Zones (ALZ) Terraform / Bicep modules and accelerator.
- Google Cloud: Security Foundations blueprint (terraform-example-foundation).

## Steps
1. **Repository layout** by lifecycle and blast radius: bootstrap (state, pipeline identity),
   organisation/policy, identity, networking, management/logging, account vending,
   per-workload baselines. Separate state per layer.
2. **Pipelines**: PR runs `plan` with policy checks (Checkov/OPA), mandatory human review of
   the plan, `apply` from main using workload identity federation (OIDC), no long-lived keys.
3. **State**: remote backend with locking and versioning, restricted access, encryption.
4. **Drift detection**: scheduled plan; alert on changes made outside code; restrict
   console write access to the platform layer.
5. **Upgrades**: pin accelerator module versions; test in a non-production organisation or
   management group copy; read release notes for breaking policy changes.
6. **Self-service**: workload teams request accounts through a PR or portal that triggers vending.

## Gotchas
- One giant state file for the whole landing zone makes every change risky and slow.
- Bootstrapping identity with a human admin key that never gets removed.

## Verify
- [ ] Zero manual changes detected in the last drift run.
- [ ] Pipeline identity uses federation; no static cloud keys in CI.
