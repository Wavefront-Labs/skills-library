---
id: computing-software.cloud-infrastructure-engineering.terraform.workspaces-vs-directories-for-environments
name: workspaces-vs-directories-for-environments
category: computing-software
field: cloud-infrastructure-engineering
product: terraform
tags: [terraform, opentofu, workspace-vs-directories, cli-workspaces, environment-layout, multi-environment]
level: practitioner
status: docs-checked
description: "Choose between CLI workspaces and separate configurations per environment using HashiCorp's guidance on credentials, backends, use cases and alternatives."
sources: ["https://developer.hashicorp.com/terraform/cli/workspaces#when-not-to-use-multiple-workspaces", "https://developer.hashicorp.com/terraform/language/state/workspaces"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Workspaces vs directories for environments

## What CLI workspaces are
Separate instances of state data inside the same working directory and the same backend.
Every initialized directory starts with a workspace named `default`, which cannot be
deleted. Manage them with `terraform workspace list`, `new`, `delete` and `select`; only
one is selected at a time, and most commands act on the selected one. You usually pass
different input variables per workspace to differentiate them. Running `plan` in a new
workspace does not access resources in other workspaces.

## HashiCorp's guidance
- Workspaces are "not a suitable isolation mechanism" for separate deployments (for
  example development stages or teams) whose backends need different credentials and
  access controls, because CLI workspaces in a directory share one backend. For those,
  HashiCorp recommends alternatives.
- They are also not a tool for system decomposition: create separate configurations at
  architectural boundaries, each with its own backend.
- Good fit: a parallel copy of infrastructure to test changes before touching
  production, for instance one workspace per feature branch, destroyed and deleted after
  merge. Workspaces share one working copy of the configuration and one set of plugin and
  module caches, whereas multiple directories duplicate caches and need separate updates
  and reinitialisation.

## The alternative
Put the common elements in reusable modules, and make each deployment a separate
configuration whose root module is only a backend configuration plus a few `module`
blocks passing the small differences. Each configuration then has its own backend,
credentials and access controls. To share data between distinct components, use paired
resource types and data sources (Consul key prefixes, tagging conventions, DNS records),
or `terraform_remote_state` if the state is readable from other configurations (tighter
coupling).

## Using the workspace name in configuration
`terraform.workspace` holds the current workspace name, for example
`count = terraform.workspace == "default" ? 5 : 1` or `Name = "web - ${terraform.workspace}"`.
Branching on it everywhere is a sign the environments differ enough to want separate
configurations (this is our reading of the guidance above, not stated on the page).

## Internals and caveats
- A workspace is technically equivalent to renaming the state file. Workspaces are a
  shared resource, not private.
- Local state is stored under `terraform.tfstate.d`; with several collaborators HashiCorp
  recommends a remote backend. In a remote backend the workspace name is appended to the
  state path (the Consul example), and names must be valid in a URL path segment.
- The current workspace name is stored locally in the ignored `.terraform` directory.
- Backends that support multiple workspaces: AzureRM, Consul, COS, GCS, Kubernetes,
  Local, OSS, Postgres, Remote, S3.
- HCP Terraform workspaces are different: each has its own configuration, variable
  values, state, run history and settings, like a separate working directory.

## Checked
Date: 2026-11-07
Read in full: "Manage Workspaces Overview" (CLI workspaces, including the When Not to Use section) and the "Workspaces" language/state page.
Confirmed: all statements above, except the one sentence marked as our reading.
Removed (not on the pages): the comparison table (blast radius, `.terraform/environment` file, divergence, duplication), recommendations for PR environments and CI path selection, the `lookup(local.cidrs, ...)` smell, the migration recipe (`state pull`/`state push`, `init -migrate-state`), and the Verify steps.
Method: documentation only; no commands were run.
