---
id: computing-software.cloud-infrastructure-engineering.terraform.multi-region-and-cross-account-provider-aliases
name: multi-region-and-cross-account-provider-aliases
category: computing-software
field: cloud-infrastructure-engineering
product: terraform
tags: [terraform, opentofu, region-alias, multi-region-replication, account-alias, cross-account-provider, assume-role, provider-alias]
level: advanced
status: docs-checked
description: "Use aliased providers for multi-region replication and cross-account resources (assume_role per alias), pass them to modules, and keep state ownership sane."
sources:
  - https://developer.hashicorp.com/terraform/language/providers/configuration
  - https://github.com/hashicorp/terraform-provider-aws/blob/main/website/docs/index.html.markdown
  - https://github.com/hashicorp/terraform-provider-aws/blob/main/website/docs/guides/enhanced-region-support.html.markdown
  - https://github.com/hashicorp/terraform-provider-aws/blob/main/website/docs/r/s3_bucket_replication_configuration.html.markdown
  - https://github.com/opentofu/opentofu/blob/main/website/docs/language/providers/configuration.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Multi-region and cross-account aliases

## Region aliases (replication)
A second `provider` block for the same provider with an `alias` gives a separate configuration. The block without an alias is the default; resources select an alias with `provider = aws.<alias>`. If every block uses an alias, Terraform creates an empty implied default, which fails for providers that need arguments.
```hcl
provider "aws" { region = "eu-west-1" }
provider "aws" {
  alias  = "dr"
  region = "eu-central-1"
}

resource "aws_s3_bucket" "primary" { bucket = "acme-data-euw1" }
resource "aws_s3_bucket" "replica" {
  provider = aws.dr
  bucket   = "acme-data-euc1"
}
```
For S3 replication, enable versioning on source and destination first (the provider docs put `depends_on = [aws_s3_bucket_versioning.source]` on the replication configuration).

Since AWS provider 6.0.0 most resources accept a top-level `region` argument, so many single-account multi-region cases no longer need an alias.

## Cross-account aliases
The AWS provider assumes a role through an `assume_role` block (`role_arn`, `session_name`, `external_id`).
```hcl
provider "aws" {
  alias  = "network"
  region = "eu-west-1"
  assume_role {
    role_arn     = "arn:aws:iam::111111111111:role/terraform-network"
    session_name = "tf-app-stack"
  }
}

resource "aws_route53_record" "app" {
  provider = aws.network
  zone_id  = var.zone_id
  name     = "app.acme.com"
  type     = "CNAME"
  ttl      = 300
  records  = [aws_lb.app.dns_name]
}
```

## Into modules
The root module passes a configuration with `providers = { aws = aws.dr }`. For a child module that uses an alias of its own, it must declare `configuration_aliases = [aws.west]` in `required_providers`, otherwise Terraform errors. Child modules do not inherit provider source or version requirements.
```hcl
module "replica" {
  source    = "./modules/bucket"
  providers = { aws = aws.dr }
}
```

## Gotchas
- Terraform has no `for_each` on provider blocks, so N regions means N alias blocks. OpenTofu documents `for_each` on a `provider` block (for example `for_each = var.aws_regions`).

## Verify
- [ ] The replica bucket is created in the DR region.
- [ ] The plan fails with an AssumeRole error if the trust relationship is removed (proves which role is used).

## Checked
2026-11-09

Method: read the Terraform provider configuration page (fetched as text), the AWS provider index, enhanced-region-support guide and S3 replication resource docs (raw markdown), and the OpenTofu provider configuration page (raw mdx). Removed as unsupported: the claim that aliased providers need valid credentials at plan even when unused, the single-state destroy remark, the base-role `sts:AssumeRole` note, and the `terraform state show` check. The Terraform-has-no-provider-for_each statement rests on the Terraform page not documenting it (the OpenTofu page does).
