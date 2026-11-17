---
id: computing-software.cloud-infrastructure-engineering.terraform.publishing-modules-to-the-private-registry-from-vcs-tags
name: publishing-modules-to-the-private-registry-from-vcs-tags
category: computing-software
field: cloud-infrastructure-engineering
product: terraform
tags: [terraform, registry-vcs-publish, semver-tags, private-registry, hcp-terraform, module-publishing, tfe-provider, tfe-registry-module]
level: practitioner
status: docs-checked
description: "Publish a module to the HCP Terraform/TFE private registry from a VCS repo using semver git tags (or branch-based publishing), then consume and retire versions."
sources: ["https://developer.hashicorp.com/terraform/cloud-docs/registry/publish-modules", "https://developer.hashicorp.com/terraform/registry/modules/publish", "https://raw.githubusercontent.com/hashicorp/terraform-provider-tfe/main/website/docs/r/registry_module.html.markdown"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Publishing modules from VCS tags

The private registry ingests a module version when a semver release tag lands on the connected repository (tag-based publishing). Get the repo shape right once and releasing becomes `git tag`.

## 1. Repository requirements
- The repo must be in a configured VCS provider, and the connecting user must have admin access to it (the registry creates a webhook to import new versions).
- The public Terraform Registry requires the repo name `terraform-<PROVIDER>-<NAME>` (for example `terraform-aws-vpc`). In the private registry you enter the module name and provider name when publishing.
- Module source (and any submodules) must follow the standard module structure so the registry can inspect it and generate documentation.
- Several modules can live in one repository: give each a **Source Directory** and a **Module Tag Prefix** (for example `app-` matches tag `app-v1.0.0` and publishes `v1.0.0`). Without a prefix, every module in the repo publishes a new version for every valid semver tag.

## 2. Tags
- Tags must be semantic versions, optionally prefixed with `v`: `v1.4.0`, `0.9.2`. Tags that do not match are ignored, which is the usual "my version never appeared" cause. At least one release tag must exist to publish.
- Deleting a tag in VCS does not remove the version from the registry.
- To redo a version: delete that version in the registry (or the whole module), then push a new tag with the same name. Prefer cutting the next patch.

## 3. Publishing
UI: Registry, Publish, Module, pick the VCS connection and repo, choose the **Tag** publishing type, fill Module Tag Prefix and Source Directory, then confirm module name and provider name. As code with the `tfe` provider:
```hcl
resource "tfe_registry_module" "vpc" {
  vcs_repo {
    display_identifier = "acme/terraform-aws-vpc"
    identifier         = "acme/terraform-aws-vpc"
    oauth_token_id     = tfe_oauth_client.github.oauth_token_id   # or github_app_installation_id
  }
}
```
(`organization` is required with a GitHub App and otherwise comes from the provider config.) When `source_directory` is used you must set both `name` and `module_provider`.

Branch-based publishing (`vcs_repo.branch` set, with `initial_version`) publishes versions from the UI/API by choosing a commit SHA and a new version number (versions cannot be reused). Only branch-based modules can enable registry module tests (`test_config { tests_enabled = true }`). You can switch modes later in Publish Settings; switching to branch needs a module branch and a new version, switching to tags needs at least one tag.

## 4. Release routine
```bash
git checkout main && git pull
terraform fmt -check -recursive && terraform validate
git tag -a v1.5.0 -m "v1.5.0: add flow logs toggle"
git push origin v1.5.0
```
Push the tag and the registry imports the new version. Breaking input/output changes are a major bump; ship `moved` blocks in the same release when addresses change.

## 5. Consuming
The module's details page lists available versions, documentation and a copyable usage example, so take the `source` address from there. Local runs need `terraform login` or a `TF_TOKEN_<hostname>` variable.

## Gotchas
- If the VCS connection loses access, the webhook stops importing new tags; check the module's version list after each release.
- Deleting the last remaining version removes the whole module.
- Publishing requires the owners team or a team with Manage private registry permissions.

## Verify
- [ ] The new tag appears as a version in the registry.
- [ ] `terraform init` in a consumer resolves the constraint to the new version.
- [ ] Non-semver tags are not used for releases.

## Checked
2026-10-28. Confirmed against the HCP Terraform "Publish private modules" page, the public registry module publishing page (repo naming, semver tags), and the tfe_registry_module resource doc in terraform-provider-tfe: admin-access requirement, standard structure, tag prefix and source directory, ignored tags, deletion behaviour, restore procedure, branch-based publishing and module tests, mode switching, permissions, resource arguments.
Corrected: "one module per repo; a monorepo needs branch-based publishing" (tag prefix plus source directory supports several modules per repo).
Removed: pre-release tag selection behaviour, the `v2.0.0-rc.1` example, "silently ignored", the lock file not pinning modules, the registry UI showing submodules automatically, an unverified timing, the hard-coded consumer `source` and `version` example, the claim that deleting a pinned version breaks `init`, and the `tags = false` example (the doc says `branch` selects branch mode).
Method: documentation only; no commands were run.
