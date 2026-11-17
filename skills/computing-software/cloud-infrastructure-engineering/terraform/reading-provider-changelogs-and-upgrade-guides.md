---
id: computing-software.cloud-infrastructure-engineering.terraform.reading-provider-changelogs-and-upgrade-guides
name: reading-provider-changelogs-and-upgrade-guides
category: computing-software
field: cloud-infrastructure-engineering
product: terraform
tags: [terraform, opentofu, provider-changelog, provider-upgrade, major-version-upgrade, upgrade-guide, deprecation-warnings]
level: practitioner
status: docs-checked
description: "Plan a provider upgrade from its CHANGELOG and version upgrade guide: classify entries, find affected resources in your code, and confirm with a plan."
sources:
  - https://registry.terraform.io/providers/hashicorp/aws/latest/docs/guides/version-6-upgrade
  - https://github.com/hashicorp/terraform-provider-aws/blob/main/CHANGELOG.md
  - https://developer.hashicorp.com/terraform/language/providers/requirements
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Reading provider changelogs and upgrade guides

## Where
- `CHANGELOG.md` in the provider repository, one heading per release.
- For major versions, the provider's "Version N Upgrade Guide" under Guides in the registry docs (for the AWS provider, the Version 6 guide).

## Classify entries
The AWS provider changelog groups each release under these headings (not every release has every one):
| Section | Action |
|---|---|
| BREAKING CHANGES, NOTES | Read first; they flag behaviour you must act on |
| FEATURES | New resources and data sources; optional |
| ENHANCEMENTS | Mostly new or extended arguments; check for changed behaviour |
| BUG FIXES | Can change plan output for resources you already have |

The Version 6 upgrade guide is organised by topic: prerequisites, removed provider arguments, deprecated resources ("will be removed in a future major release"), removed services, and per-resource and per-data-source changes. Go through every heading and mark the ones that touch resources in your configuration.

## Map to your code
1. List the resource and data source types your configuration uses (search your `.tf` files for `resource "..."` and `data "..."` blocks).
2. Search the changelog entries since your current version, and the upgrade guide, for those type names and for provider arguments you set (for example `endpoints` entries).
3. Write down each hit and what it asks you to change.

## Validate with a plan
1. Raise the provider version constraint in a branch (`~>` style constraints are described in the provider requirements page) and run `terraform init -upgrade`, which downloads the new version and updates the dependency lock file.
2. Commit the lock file change. Locally, plan and apply use the versions recorded in the lock file; HCP Terraform and Terraform Enterprise use the lock file too, if there is one.
3. Run `terraform plan` for every configuration that uses the provider. Any difference should trace back to a changelog or upgrade guide entry.
4. Read all warnings; deprecated resources and arguments stay usable until the next major version but need scheduled work.

## Verify
- [ ] Every plan change after the upgrade traces to a changelog or upgrade-guide entry.
- [ ] Deprecations listed for the next major version are recorded as follow-up work.

## Checked

Method: documentation only; no commands were run. Checked 2026-11-09 against the Terraform AWS provider CHANGELOG.md on GitHub (heading names BREAKING CHANGES, NOTES, FEATURES, ENHANCEMENTS, BUG FIXES), the AWS provider Version 6 upgrade guide (section list, `terraform init -upgrade`, deprecation wording) and the Terraform provider requirements page (lock file behaviour locally and in HCP Terraform and Terraform Enterprise). Removed as unsupported by those pages: the grep and sort shell pipeline, the "perpetual diff" explanation of bug fixes, the claim that breaking changes appear only in majors, `moved` blocks as an upgrade step, `-compact-warnings`, the weekly Renovate cadence, and "after the first patch release of the major".
