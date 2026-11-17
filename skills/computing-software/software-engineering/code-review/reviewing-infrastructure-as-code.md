---
id: computing-software.software-engineering.code-review.reviewing-infrastructure-as-code
name: reviewing-infrastructure-as-code
category: computing-software
field: software-engineering
product: code-review
tags: [code-review, iac-review, terraform, kubernetes, policy-as-code, blast-radius]
level: advanced
status: draft
description: "Review infrastructure-as-code changes: read the plan not just the diff, check destroys and replacements, security groups, IAM, state and blast radius, with policy tools in CI."
sources: ["https://developer.hashicorp.com/terraform/cli/commands/plan", "https://www.checkov.io/", "https://www.openpolicyagent.org/docs/latest/terraform/", "https://kubernetes.io/docs/reference/kubectl/generated/kubectl_diff/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Reviewing infrastructure-as-code changes

## Review the plan, not only the code
A one-line diff can destroy a database. Require the **plan output** on the PR (Atlantis, Terraform
Cloud, Spacelift, `tfcmt`, or a CI job posting `terraform plan`).
- Look for `-/+ destroy and then create replacement` and `# forces replacement` on stateful resources
  (databases, volumes, buckets, DNS zones, load balancers with fixed IPs). Ask why.
- Count: `Plan: 3 to add, 1 to change, 0 to destroy`; any destroy needs explicit justification.
- `moved {}` / `terraform state mv` used for refactors so resources aren't recreated.
- Kubernetes: `kubectl diff -k overlays/prod` or Argo CD/Flux diff; Helm `helm diff upgrade`.

## Checklist
- **Security**: `0.0.0.0/0` ingress, public buckets/ACLs, IAM `*` actions/resources, wildcard
  principals, disabled encryption, secrets in variables/state/plain manifests.
- **Blast radius**: which environments/accounts/regions does this touch? Shared modules change every
  consumer: check module version pinning.
- **Protection**: `prevent_destroy`, deletion protection, backups/PITR, versioning on buckets.
- **State**: backend changes, workspace correctness, no local state, state locking intact.
- **Drift and ordering**: depends_on, provider version bumps (read provider changelogs for
  behaviour changes), data sources that resolve differently per environment.
- **Cost**: instance sizes, NAT gateways, cross-AZ traffic, log retention (Infracost comment).
- **Kubernetes**: resource requests/limits, probes, PodDisruptionBudget, securityContext
  (non-root, read-only FS), image tags pinned by digest, RBAC scope.
- **Rollout**: apply order across environments, maintenance window, rollback plan.

## Automate the routine checks
`terraform fmt -check`, `terraform validate`, `tflint`, Checkov/Trivy (tfsec)/KICS for misconfig,
OPA Conftest or Sentinel policies on the plan JSON (`terraform show -json plan.out`), Infracost
for cost deltas, kube-linter/kubeconform/Polaris for manifests. Humans review intent and risk.
