---
id: computing-software.cloud-infrastructure-engineering.terraform.noisy-json-policy-diffs-and-normalisation
name: noisy-json-policy-diffs-and-normalisation
category: computing-software
field: cloud-infrastructure-engineering
product: terraform
tags: [terraform, opentofu, json-diff-noise, policy-diff-normalisation, jsonencode, iam-policy, perpetual-diff]
level: practitioner
status: docs-checked
description: "Stop perpetual or unreadable diffs on JSON policy attributes by building JSON with jsonencode or policy-document data sources and comparing plan before/after."
sources: ["https://developer.hashicorp.com/terraform/language/functions/jsonencode", "https://registry.terraform.io/providers/hashicorp/aws/latest/docs/data-sources/iam_policy_document", "https://developer.hashicorp.com/terraform/internals/json-format"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Noisy JSON policy diffs

## Symptoms
- Every plan shows a changed `policy` attribute with the same content reordered.
- A one-word change looks like the whole policy was replaced.
- Heredoc JSON with different whitespace than the API returns.

## Why
If your configuration produces JSON that is semantically equal to what the API
stores but textually different (whitespace, key order, string vs list), a provider
that does not treat equivalent JSON as equal shows a diff on every plan. Whether a
given resource suppresses equivalent JSON depends on the provider and resource; check
that resource's documentation.

## Fixes in order of preference
1. **Build the JSON with `jsonencode()`** from HCL objects rather than heredocs or
   template files. It produces a minified string, so whitespace never differs. Note
   it escapes `<`, `>` and `&` as `<`, `>`, `&` (and U+2028/U+2029),
   which JSON parsers treat as the same characters.
2. **Policy document data sources**: `aws_iam_policy_document` generates an IAM policy
   in JSON for resources that expect one, via its `.json` attribute. Using it is
   optional; literal JSON or `file()` are also valid.
3. **Match the API's form**: if the API returns a list for a single action, write a
   list.
4. **Round-trip** foreign JSON through `jsonencode(jsondecode(file("policy.json")))`
   to remove whitespace differences. Decoding then re-encoding does not preserve every
   Terraform type exactly, which rarely matters in practice.
5. Last resort: `lifecycle { ignore_changes = [policy] }`, only when the policy is
   managed elsewhere.

## Reading a big diff
Use the plan JSON, where each entry of `resource_changes` has `change.before` and
`change.after`:
```bash
terraform show -json tfplan | jq -r '.resource_changes[] | select(.address=="aws_sqs_queue.q") | .change.before.policy' > before.json
terraform show -json tfplan | jq -r '.resource_changes[] | select(.address=="aws_sqs_queue.q") | .change.after.policy' > after.json
diff <(jq -S . before.json) <(jq -S . after.json)
```
An empty sorted diff means the change is only formatting or key order.

## Verify
- [ ] Two consecutive plans after apply show `No changes`.
- [ ] Policies are built with `jsonencode` or policy-document data sources.

## Checked
2026-11-09. Confirmed against the Terraform `jsonencode` function page (minified output, Unicode escapes, type mapping, `jsondecode` round trip is not identical), the AWS provider `aws_iam_policy_document` data source page (JSON via `.json`, use is optional, `file()` valid) and the Terraform JSON output format page (`resource_changes`, `change.before`, `change.after`).
Removed as unconfirmed: the claim that the API returns canonicalised JSON with sorted keys, the list of services whose provider does not suppress equivalence (SQS, SNS, ECR, Kubernetes annotations), the claim that the AWS provider suppresses most IAM equivalence, the sample structural-diff output, and the original multi-step jq pipeline (replaced by a simpler one).
Method: documentation only; no commands were run.
