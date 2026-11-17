---
id: computing-software.cloud-infrastructure-engineering.terraform.iam-propagation-delays-and-retries
name: iam-propagation-delays-and-retries
category: computing-software
field: cloud-infrastructure-engineering
product: terraform
tags: [terraform, opentofu, iam-propagation, eventual-consistency, time-sleep, aws-provider, hidden-dependency]
level: practitioner
status: docs-checked
description: "Handle IAM and RBAC propagation delays that break the first apply: provider retries, time_sleep after role and policy creation, and role-assignment waits on Azure and GCP."
sources: ["https://docs.aws.amazon.com/IAM/latest/UserGuide/troubleshoot_general.html#troubleshoot_general_eventual-consistency", "https://registry.terraform.io/providers/hashicorp/time/latest/docs/resources/sleep", "https://learn.microsoft.com/en-us/azure/role-based-access-control/troubleshooting"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# IAM propagation delays

## Symptoms (first apply fails, re-run succeeds)
- AWS: access or assume-role failures right after creating or changing a role, user, group
  or policy. AWS says IAM uses eventual consistency: changes take time to become visible from
  all endpoints (server-to-server and Region-to-Region replication, plus caching).
- Azure: role assignments and removals can take up to 10 minutes to take effect
  (Azure RBAC troubleshooting). A just-created principal can hit a replication delay
  ("Principal ... does not exist in the directory"): set the role assignment's `principalType`
  (for example `ServicePrincipal`).

AWS recommends keeping IAM changes out of critical code paths and verifying propagation
before production workflows depend on them.

## Options
1. **Prefer fixes in the provider** first. HashiCorp's `time_sleep` docs call it a
   workaround: downstream resources can usually add retries, or upstream resources can wait
   until a resource is ready. Upgrade the provider and report the gap before adding sleeps.
2. **Explicit dependency on the attachment, not just the role**:
```hcl
resource "aws_lambda_function" "f" {
  role       = aws_iam_role.f.arn
  depends_on = [aws_iam_role_policy_attachment.f_logs]   # policy attached before create
}
```
3. **time_sleep** for services without retries:
```hcl
resource "time_sleep" "iam" {
  depends_on      = [aws_iam_role_policy_attachment.f_logs]
  create_duration = "30s"
  triggers = { policy = aws_iam_role_policy_attachment.f_logs.policy_arn }
}
resource "aws_lambda_function" "f" {
  role       = aws_iam_role.f.arn
  depends_on = [time_sleep.iam]
}
```
   `triggers` re-runs the delay when its values change; changing `create_duration` alone does
   not (`destroy_duration` delays destroys the same way).
4. **Azure**: for a newly created principal set the role assignment's `principalType`
   (check the azurerm `azurerm_role_assignment` docs for the argument name); otherwise a
   `time_sleep` sized to the up-to-10-minute RBAC propagation window.
5. **Split stacks**: identity in one stack applied earlier; consumers in another.

## Gotchas
- Sleeps slow every create of that resource; keep durations minimal and scoped.

## Verify
- [ ] Fresh environment build succeeds on the first apply, three times in a row.

## Checked
- 2026-10-28. Confirmed against the AWS IAM troubleshooting page ("Changes that I make are not always immediately visible": eventual consistency, caching, design advice), the Azure RBAC troubleshooting page (role assignment changes take up to 10 minutes; `principalType` for new principals) and the `time` provider's `time_sleep` docs (`create_duration`, `destroy_duration`, `triggers`, workaround note).
- Removed: named AWS error messages, the GCP symptom and its timings, the EKS node group symptom, the provider-retry claim, the `skip_service_principal_aad_check` argument, the 60-120s Azure sleep and the data-source `depends_on` claim (not in the fetched docs).
Method: documentation only; no commands were run.
