---
id: computing-software.cloud-infrastructure-engineering.terraform.no-code-provisioning-modules
name: no-code-provisioning-modules
category: computing-software
field: cloud-infrastructure-engineering
product: terraform
tags: [terraform, no-code-module, no-code-modules, no-code-provisioning, hcp-terraform, private-registry, self-service, tfe-no-code-module]
level: practitioner
status: docs-checked
description: "Make a private-registry module no-code ready in HCP Terraform so non-Terraform users provision workspaces from a form, with pinned versions and variable options."
sources: ["https://developer.hashicorp.com/terraform/cloud-docs/workspaces/no-code-provisioning/module-design", "https://developer.hashicorp.com/terraform/cloud-docs/workspaces/no-code-provisioning/provisioning"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# No-code provisioning modules

A no-code ready module lets someone pick a module from the private registry, fill in inputs, and get a new HCP Terraform workspace that deploys it, without writing HCL. Design the module for this use rather than flipping the switch on an existing one. No-code provisioning is available in HCP Terraform Standard and Premium editions; check your edition before promising it.

## 1. Requirements and design rules
- **Root module structure.** Follow standard module structure with resources in the root directory of the repository, so the registry can generate docs, track usage and parse submodules and examples.
- **Declare providers in the module.** Unlike modules used from written configuration, a no-code ready module must declare its required provider(s) directly.
- **Credentials.** New workspaces must be able to reach credentials for every provider in the module. Methods the docs list: a project-scoped variable set (recommended; applies to existing and future workspaces in the project), a global variable set, sensitive outputs from another workspace read via remote state, or letting the first run fail and having users add credentials (then start a new run manually).
- **One specific use case.** Scope each module to a single, well-defined use case (for example a three-tier web app, or a database with constrained size and region) to reduce technical decisions for users.
- **Defaults and options.** Set reasonable variable defaults. For variables without defaults, define dropdown options through the HCP Terraform UI, the No-Code Provisioning API or the TFE provider (use the provider if options should go through code review).

## 2. Enabling and version pinning
Enable no-code provisioning on a public or private module in the private registry. HCP Terraform pins the No-code Ready designation to a module version you choose (by default the latest), and deploys that version whenever someone provisions. Variable input options are tied to that version, so revisit them when you change it. To change the version: Registry, the module, Configure Settings, Edit version and variable options, pick the version, Save.

## 3. Provisioning flow
Requirement: a team with manage all projects, manage all workspaces, or project admin permission (custom project permissions need create workspaces, write variables and apply runs).
Registry, Modules (No-code Ready badge), select the module, Provision workspace. Set inputs (HCP Terraform prompts for variables without defaults and does type validation), then workspace name (unique in the organisation; letters, numbers, dashes, underscores), project, optional description and apply method. Auto apply is the default for no-code workspaces. Creating the workspace starts a run immediately.

## 4. Operations and upgrades
No-code workspaces cannot expose the configuration, but you can edit variables and settings (notifications, permissions, run triggers) and start new runs. When the designated module version changes, each provisioned workspace shows an update notice; HCP Terraform does not upgrade automatically. A workspace admin must act on it and is prompted for values of any new input variables.

## Gotchas
- A module's variables with no default and no dropdown options are free-form inputs, so add type constraints and validation in the module.
- If you skip setting inputs in the form, HCP Terraform does not prompt again and runs may fail.

## Verify
- [ ] Provisioning from the registry in a test project succeeds with credentials from the project variable set, not from form input.
- [ ] Changing the designated version shows an update notice on an existing workspace.

## Checked
2026-11-08. Read in full: the "Design no-code ready modules" and "Provision no-code infrastructure" pages. Removed: the `tfe_no_code_module` HCL example and `version_pin` argument (registry page was unreadable in this batch), claims about no VCS connection, plan-for-review during upgrade and `moved` blocks, and the missing-provider failure note, none of which the pages state. Dropped the unread tfe provider registry source.
Method: documentation only; no commands were run.
