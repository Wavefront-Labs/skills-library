---
id: computing-software.cloud-infrastructure-engineering.terraform.branch-based-module-publishing-in-the-private-registry
name: branch-based-module-publishing-in-the-private-registry
category: computing-software
field: cloud-infrastructure-engineering
product: terraform
tags: [terraform, opentofu, branch-based-publishing, private-registry, registry-tests, module-publishing, hcp-terraform]
level: practitioner
status: docs-checked
description: "Publish private registry modules from a branch, not tags: pick versions by hand, enable registry tests on the branch, switch publishing type, and create versions via the API."
sources: ["https://developer.hashicorp.com/terraform/cloud-docs/registry/publish-modules", "https://developer.hashicorp.com/terraform/cloud-docs/registry/test", "https://developer.hashicorp.com/terraform/cloud-docs/api-docs/private-registry/modules"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Branch-based publishing (HCP Terraform private registry)

## Tag-based vs branch-based
| | Tag-based | Branch-based |
|---|---|---|
| New version created by | pushing a release tag (semantic version, optional `v` prefix) to the VCS repository | **Publish New Version** on the module overview screen: pick a commit SHA and assign a new module version |
| Tag or release needed in VCS | at least one release tag | no matching tag or release needed |
| Registry tests | not available | can be enabled |

Only branch-based modules can have testing enabled. Testing is disabled when the organization setting "Publish modules to your private registry from a single repository" is enabled.

## Add a module with branch publishing
Registry > Publish > Module > pick the VCS connection and repository > enable **Branch** > fill **Branch Name** (an existing branch), **Module Version** and **Source Directory** > Next > set **Module Name** and **Provider Name** > **Publish module**. You need the owners team or a team with Manage private registry permission, and the VCS user needs admin access to the repository (the registry creates webhooks).

## Release a new version
- UI: module overview > **Publish New Version** > select the commit SHA > assign a new version. An existing module version cannot be re-used.
- API: `POST /organizations/:organization_name/registry-modules/:registry_name/:namespace/:name/:provider/versions` with `registry-name` `private`. The endpoint applies to private modules without a VCS repository and to VCS-linked branch-based modules. Body attributes: `version` (required, a valid semver string) and `commit-sha` (optional, default null).
```bash
curl --header "Authorization: Bearer $TOKEN" \
  --header "Content-Type: application/vnd.api+json" \
  --request POST --data @payload.json \
  https://app.terraform.io/api/v2/organizations/my-organization/registry-modules/private/my-organization/my-module/aws/versions
```
```json
{"data": {"type": "registry-module-versions", "attributes": {"version": "1.2.3", "commit-sha": "abcdef12345"}}}
```
For a module without a VCS repository, upload the module archive to the link the response returns.

## Registry tests
- Enable when publishing (checkbox "Enable testing for module" under testing) or later: module overview > **Configure Tests** > **Enable testing for module**.
- HCP Terraform runs tests for every commit to the designated branch, to show whether publishing a new version is safe.
- Environment variables for tests: Configure Tests > Variables > **+ Add variable** (Key, Value, optional Sensitive). If tests provision infrastructure you must configure provider credentials; OIDC dynamic credentials for module testing are recommended and need a Standard, Plus or Enterprise tier.
- Run remotely from your machine: `terraform test -cloud-run=app.terraform.io/:ORG/:MODULE_NAME/:PROVIDER`.

## Switching publishing type
Module overview > Manage Module for Organization > Publish Settings.
- Tag to branch: configure a module branch and create a new module version; HCP Terraform does not create one automatically.
- Branch to tag: create at least one tag in the VCS repository.

## Gotchas
- Deleting a tag in VCS does not remove the version from the private registry; deleting a version is a manual step in the module's details page.
- If deleting a version would leave the module with no versions, the whole module is removed.

## Checked
Date: 2026-11-07. Read in full (text extract): the private registry publish-modules page (publishing workflows, branch-based considerations, release a new version, update publish settings, delete versions), the registry test page (enable testing, `-cloud-run`, environment variables, dynamic credentials), and the "Create a Module Version" section of the private-registry modules API page (path, `version`, `commit-sha`, `registry-name`, applicability). The rest of the API page (43k characters) was searched, not read end to end. Removed as unsupported: the Verify checklist, "you cannot mix both types" wording, the claim that publishing can require tests to pass, the semver-validity and root-directory gotchas, "tests run on PR pushes" and the consumer-pin step. The `#branch-based-publishing` anchor was dropped from the source URL. Code tabs on the pages were not separately opened.
Method: documentation only; no commands were run.
