---
id: computing-software.cloud-infrastructure-engineering.google-cloud.terraform-module-structure-and-environment-layout
name: terraform-module-structure-and-environment-layout
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, infrastructure-as-code, terraform-module-structure, terraform-layout, gcs-backend, environments]
level: advanced
status: docs-checked
description: "Lay out Terraform for Google Cloud per Google's best practices: modules plus per-environment root configs, small states, remote state outputs, style and operations."
sources: ["https://cloud.google.com/docs/terraform/best-practices/general-style-structure", "https://cloud.google.com/docs/terraform/best-practices/root-modules", "https://cloud.google.com/docs/terraform/best-practices/operations"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Terraform module structure and environment layout

## 1. Layout (root modules guide)
Per application or service (for example shared networking), keep all its Terraform under one directory, split into:
```
SERVICE-DIRECTORY/
  modules/<service-name>/   main.tf variables.tf outputs.tf provider.tf README
  environments/
    dev/   backend.tf main.tf
    qa/    backend.tf main.tf
    prod/  backend.tf main.tf
```
- Each environment directory holds a `backend.tf` (state location, typically Cloud Storage) and a `main.tf` that
  instantiates the service module. Service modules hard-code common inputs and require only environment-specific ones.
- Each environment directory maps to the default workspace; use only the default workspace. Multiple CLI workspaces
  per environment are discouraged (hard to inspect, a shared backend becomes a single point of failure, workspace
  conditionals hurt readability).
- Keep each root small: all resources in a root refresh on every run. Guidance: no more than 100 resources in one
  state, ideally a few dozen.
- Separate directories per application so they are managed independently.

## 2. Wiring stacks
Export useful outputs from a root module and read them from other stacks with `terraform_remote_state`; only root-module
level outputs are referenceable. Expose service endpoints this way. Re-exporting an entire child module as one output is
acceptable when invoking a shared service module from environment directories.

## 3. Style (general style and structure guide)
- Standard module structure: start with `main.tf`, include a `README.md`, examples in `examples/` (one subdirectory
  each), group resources by purpose (`network.tf`, `dns.tf`), only `.tf` and repo metadata in the module root.
- Names: underscores between words; name a single resource of its type `main`; singular names; do not repeat the type.
- Variables in `variables.tf` with descriptions and types; units in names (`ram_size_gb`); positive boolean names; defaults
  for environment-independent values but none for environment-specific ones such as `project_id`; only parameterise what
  must vary. Adding a variable with a default is backwards-compatible; removing one is not.
- Outputs in `outputs.tf` with descriptions, referencing resource attributes (not input variables) so dependencies form.
- `count` for conditional creation, `for_each` for iterated resources; avoid user-specified values that are unknown at plan
  time driving `count`; no more than one ternary per line.
- Protect stateful resources, for example `lifecycle { prevent_destroy = true }`.
- Format with `terraform fmt`. Avoid custom scripts; put required ones in `scripts/`, helpers in `helpers/`, static files in
  `files/`, templates in `templates/` (`.tftpl`).
- Root modules: declare each provider in `versions.tf` pinned to a minor version, provide variables in
  `terraform.tfvars` (not CLI options), and check in `.terraform.lock.hcl`.

## 4. Operations
Always plan first and save the plan; run Terraform through an automated pipeline (Cloud Build or Terraform Cloud if none
exists); use CI service account credentials or workload identity federation rather than downloaded keys; use
`gcloud auth application-default login` locally; avoid `terraform import` where possible (new resources, delete old);
do not edit state by hand (use `terraform state`); review version pins regularly (for example with Dependabot).

## Verify
- [ ] `terraform fmt -check -recursive` and `terraform validate` pass for every root; each root stays well under 100 resources.

## Checked
2026-11-09: read the Google Cloud Terraform best-practice pages for general style and structure, root modules and
operations in full. Removed: the GCS bucket settings and IAM role (the store-state page was not read), the
`terraform_remote_state` alternative via data sources, `state mv`/`moved` advice, the "workspaces vs directories"
wording beyond what the page states, and the `?ref=` module pin example.
Method: documentation only; no commands were run.
