---
id: computing-software.cloud-infrastructure-engineering.terraform.aws-iam-policy-document-data-source
name: aws-iam-policy-document-data-source
category: computing-software
field: cloud-infrastructure-engineering
product: terraform
tags: [terraform, opentofu, iam-policy-document, aws-provider, iam-policy, data-sources, jsonencode]
level: practitioner
status: docs-checked
description: "Build IAM policies with aws_iam_policy_document: statements, conditions, principals, source and override documents for composition, and when jsonencode is better."
sources: ["https://raw.githubusercontent.com/hashicorp/terraform-provider-aws/main/website/docs/d/iam_policy_document.html.markdown", "https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_iam-quotas.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# `aws_iam_policy_document`

```hcl
data "aws_iam_policy_document" "bucket_read" {
  statement {
    sid       = "ReadLogs"
    effect    = "Allow"
    actions   = ["s3:GetObject", "s3:ListBucket"]
    resources = [aws_s3_bucket.logs.arn, "${aws_s3_bucket.logs.arn}/*"]
    condition {
      test     = "StringEquals"
      variable = "aws:PrincipalOrgID"
      values   = [var.org_id]
    }
  }
}
resource "aws_iam_policy" "bucket_read" {
  name   = "bucket-read"
  policy = data.aws_iam_policy_document.bucket_read.json
}
```

## Trust policies
```hcl
data "aws_iam_policy_document" "assume" {
  statement {
    actions = ["sts:AssumeRoleWithWebIdentity"]
    principals {
      type        = "Federated"
      identifiers = [aws_iam_openid_connect_provider.github.arn]
    }
    condition {
      test     = "StringLike"
      variable = "token.actions.githubusercontent.com:sub"
      values   = ["repo:corp/infra:ref:refs/heads/main"]
    }
  }
}
```
Principal `type` (required) values include `AWS`, `Service`, `Federated`, `CanonicalUser` and `*`.

## Composition
- `source_policy_documents = [a.json, b.json]`: merge statements; all documents must have unique Sids.
- `override_policy_documents = [c.json]`: statements with a matching Sid iteratively override earlier ones.
- Both can be combined in one document.
Use these to let module callers append statements (`var.extra_policy_json`).

## Why use it over `jsonencode`
- HCL lists for actions/resources instead of hand-written JSON.
- `not_actions`, `not_resources`, `not_principals` supported; `effect` defaults to `Allow`,
  `version` defaults to `2012-10-17`.
- Using the data source is optional; literal JSON or `file()` is also valid.

## When `jsonencode` is better
- Terraform may defer reading a data source to apply when an argument refers to a value it
  cannot predict at plan time, and values read from it are then computed in the plan.
- Non-IAM JSON policies (some services) with fields the data source does not model.

## Gotchas
- AWS policy variables (`${aws:username}`) clash with Terraform interpolation: write them
  as `&{aws:username}` in this data source.
- Size limits (IAM quotas page, whitespace not counted): customer managed policy 6,144
  characters; role inline policies 10,240 in aggregate per role; split large ones.

## Verify
- [ ] `terraform plan` twice shows no policy diffs.
- [ ] IAM Access Analyzer `validate-policy` passes on the rendered JSON.

## Checked
2026-10-31. Confirmed against the aws provider `aws_iam_policy_document` docs (raw GitHub; registry page is a stub), the Terraform data sources page and the IAM quotas page: source/override semantics, `&{...}` policy-variable notation, principal types, `effect`/`version` defaults, `not_*` arguments, 6,144 and 10,240 character limits, deferred reads. Removed: claims about canonical JSON, plan-time validation, statement order diffs and the quoting gotcha.
Method: documentation only; no commands were run.
