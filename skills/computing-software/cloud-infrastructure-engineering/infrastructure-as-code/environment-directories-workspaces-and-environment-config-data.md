---
id: computing-software.cloud-infrastructure-engineering.infrastructure-as-code.environment-directories-workspaces-and-environment-config-data
name: environment-directories-workspaces-and-environment-config-data
category: computing-software
field: cloud-infrastructure-engineering
product: infrastructure-as-code
tags: [infrastructure-as-code, environment-promotion, environment-directories, env-per-directory, environment-config, env-inventories, terraform-workspaces, tfvars]
level: practitioner
status: docs-checked
description: "Know what Terraform CLI workspaces are and are not suited for, and how terraform.workspace can vary naming and sizing."
sources:
  - https://developer.hashicorp.com/terraform/language/state/workspaces
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Terraform CLI workspaces and when not to use them

## What a workspace is
- A configuration has one backend. The backend holds persistent data (state) belonging to a workspace. It starts with one workspace, named `default`, which cannot be deleted.
- Some backends support multiple named workspaces, so several states can belong to one configuration without a new backend or new credentials. Backends listed as supporting this: AzureRM, Consul, COS, GCS, Kubernetes, Local, OSS, Postgres, Remote, S3.
- A plan in a new workspace does not see resources in other workspaces. They still exist; switch workspace to manage them.
- Terraform CLI workspaces are a different concept from HCP Terraform workspaces.

## When not to use them
The docs state workspaces are not appropriate for system decomposition or for deployments that need separate credentials and access controls. Because all workspaces share one backend and one set of credentials, environments with different access needs (for example production) need a different layout, such as separate configurations and backends. The docs point to the CLI "Use Cases" page for alternatives.

## Using the workspace name in code
`terraform.workspace` gives the current workspace name, for example to size a resource differently outside `default` or to include the name in naming and tags:
```hcl
resource "aws_instance" "example" {
  count = terraform.workspace == "default" ? 5 : 1
  tags = {
    Name = "web - ${terraform.workspace}"
  }
}
```

## Checked
Method: docs-checked 2026-11-09 against the Terraform "Workspaces" page (full text read).
Removed: directory-per-environment layout, `terraform workspace new/select` and `-var-file` commands, tfvars-per-environment advice, Ansible per-environment inventory layout and `ansible-inventory` check, guard rails, gotchas and verify steps (HashiCorp recommended-practices and Ansible sample-setup pages were not read).
