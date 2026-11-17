---
id: computing-software.cloud-infrastructure-engineering.terraform.terraform-query-and-list-blocks
name: terraform-query-and-list-blocks
category: computing-software
field: cloud-infrastructure-engineering
product: terraform
tags: [terraform, opentofu, terraform-query, list-block, tfquery-hcl, bulk-import, resource-discovery]
level: practitioner
status: docs-checked
description: "Discover existing infrastructure with terraform query and list blocks in .tfquery.hcl files, and generate import blocks and resource config from the results."
sources: ["https://developer.hashicorp.com/terraform/cli/commands/query", "https://developer.hashicorp.com/terraform/language/block/tfquery/list", "https://developer.hashicorp.com/terraform/language/import/bulk"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# `terraform query` and `list` blocks

`terraform query` searches existing infrastructure for resources that match the
`list` blocks in `.tfquery.hcl` files, so you can import unmanaged resources in
bulk. Searching by resource identity needs Terraform v1.12 or newer. Each provider
decides which resource types it supports (check the provider docs).

## Query file
Files end in `.tfquery.hcl` and sit in the configuration directory next to a normal
`.tf` configuration (which needs a `required_providers` block). `list` blocks are
only allowed in `.tfquery.hcl` files:
```hcl
# discover.tfquery.hcl
list "aws_instance" "prod" {
  provider = aws
  limit    = 50
  config {
    region = "us-east-2"
    filter {
      name   = "instance-state-name"
      values = ["running"]
    }
  }
}
```
Built-in arguments: `provider` (required), `count` or `for_each` (mutually
exclusive), `include_resource` and `limit`. Everything inside `config { }` is
provider-specific (filters, region), so read the provider docs. The label must be
unique in the directory; reference a list as `list.<label>.<attribute>`. A
`.tfquery.hcl` file may also hold `variable`, `locals` and its own `provider`
blocks.

## Running it
```bash
terraform init
terraform query                                   # prints list reference + identity per result
terraform query -generate-config-out=generated.tf # writes import and resource blocks
terraform query -json                             # machine-readable
terraform query -var 'env=prod'                   # set a variable of the query file
```
- `-generate-config-out` needs a path to a file that does not exist; rerunning with
  the file present is an error, so delete it first. With `-json`, the generated
  config appears in the JSON output instead of a file.
- Copy the generated `import` and `resource` blocks into `main.tf` and run
  `terraform apply`. The `import` blocks can then be removed or kept as a record of
  origin.

## Workflow
1. Write narrow list filters in `config` so results are reviewable.
2. Generate config into a new file, review it, then copy it into your configuration.
3. Apply to import; check the plan first.
4. In HCP Terraform, resource identity is how it tells that a resource is already
   managed by another workspace.

## Gotchas
- `limit` defaults to 100 results per list block; raise it deliberately.
- `include_resource` defaults to returning identities only. Set it to `true` to
  retrieve all attributes (needed to reference attributes of results); the docs
  warn it may affect performance.
- `-generate-config-out` requests full resource data even without
  `include_resource`.
- Policy evaluation with `-policies` (HCP Terraform remote queries) is documented as
  requiring Terraform v1.17.0 or later, and its results are informational only.

## Verify
- [ ] Result count matches what the cloud console shows for the same filter.
- [ ] The generated file reviewed before it is copied into `main.tf`.

## Checked
2026-11-08. Confirmed against the three cited HashiCorp pages: file extension, list
block arguments and defaults (limit 100, include_resource), `-generate-config-out`,
`-json`, `-var` behaviour, v1.12 identity requirement and v1.17.0 policy
requirement. Removed unsupported claims: "Terraform 1.14", the "unsupported types
error" text, OpenTofu has no `query`, the credentials-permissions note and the
"0 to add/change/destroy" plan assertion.
Method: documentation only; no commands were run.
