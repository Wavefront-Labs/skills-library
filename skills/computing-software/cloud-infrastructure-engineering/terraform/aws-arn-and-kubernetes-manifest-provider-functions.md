---
id: computing-software.cloud-infrastructure-engineering.terraform.aws-arn-and-kubernetes-manifest-provider-functions
name: aws-arn-and-kubernetes-manifest-provider-functions
category: computing-software
field: cloud-infrastructure-engineering
product: terraform
tags: [terraform, opentofu, provider-functions, arn-parse, arn-build, manifest-decode, manifest-encode, kubernetes-provider]
level: practitioner
status: docs-checked
description: "Use built-in provider functions: provider::aws::arn_parse/arn_build and provider::kubernetes::manifest_decode/_multi/encode, with signatures and the version requirement."
sources: ["https://registry.terraform.io/providers/hashicorp/aws/latest/docs/functions/arn_parse", "https://registry.terraform.io/providers/hashicorp/aws/latest/docs/functions/arn_build", "https://registry.terraform.io/providers/hashicorp/kubernetes/latest/docs/functions/manifest_decode", "https://github.com/hashicorp/terraform-provider-kubernetes/blob/main/docs/functions/manifest_decode_multi.md", "https://github.com/hashicorp/terraform-provider-kubernetes/blob/main/docs/functions/manifest_encode.md", "https://developer.hashicorp.com/terraform/language/functions#provider-defined-functions"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# AWS ARN and Kubernetes manifest provider functions

Provider-defined functions are called as `provider::<local-name>::<function>(...)`,
where `<local-name>` matches an entry in the `required_providers` block. The provider
function docs show configuration using them with a `required_providers` entry and
`required_version = ">= 1.8.0"` ("Provider functions require Terraform 1.8 and later").

## AWS ARNs
`arn_parse(arn string) object` parses an ARN into `partition`, `service`, `region`,
`account_id` and `resource`.
`arn_build(partition, service, region, account_id, resource) string` builds one; all five
arguments are strings. Supported partitions include `aws`, `aws-cn` and `aws-us-gov`.
```hcl
output "parsed" {
  # { partition = "aws", service = "iam", region = "", account_id = "444455556666", resource = "role/example" }
  value = provider::aws::arn_parse("arn:aws:iam::444455556666:role/example")
}

output "built" {
  # arn:aws:iam::444455556666:role/example
  value = provider::aws::arn_build("aws", "iam", "", "444455556666", "role/example")
}
```

## Kubernetes manifests
- `manifest_decode(manifest string) object`: given YAML text containing a Kubernetes
  manifest, returns an object that mirrors the structure of the YAML (a dynamic type).
- `manifest_decode_multi(manifest string) tuple`: for YAML text with multiple resources;
  returns a tuple of objects, one per resource.
- `manifest_encode(manifest object) string`: encodes an object representation of a
  manifest as a YAML string.
```hcl
terraform {
  required_providers {
    kubernetes = {
      source = "hashicorp/kubernetes"
    }
  }
  required_version = ">= 1.8.0"
}

locals {
  decoded = provider::kubernetes::manifest_decode(file("manifest.yaml"))
  bundle  = provider::kubernetes::manifest_decode_multi(file("manifest.yaml"))
}

output "encoded" {
  value = provider::kubernetes::manifest_encode({
    apiVersion = "v1"
    kind       = "ConfigMap"
    metadata   = { name = "example" }
    data       = { EXAMPLE = "example" }
  })
}
```
The provider docs recommend setting the provider `version` in `required_providers`.

## Checked
Date: 2026-11-07

Read in full: the AWS provider docs source for `arn_parse` and `arn_build` and the Kubernetes provider docs source for `manifest_decode`, `manifest_decode_multi` and `manifest_encode` (the registry pages render empty to a plain fetch, so I read the same docs files on GitHub), plus the top of the Terraform built-in functions page (the provider-defined functions section; its function tables were not read). No code tabs were present.

Trimmed as unconfirmed: "OpenTofu >= 1.7"; "Replaces `split(":", arn)[4]`, which breaks for resources containing colons"; `data.aws_partition` advice; the `kubernetes_manifest` resource examples and for_each key advice; "exactly one YAML document"; "keeps Kubernetes-friendly typing unlike `yamldecode`"; "kubernetes provider >= 2.29"; all three Gotchas (provider config not needed, plan-time unknowns, namespace keys); both Verify steps. Examples replaced with ones taken from the function docs. Added the two Kubernetes function doc files to `sources`.

Method: documentation only; no commands were run.
