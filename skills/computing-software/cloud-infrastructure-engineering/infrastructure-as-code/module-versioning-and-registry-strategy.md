---
id: computing-software.cloud-infrastructure-engineering.infrastructure-as-code.module-versioning-and-registry-strategy
name: module-versioning-and-registry-strategy
category: computing-software
field: cloud-infrastructure-engineering
product: infrastructure-as-code
tags: [infrastructure-as-code, iac, module-versioning, semver, semantic-versioning, module-registry, git-tags, version-constraints, pessimistic-constraint, renovate]
level: advanced
status: docs-checked
description: "Version and distribute shared Terraform modules: semver rules, registry publishing by git tag, consumer version constraints, and automated upgrade PRs."
sources: ["https://semver.org/", "https://developer.hashicorp.com/terraform/registry/modules/publish", "https://developer.hashicorp.com/terraform/language/expressions/version-constraints", "https://developer.hashicorp.com/terraform/language/modules/configuration", "https://developer.hashicorp.com/terraform/language/files/dependency-lock", "https://docs.renovatebot.com/modules/manager/terraform/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Module versioning and registry strategy

**Goal:** a platform team publishes modules that consumers pin and upgrade on their own schedule, without being silently broken.

## 1. Semantic versioning
Per semver.org: increment MAJOR for incompatible API changes, MINOR for backward-compatible functionality, PATCH for backward-compatible bug fixes. 0.y.z is for initial development where anything may change; 1.0.0 defines the public API.
Applying this to infrastructure is a judgement call, so write the policy down. A sensible reading (practitioner guidance, not from the sources): removing or renaming a variable or output, changing a variable's type, or any change that makes Terraform replace an existing resource is a breaking change for consumers. Check by planning the new version against infrastructure created with the previous one: a non-empty plan needs a changelog note, a replacement needs a major bump.

## 2. Publishing to a registry (Terraform Registry rules)
- Release versions are detected from git tags. A tag must be a semantic version, optionally prefixed with `v` (for example `v1.0.4` or `0.9.2`); tags that do not look like versions are ignored. At least one release tag must exist before the first publish. A webhook notifies the registry when you push a new tag.
- Public registry requirements: GitHub public repository named `terraform-<PROVIDER>-<NAME>`, a repository description, and the standard module structure. A private registry can ignore the public-GitHub requirement.
- Registry modules support versioning, generated documentation and version history. HashiCorp recommends publishing reusable modules to a registry. Removal of published versions is discouraged unless a version has a critical flaw.

## 3. Consumers: pinning
- For registry modules, the `version` argument takes a constraint. For git sources, pin with a `?ref=` tag or commit in the source URL (for example `git::https://example.com/vpc.git?ref=v1.2.0`, or a full commit hash).
- Constraint operators: `=` (exact), `!=`, `>`, `>=`, `<`, `<=`, and `~>`, which allows only the right-most version component to increment (`~> 1.1` allows 1.2 and 1.10 but not 2.0). Pre-release versions are matched only with an exact version.
- HashiCorp's best practice for modules: require specific versions when depending on third-party modules so updates happen when convenient; use ranges only when your organisation consistently uses semantic versioning and a well-defined release process.
- The dependency lock file records provider selections, not remote modules. Terraform always selects the newest module version meeting the constraints, so the constraint is the only control over module versions.
- After changing a module `source` or registry `version`, rerun `terraform init`; add `-upgrade` to move already-installed modules to the newest version the constraint allows.
- Reusable modules should constrain only minimum Terraform and provider versions (for example `>= 0.12.0`); root modules should use `~>` to give providers lower and upper bounds.
- `source` and `version` can use expressions only if their values are known during configuration loading.

## 4. Automated upgrades
Renovate's Terraform manager extracts module source references (and providers and `required_version`), supports datasources including `git-tags`, `github-tags`, `github-releases` and `terraform-module`, and uses the Terraform registry by default unless you configure an OpenTofu registry URL. Have the bot raise upgrade PRs and let CI plan them so reviewers see the real diff.

## Gotchas
- `?ref=main` in production configs means each plan may use different code.
- Re-tagging an existing version breaks reproducibility; treat tags as immutable by policy.

## Verify
- [ ] Written semver policy that says what counts as breaking, including resource replacement.
- [ ] No production config sources a module from a branch.

## Checked
Method: docs-checked 2026-11-09 against semver.org, the Terraform Registry publish page, version constraints, module configuration (module block) and dependency lock pages, and the Renovate Terraform manager page.
Removed as unconfirmed: repo-per-module versus monorepo guidance and thresholds, the distribution comparison table (Artifactory, Spacelift, env0, GitLab, Bicep, Pulumi, CDK), release-please and semantic-release, the deprecation support-window example and the `deprecated` variable argument, UPGRADING.md advice, and reference to a Terraform skill by id. Tags trimmed to match.
