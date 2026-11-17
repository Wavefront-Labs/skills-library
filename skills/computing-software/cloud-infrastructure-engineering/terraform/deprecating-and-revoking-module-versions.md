---
id: computing-software.cloud-infrastructure-engineering.terraform.deprecating-and-revoking-module-versions
name: deprecating-and-revoking-module-versions
category: computing-software
field: cloud-infrastructure-engineering
product: terraform
tags: [terraform, opentofu, module-deprecation, private-registry, module-versioning, semver]
level: practitioner
status: docs-checked
description: "Retire private registry module versions in HCP Terraform: deprecate to warn, revoke to block new consumers, revert either, and where the warnings show."
sources:
  - https://github.com/hashicorp/web-unified-docs/blob/main/content/terraform-docs-common/docs/cloud-docs/registry/manage/module-versions.mdx
  - https://github.com/hashicorp/web-unified-docs/blob/main/content/terraform-docs-common/docs/cloud-docs/api-docs/private-registry/modules/versions.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Deprecating and revoking module versions

This applies to modules in an organization's **private registry** in HCP Terraform (and Terraform Enterprise).

## What each state does
- **Deprecate**: the version is still maintained but not recommended. Warnings appear on the module's registry page and in the run output of every user of that version. New users can still use it.
- **Revoke**: you no longer support the version. Warnings appear as for deprecation, and runs of *new* users who add that version fail. Existing users of a revoked version get a warning and their runs continue (the run output says it proceeds because they previously used that version).
- **Revert** a deprecation to remove all warnings. Reverting a revocation sets the version back to deprecated.

## Requirements
- Permission to manage private registry modules, and the module must be in the private registry.
- Deprecating needs the HCP Terraform Standard edition; revoking needs Premium.

## Deprecate in the UI
1. Open your organization, choose **Registry**, find the module.
2. Open the **Manage module for organization** dropdown and select the version.
3. Optionally fill **Reason for module deprecation** (shown in warnings) and **Link to additional information**.
4. Click **Deprecate**.

If the version carries the **No-code ready** pin, you are offered another version to move it to; the docs recommend pinning a version you will keep supporting.

## Revoke in the UI
Deprecate the version first, then use the same dropdown, optionally add a reason and link, and click **Revoke**. A revoked version with the **No-code ready** pin requires you to select another version for that pin.

## Via the API
Deprecation, reverting deprecation, revocation and reverting revocation are `PATCH` requests to `/api/v2/organizations/:organization_name/registry-modules/private/:organization_name/:module_name/:module_provider/:module_version`. A separate endpoint fetches a version's deprecation data. See the API page for payloads.

## Where warnings show
- Only workspaces in **remote** or **agent** execution mode receive deprecation or revocation warnings.
- In **Structured Run Output** mode the warnings are under the run's **Diagnostics** dropdown; in **Console UI** mode they appear in the run log.
- A deprecation warning begins "Found the following deprecated module versions, consider using an updated version." A run blocked by revocation says "This run references revoked module versions, this run will not proceed."

## Process
1. Release a fixed version and announce it.
2. Deprecate affected versions with a reason and a link to upgrade notes.
3. Revoke when you want to stop new consumers; revert if you decide to keep supporting it.

## Verify
- [ ] The deprecation or revocation message shows on the registry page and in a test workspace run (remote or agent execution mode).
- [ ] New runs referencing a revoked version fail as expected, and existing users only get warnings.

## Checked

Method: documentation only; no commands were run. Checked 2026-11-09 against the "Manage module versions" page and the private registry module versions API page in the hashicorp/web-unified-docs repository (the old `cloud-docs/registry/manage-module-versions` URL now 404s on developer.hashicorp.com; the page is `cloud-docs/registry/manage/module-versions`). Rewritten to what those pages state. Removed as not on them: the "delete a version" step, finding consumers with HCP Terraform Explorer or `gh search code`, the claim that public registry versions cannot be deprecated, the guidance on Git tags, the semver and `moved` block advice, and the "cached workspaces may continue until re-init" detail. The semver.org source was dropped with the semver advice.
