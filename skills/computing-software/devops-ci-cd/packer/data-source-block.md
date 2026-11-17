---
id: computing-software.devops-ci-cd.packer.data-source-block
name: data-source-block
category: computing-software
field: devops-ci-cd
product: packer
tags: [data-source, datasource, evaluate-datasources, hcl2, block-data]
level: practitioner
status: docs-checked
description: "Read external data such as an AMI id with a data block and reference it as data.TYPE.NAME.ATTR."
sources:
  - "https://developer.hashicorp.com/packer/docs/templates/hcl_templates/blocks/data/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

A `data` block instructs Packer to fetch or compute data defined outside Packer, for use in `locals` blocks and `source` blocks. It takes two labels: the data source type and a name. The combination of type and name must be unique within a configuration.

```hcl
data "amazon-ami" "example" {
  filters = {
    virtualization-type = "hvm"
    name                = "ubuntu/images/*ubuntu-xenial-16.04-amd64-server-*"
    root-device-type    = "ebs"
  }
  owners      = ["099720109477"]
  most_recent = true
}

locals {
  source_ami_id   = data.amazon-ami.example.id
  source_ami_name = data.amazon-ami.example.name
}
```

The configuration inside the block depends on the data source type and is documented for each data source. A data source can output one or more attributes, referenced as `data.<TYPE>.<NAME>.<ATTRIBUTE>`; for `amazon-ami` the outputs include `id`, `name`, `creation_date`, `owner`, `owner_name` and `tags`.

Known limitation: locals can reference data sources, but data sources cannot reference locals, to avoid cyclic dependencies. To pass user input into a data source, use a `variable` block and `var.<name>`.

You can also write your own custom data source as a plugin.

## Checked

Method: docs-checked 2026-11-09 against the Packer data block page and the Data sources reference page including its known-limitations text (read in full as published page source). Dropped the claims about `packer validate` and `-evaluate-datasources`, `required_plugins`/`packer init`, billing, and filter-pinning advice, which these pages do not state.
