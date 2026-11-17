---
id: computing-software.cloud-infrastructure-engineering.pulumi.policy-pack-enforcement
name: policy-pack-enforcement
category: computing-software
field: cloud-infrastructure-engineering
product: pulumi
tags: [cloud-infrastructure-engineering, pulumi, enforcement-level, mandatory-advisory, policy-groups, remediate]
level: practitioner
status: docs-checked
description: "Pulumi policy enforcement levels (advisory, mandatory, remediate, disabled), preventative vs audit policy groups, and default policy groups."
sources:
  - https://www.pulumi.com/docs/iac/crossguard/core-concepts/
  - https://www.pulumi.com/docs/iac/crossguard/configuration/
  - https://www.pulumi.com/docs/iac/crossguard/get-started/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Policy pack enforcement

**Enforcement level** is set per policy:
- `advisory`: reports a violation as a warning.
- `mandatory`: blocks the deployment.
- `remediate`: fixes the resource automatically.
- `disabled`: turns the policy off.

A policy group can override these levels for the packs it applies, so one pack can warn in one group and block in another.

**Enforcement mode** is chosen per policy group:
- Preventative groups evaluate IaC-managed resources during `pulumi preview` and `pulumi up` and can block a deployment (Terraform/OpenTofu stacks with Pulumi Cloud remote execution are evaluated against the plan before apply).
- Audit groups evaluate discovered cloud resources and the latest stack state and report violations without blocking, whatever the enforcement level. Audit policies need Pulumi Cloud (not available on a self-managed backend); violations appear in Policy Findings.

**Policy groups** (Pulumi Cloud, Essentials and above) apply packs to many stacks or accounts without passing `--policy-pack`; Pulumi downloads the packs. In the console: Governance > Policy configuration > Policy Groups > Create preventative (or audit) policy group; choose stacks/accounts (or Match by tags), select packs, and set Advisory or Mandatory per pack. Each organization has `default-policy-group` (preventative, all stacks) and `default-accounts-policy-group` (audit, all cloud accounts); new stacks and accounts join them automatically and there are limits on changing them.

Local `--policy-pack` runs (`pulumi preview --policy-pack <path>`, repeatable) use the pack's own enforcement levels.

## Gotchas
- Audit policies cannot block a change that already happened.
- A pack does nothing until it is in a policy group (or passed with `--policy-pack`).
- Publishing a new pack version enforces nothing new until the group references it (or tracks `latest`).

## Checked
2026-11-03. Confirmed on the Policy as code, Policy packs and Get started pages. Removed: the policy config JSON (`--policy-pack-config`), `remediateResource` code, `pulumi policy ls`/`group ls` commands, "remediation runs before validation" and "mandatory fails existing stacks" claims, and the Verify paragraph; none are on the pages read.
Method: documentation only; no commands were run.
