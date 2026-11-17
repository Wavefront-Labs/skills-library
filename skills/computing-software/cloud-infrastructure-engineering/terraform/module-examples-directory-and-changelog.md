---
id: computing-software.cloud-infrastructure-engineering.terraform.module-examples-directory-and-changelog
name: module-examples-directory-and-changelog
category: computing-software
field: cloud-infrastructure-engineering
product: terraform
tags: [terraform, opentofu, module-examples, module-changelog, standard-module-structure, terraform-docs, semver, release-notes]
level: practitioner
status: docs-checked
description: "Lay out a reusable module per the standard structure: examples/ that run, README generated with terraform-docs, a Keep a Changelog CHANGELOG, and release-please automation."
sources: ["https://developer.hashicorp.com/terraform/language/modules/develop/structure", "https://terraform-docs.io/user-guide/configuration/", "https://keepachangelog.com/en/1.1.0/", "https://github.com/googleapis/release-please"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Module examples/ and CHANGELOG

## Standard module structure
From the Terraform "Standard Module Structure" page (for reusable modules in separate repositories). Only the root
module is required; everything else is optional:
```
terraform-aws-bucket/
  main.tf  variables.tf  outputs.tf     # recommended minimum, even if empty
  README.md                             # description and usage; inputs/outputs can be tool-generated
  LICENSE
  modules/                              # nested modules; one with a README.md is considered usable externally
    nestedA/  (README.md, main.tf, variables.tf, outputs.tf)
  examples/
    basic/    main.tf, optional README.md
    complete/
```
- `main.tf` is the primary entrypoint; nested module calls belong in it. Variables and outputs should have one or two
  sentence descriptions, used for documentation.
- Nested modules called from the root module should use relative paths such as `./modules/consul-cluster`, and should
  be composable by the caller rather than calling each other in a deep tree.
- Examples live in the root `examples/` directory (examples for submodules too). Because examples are often copied,
  their `module` blocks should use the source address an external caller would use, not a relative path. The page
  says a README does not need to document inputs/outputs because tooling generates them, and to use commit-specific
  absolute URLs for links or images inside the repository.

Local-path sources (`source = "../../"`) are fine for a CI harness that must test the checked-out code, but keep the
examples shown to users on the published address and a version constraint.

## README generation with terraform-docs
terraform-docs reads `.terraform-docs.yml` (module root first, then `.config/`, current directory, `$HOME/.tfdocs.d/`);
`-c`/`--config` selects another file and CLI flags override the file. `formatter` is the only required option. The
default `output.mode` is `inject`, which writes the content between the default markers:
```yaml
# .terraform-docs.yml
formatter: "<FORMATTER>"      # required; pick one from the terraform-docs formatter list
output:
  file: README.md
  mode: inject
```
```
<!-- BEGIN_TF_DOCS -->
<!-- END_TF_DOCS -->
```
Run `terraform-docs .` locally or in pre-commit. A CI check that fails when the committed README differs from
regenerated output is a team policy, not something these pages prescribe.

## CHANGELOG
Keep a Changelog 1.1.0 groups entries under `Added`, `Changed`, `Deprecated`, `Removed`, `Fixed` and `Security`, keeps
an `[Unreleased]` section, uses ISO 8601 dates, and says the project adheres to Semantic Versioning. One entry per
release:
```
## [3.0.0] - 2026-10-16
### Changed
- BREAKING: `logging` variable is now an object; see upgrade notes.
### Added
- `object_lock` support.
```
(`BREAKING:` prefixes are a convention of your own; Keep a Changelog defines only the six headings.) Decide and write
down what your module treats as a major bump (for example removed or renamed inputs and outputs).

## Automating
Release Please parses Git history for Conventional Commit messages and creates and updates release PRs. Merging the
release PR updates the changelog file (for example `CHANGELOG.md`), bumps versions, tags the release and creates a
GitHub release.

## Verify
- [ ] Every `examples/*` directory initialises and validates in CI.
- [ ] Every tag has a CHANGELOG entry; breaking changes have upgrade notes.

## Checked
Confirmed 2026-11-08 against the Terraform standard module structure page, the terraform-docs configuration page, Keep
a Changelog 1.1.0 and the release-please README. Removed: registry auto-rendering of examples, a `tests/` directory,
`sort.by: required`, the `markdown table` formatter value, the semver breaking-change list, `semantic-release`, and the
claim that the registry publishes from `vX.Y.Z` tags (not on the cited pages).
Method: docs-only read of cited pages, 2026-11-08
