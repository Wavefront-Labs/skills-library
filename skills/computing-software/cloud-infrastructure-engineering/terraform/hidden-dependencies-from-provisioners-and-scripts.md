---
id: computing-software.cloud-infrastructure-engineering.terraform.hidden-dependencies-from-provisioners-and-scripts
name: hidden-dependencies-from-provisioners-and-scripts
category: computing-software
field: cloud-infrastructure-engineering
product: terraform
tags: [terraform, opentofu, hidden-dependency, hidden-dependencies, depends-on, eventual-consistency, race-condition, provisioners]
level: advanced
status: docs-checked
description: "Find and fix ordering bugs Terraform cannot see: scripts, provisioners, IAM propagation and API side effects, preferring references, with depends_on as a last resort."
sources: ["https://developer.hashicorp.com/terraform/language/meta-arguments/depends_on", "https://developer.hashicorp.com/terraform/cli/commands/plan"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Hidden dependencies

Terraform infers ordering from references between resources; `depends_on` handles hidden
dependencies it cannot infer, where one resource relies on another's behaviour without
using its data. Anything else is invisible and may run in parallel. Symptoms: works on the
second apply, fails on greenfield, intermittent `AccessDenied`/`NotFound` right after creation.

## Common hidden dependencies
| Hidden link | Example | Fix |
|---|---|---|
| Script reads a resource by name | `local-exec` calls `aws s3 cp` to a bucket | reference it in the command: `command = "aws s3 cp f s3://${aws_s3_bucket.b.bucket}/"` |
| Permission needed by a later resource | Function created before its role policy attaches | `depends_on = [aws_iam_role_policy_attachment.x]` on the function |
| IAM/eventual consistency | role exists but the cloud cannot use it yet | an explicit wait or retry as a last resort (check the provider's docs for built-in retries first) |

## Prefer references
The docs say to use `depends_on` only as a last resort: it can make plans more
conservative, with more values "(known after apply)" and more resources replaced, which is
especially likely for modules. Expression references let Terraform see which value
derives from which and avoid planning changes when that value is unchanged. The
`depends_on` list takes references to resources or child modules in the same calling
module, not arbitrary expressions.

## Finding them
- Greenfield test: apply into an empty account/project in CI; hidden dependencies fail there first.
- `terraform apply -parallelism=1` passes but the default fails: a race exists (`-parallelism` limits concurrent operations; default 10).
- `terraform graph` and look for an edge between the two resources; no edge means no ordering.

## Gotchas
- Put `depends_on` on the resource that needs the dependency (the one declaring it
  waits for all actions on the dependency, including reads).

## Verify
- [ ] Greenfield apply in a scratch environment succeeds on the first run.
- [ ] `terraform graph` shows an edge for each dependency you added.

## Checked
Date: 2026-10-28.
Confirmed in the depends_on reference: purpose (hidden dependencies), last-resort guidance and its plan side effects, preference for expression references, list-of-references restriction, completes all actions on the dependency including reads. Confirmed in the plan command page: `-parallelism` default 10.
Removed as unconfirmed: `time_sleep` arguments and the 15s example (registry page unreadable), EKS aws-auth and ACM validation rows, provider-native waiter claims, TF_LOG timestamp tip, destroy-order gotcha.
Method: documentation only; no commands were run.
