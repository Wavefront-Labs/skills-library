---
id: computing-software.cloud-infrastructure-engineering.terraform.data-sources
name: data-sources
category: computing-software
field: cloud-infrastructure-engineering
product: terraform
tags: [terraform, opentofu, data-source, data-sources, data-block, lookup, read-only, aws-ami, caller-identity, terraform-remote-state, depends-on, refresh, deferred-read]
level: intro
status: docs-checked
description: "Read existing infrastructure with data blocks: references, the single-result rule, reads deferred to apply, depends_on, conditions, and remote_state, http and external sources."
sources: ["https://developer.hashicorp.com/terraform/language/data-sources", "https://developer.hashicorp.com/terraform/language/state/remote-state-data", "https://raw.githubusercontent.com/hashicorp/terraform-provider-aws/main/website/docs/d/ami.html.markdown", "https://raw.githubusercontent.com/hashicorp/terraform-provider-aws/main/website/docs/d/caller_identity.html.markdown", "https://raw.githubusercontent.com/hashicorp/terraform-provider-aws/main/website/docs/d/ssm_parameter.html.markdown", "https://raw.githubusercontent.com/hashicorp/terraform-provider-external/main/docs/data-sources/external.md", "https://raw.githubusercontent.com/hashicorp/terraform-provider-http/main/docs/data-sources/http.md"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Data sources

**Goal:** reference things Terraform does not manage (or that another state manages) by querying them instead of hard-coding IDs. Data sources fetch data from the provider but do not create or modify resources; Terraform can only read them.

## 1. Shape
```hcl
data "aws_ami" "web" {
  most_recent = true
  filter {
    name   = "state"
    values = ["available"]
  }
  filter {
    name   = "tag:Component"
    values = ["web"]
  }
}

resource "aws_instance" "web" {
  ami           = data.aws_ami.web.id
  instance_type = "t1.micro"
}
```
- Referenced as `data.<TYPE>.<NAME>.<ATTRIBUTE>`; the type and name combination must be unique. Arguments are provider-specific (see the provider docs).
- Data blocks support expressions, `count`, `for_each`, the `provider` meta-argument (alternate configuration, `provider = aws.uswest1`), `depends_on`, and `precondition`/`postcondition` in `lifecycle`.

## 2. The single-result rule
`aws_ami` fails if more or less than one image matches: narrow the filters, use `most_recent`, or use the `aws_ami_ids` data source to match several. Arguments `filter`, `owners`, `most_recent` are specific to that provider; read its page before relying on them elsewhere. `owners` accepts an account ID, `self`, or an alias such as `amazon`.

## 3. When reads are deferred to apply
Terraform tries to read data sources during planning (the refresh phase, by default before the plan), but defers the read to apply when an argument refers to a value it cannot predict:
- the data block directly depends on a managed resource that is changing in this plan;
- its custom conditions depend, directly or indirectly, on such a resource;
- arguments refer to values computed only during apply.
Deferred reads are indicated in the plan output and the data source's attributes show as computed. `depends_on` on a data block defers the query until Terraform has finished the operations for that dependency, so prefer referencing the resource's attribute directly. The docs recommend Terraform 0.13 or newer for `depends_on` in data blocks (in 0.12 and earlier it always defers the read to apply).
Specialized local-only data sources such as `template_file`, `local_file` and `iam_policy_document` are recalculated on each plan.

## 4. A common lookup
```hcl
data "aws_caller_identity" "current" {}   # takes no arguments; exports account_id, arn, user_id
```

## 5. Cross-state and external reads
- `terraform_remote_state` (built-in provider `terraform.io/builtin/terraform`, needs no provider configuration) reads the latest state snapshot from a backend and exposes only root-module output values as `outputs`, which means nested module outputs need a passthrough output. The reader needs access to the entire state snapshot, which often includes sensitive data, so the docs recommend publishing shared data to a separate store (for example SSM Parameter Store, S3 objects, Route 53/DNS records, Consul, Kubernetes ConfigMaps), and `tfe_outputs` for HCP Terraform/Terraform Enterprise. See `computing-software.cloud-infrastructure-engineering.terraform.remote-state-and-module-layout`.
- `http` (HTTP provider): makes a GET (also `HEAD` or `POST` for read-only URLs) request; exports `response_body`, `status_code`, `response_headers`. `body` is deprecated. No retries unless a `retry` block is configured (then retries on client errors and 5xx other than 501). HTTPS gives no server authentication beyond certificate chain verification, so treat data from servers you do not control as untrustworthy. `insecure` defaults to `false`.
- `external`: runs a program (`program` list, not run through a shell) that reads a JSON object of strings from stdin and must print a JSON object of strings to stdout and exit zero; on error it prints a message to stderr and exits non-zero. It passes all environment variables through, re-runs on each state refresh, and the docs call it an escape hatch that hurts portability and is not recommended in Terraform Enterprise.

## 6. Validating what you read
```hcl
data "aws_ami" "example" {
  id = var.aws_ami_id

  lifecycle {
    postcondition {
      condition     = self.tags["Component"] == "nomad-server"
      error_message = "tags[\"Component\"] must be \"nomad-server\"."
    }
  }
}
```

## Gotchas
- The `http` data source issues a warning if the response is not UTF-8 encoded.
- Sensitive values returned by data sources can still be written to state (for `aws_ssm_parameter`, a SecureString value is stored in plain text in the raw state).

## Checked
Date: 2026-11-07. Read in full: "Query infrastructure data" (data sources), the `terraform_remote_state` page, and the provider docs for `aws_ami`, `aws_caller_identity`, `external` and `http` (raw files from the provider repositories; the registry website pages return no readable text). Removed as unsupported: the `<= (read during apply)` marker text, "permanently noisy plans" from depends_on, the `aws_region`, `aws_availability_zones`, `aws_iam_policy_document` and `aws_secretsmanager_secret_version` snippets, the `checkip.amazonaws.com` example, "plan-only CI needs read permissions", "no diff for a data source", the for_each key rules, and all three Verify items. The `aws_ssm_parameter` plain-text-in-state note comes from its provider page, also read in full.
Method: documentation only; no commands were run.
