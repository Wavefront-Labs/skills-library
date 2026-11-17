---
id: computing-software.cloud-infrastructure-engineering.terraform.jsonencode-yamldecode-and-policy-documents
name: jsonencode-yamldecode-and-policy-documents
category: computing-software
field: cloud-infrastructure-engineering
product: terraform
tags: [terraform, opentofu, encoding-functions, jsonencode, jsondecode, yamldecode, base64encode, policy-template, json-template, iam-policy]
level: practitioner
status: verified
description: "Produce and consume JSON/YAML with jsonencode, jsondecode, yamldecode/yamlencode and base64 functions; render IAM-style policy documents without whitespace diffs."
sources: ["https://developer.hashicorp.com/terraform/language/functions/jsonencode", "https://developer.hashicorp.com/terraform/language/functions/yamldecode", "https://developer.hashicorp.com/terraform/language/functions/templatefile#generating-json-or-yaml-from-a-template", "https://registry.terraform.io/providers/hashicorp/aws/latest/docs/data-sources/iam_policy_document"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Encoding functions and policy documents

## jsonencode for policies (not heredoc JSON)
```hcl
resource "aws_iam_policy" "read_bucket" {
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect   = "Allow"
      Action   = ["s3:GetObject", "s3:ListBucket"]
      Resource = [aws_s3_bucket.data.arn, "${aws_s3_bucket.data.arn}/*"]
    }]
  })
}
```
Heredoc JSON breaks on trailing commas, quoting and interpolation; `jsonencode` is
always valid. For AWS, `data "aws_iam_policy_document"` is the other good option
(merging via `source_policy_documents`).

## templatefile producing JSON
Templates that build JSON by string concatenation are fragile. Instead, make the
whole template a single `jsonencode` call:
```
${jsonencode({
  "Statement" : [for b in buckets : {
    "Effect" : "Allow",
    "Action" : "s3:GetObject",
    "Resource" : "arn:aws:s3:::${b}/*"
  }]
})}
```
`policy = templatefile("${path.module}/policy.json.tftpl", { buckets = var.buckets })`. The rendered text ends with a newline after the JSON (checked); that is harmless to JSON parsers.

## Decoding
```hcl
locals {
  cfg      = yamldecode(file("${path.module}/config/${var.env}.yaml"))
  services = jsondecode(data.http.catalog.response_body).services
}
```
- `yamldecode` supports one document: a file with `---` between documents fails ("unexpected extra content after value"). Split first (`[for d in split("\n---\n", file("multi.yaml")) : yamldecode(d)]` worked), or use the kubernetes provider's `manifest_decode_multi` function (provider docs).
- YAML anchors, aliases and `<<` merge keys all decoded correctly in a test (`derived: {<<: *b, y: 3}` merged the base keys and overrode `y`). YAML 1.1 booleans bite: unquoted keys/values `y`, `n`, `yes`, `on` decode as booleans (`yamldecode("c: y")` gives `c = true`, and a key `y` becomes `"true"`), so quote them.

## Other encoders
`base64encode/decode`, `base64gzip` (user data), `urlencode` (`urlencode("a b/c")` is `a+b%2Fc`), `csvdecode` (list of
maps from CSV with every value a string, so ports arrive as `"80"`; handy for bulk inputs), `textencodebase64(s, "UTF-16LE")` (Windows; `textencodebase64("hi","UTF-16LE")` is `aABpAA==`),
`yamlencode` (Kubernetes manifests, cloud-init; keys are quoted in the output).

## Perpetual diffs
Providers often normalise JSON (key order, whitespace, single vs list values). If a
policy shows changes every plan: ensure `Action`/`Resource` forms match what the API
returns, or use the provider's policy-document data source; some resources apply
semantic-equality suppression, others do not.

## Verify
- [ ] `terraform console` → `jsondecode(aws_iam_policy.read_bucket.policy)` round-trips.
- [ ] Two consecutive plans show no policy diffs.
