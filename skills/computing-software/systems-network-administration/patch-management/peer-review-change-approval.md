---
id: computing-software.systems-network-administration.patch-management.peer-review-change-approval
name: peer-review-change-approval
category: computing-software
field: systems-network-administration
product: patch-management
tags: [peer-review-approval, peer-review, devops-change, pull-request-approval, change-enablement, patch-management]
level: practitioner
status: draft
description: "Replace CAB approval with peer review for infrastructure and patch changes delivered as code: PR rules, required reviewers, automated evidence and audit traceability."
sources:
  - https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches
  - https://dora.dev/capabilities/streamlining-change-approval/
  - https://www.axelos.com/certifications/itil-service-management/itil-4-foundation
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Peer review approval in DevOps teams

DORA research found heavyweight external change approval (CAB) does not reduce change failure rates but slows delivery; peer review plus automated testing does better. ITIL 4 change enablement allows delegated change authorities.

## When it applies
Patch and config changes made through code: Ansible playbooks/inventories, Terraform (AMI IDs, node pool versions), Dockerfile base image bumps, GPO/baseline as code, Renovate PRs.

## Controls that make it auditable
- Protected branch: at least 1-2 approving reviews, **reviewer is not the author**, CODEOWNERS for sensitive paths (prod inventories, baselines), dismiss stale approvals on new commits.
- Required status checks: lint, tests (Molecule/Testinfra), plan output, image scan.
- Signed commits or verified authors.
- Merge triggers the pipeline; pipeline is the only path to production (no manual console changes).
```text
# CODEOWNERS
/inventories/prod/   @infra-leads
/baselines/          @security-engineering
```

## Linking to change management
- Pipeline auto-creates a standard change (or updates one) with PR link, approvers, test results, deployment time (ServiceNow DevOps Change Velocity, Jira integration).
- Change authority policy states which repos/paths are peer-review approved and which still need CAB (e.g. tier-1 DB major upgrades).

## Gotchas
- Rubber-stamp reviews (approve in 30 seconds on 2,000-line diffs) destroy the control; keep PRs small and measure review time.
- Emergency bypass (admin merge) must be logged and reviewed afterwards.
- Auditors will ask for evidence of segregation of duties: branch protection settings export and merge logs.

## Verify
Sample of production changes each traces to a PR with independent approval and passing checks; zero merges without review outside the documented emergency path.
