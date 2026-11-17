---
id: computing-software.cloud-infrastructure-engineering.terraform.data-source-filters-most-recent-and-for-each
name: data-source-filters-most-recent-and-for-each
category: computing-software
field: cloud-infrastructure-engineering
product: terraform
tags: [terraform, opentofu, data-filter, most-recent, data-source-for-each, data-for-each, aws-ami, data-sources]
level: practitioner
status: docs-checked
description: "Write data-source lookups with filter blocks, owners and most_recent that match one result, use aws_subnets ids, and iterate data sources with for_each."
sources: ["https://developer.hashicorp.com/terraform/language/data-sources", "https://raw.githubusercontent.com/hashicorp/terraform-provider-aws/main/website/docs/d/ami.html.markdown", "https://raw.githubusercontent.com/hashicorp/terraform-provider-aws/main/website/docs/d/subnets.html.markdown", "https://raw.githubusercontent.com/hashicorp/terraform-provider-aws/main/website/docs/d/ssm_parameter.html.markdown"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Data-source filters, `most_recent`, and `for_each`

## Filtered lookup returning one result
```hcl
data "aws_ami" "example" {
  most_recent = true
  owners      = ["self"]

  filter {
    name   = "name"
    values = ["myami-*"]
  }
  filter {
    name   = "virtualization-type"
    values = ["hvm"]
  }
}
```
- `filter` names are the cloud API's filter names, not Terraform attribute names: for `aws_ami` they come from EC2 `describe-images`; for `aws_subnets` from `DescribeSubnets` (for a tag use `tag:Name`).
- `owners` takes an AWS account ID, `self`, or an owner alias such as `amazon`, `aws-marketplace` or `microsoft`.
- If more or less than one AMI matches, Terraform fails. Make the search specific, or use `most_recent`. To match several AMIs use the `aws_ami_ids` data source.
- `most_recent` only applies when more than one result is returned.
- `name_regex` filters locally on what AWS returns and can be slow on large results.
- `allow_unsafe_filter`: the provider warns that with an unsafe filter and `most_recent = true`, a third party may introduce a new image that your lookup returns; it recommends filtering by owner or image ID.
- A data source without `region` uses the provider configuration's Region. To read from another provider configuration use `provider = aws.<alias>` (the language page's example is `provider = aws.uswest1`).

## Choosing a stable result
With `most_recent = true` the data source returns whichever matching image is newest at read time, so the value passed to `ami` changes whenever a newer match appears. Decide deliberately between a lookup that follows new images and a pinned AMI ID held in a variable.

## Plural data sources
```hcl
data "aws_subnets" "private" {
  filter {
    name   = "vpc-id"
    values = [var.vpc_id]
  }
  tags = { Tier = "Private" }
}
```
`aws_subnets` exports `ids` (list of subnet IDs found). `tags` must exactly match pairs on the desired subnets. A subnet is selected if any one of a filter's `values` matches.

## Iterating
Data blocks accept `count` and `for_each`; each instance is read and indexed separately and referenced as `data.<TYPE>.<NAME>[<KEY>]`.
```hcl
data "aws_subnet" "private" {
  for_each = toset(data.aws_subnets.private.ids)
  id       = each.value
}

data "aws_ssm_parameter" "cfg" {
  for_each = toset(["db_host", "db_port"])
  name     = "/app/${var.env}/${each.key}"
}
```
- The first form is the provider's own `aws_subnets` pattern.
- `aws_ssm_parameter` `value` is always marked sensitive in plan output (`insecure_value` is never sensitive), and the decrypted value of a SecureString is stored in the raw state as plain text.

## Gotchas
- Terraform may defer reading a data source to apply when an argument refers to a resource attribute it cannot predict at plan time; the plan indicates this and values show as computed.
- `depends_on` on a data block makes Terraform defer the query until after the specified dependency.

## Checked
Date: 2026-11-07. Read in full: the Terraform "Query infrastructure data" page and the provider docs for `aws_ami`, `aws_subnets` and `aws_ssm_parameter` (raw files from the terraform-provider-aws repository, because the registry website returns no readable text). The EC2 `DescribeImages` API page was not re-read. Removed as unsupported: the Canonical owner ID and Ubuntu name pattern, "ALWAYS pin owners" as a rule (the page only warns about unsafe filters), the exact "Your query returned no results" string, `lifecycle { ignore_changes = [ami] }` and instance-refresh advice, the postcondition-on-empty advice, the claim that for_each keys must be non-sensitive, the unverified tag-filter statement for other data sources, and both Verify items.
Method: documentation only; no commands were run.
