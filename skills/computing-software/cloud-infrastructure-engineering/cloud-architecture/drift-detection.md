---
id: computing-software.cloud-infrastructure-engineering.cloud-architecture.drift-detection
name: drift-detection
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-architecture
tags: [cloud-architecture, management-and-monitoring, drift-detection, configuration-drift, terraform-plan-drift, cloudformation-drift, aws-config, desired-state]
level: practitioner
status: draft
description: "Detect and handle configuration drift between IaC and live cloud resources: scheduled plans, provider drift tools, policy-based detection, and a remediate-or-import process."
sources: ["https://developer.hashicorp.com/terraform/tutorials/state/resource-drift", "https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-stack-drift.html", "https://learn.microsoft.com/azure/azure-resource-manager/bicep/deploy-what-if"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Configuration drift detection

## Detection methods
1. **Scheduled IaC plans**: nightly `terraform plan -detailed-exitcode` per stack (exit 2 = changes)
   in CI; HCP Terraform health assessments; `terraform plan -refresh-only` to see drift only.
2. **Provider tools**: CloudFormation drift detection (`aws cloudformation detect-stack-drift`),
   Bicep/ARM `what-if`, Pulumi `refresh --preview-only`.
3. **Change events**: CloudTrail / Activity Log events for writes by humans (console sessions)
   on IaC-managed resources -> alert.
4. **Policy/compliance** (AWS Config, Azure Policy) for properties that must never drift.
5. **GitOps** controllers (Argo CD, Flux) show drift and can self-heal Kubernetes objects.

## Handling drift
- Emergency hotfix in console -> **codify** it (update IaC, or `terraform import`/`import` blocks).
- Unauthorised change -> **revert** by applying IaC, investigate.
- Provider-side defaults that differ (noise) -> `lifecycle { ignore_changes = [...] }` sparingly
  with a comment.

## Prevention
Read-only console access in production; break-glass for emergencies; all changes via pipelines.

## Gotchas
- Plans that always show diffs train people to ignore drift reports; fix noisy diffs.
- `ignore_changes` used broadly hides real drift.

## Verify
- [ ] Nightly drift report per stack; zero unexplained drift older than a week.
- [ ] Console write events in production alert the owning team.
