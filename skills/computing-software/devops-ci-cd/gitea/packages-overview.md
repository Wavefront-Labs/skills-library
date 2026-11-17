---
id: computing-software.devops-ci-cd.gitea.packages-overview
name: packages-overview
category: computing-software
field: devops-ci-cd
product: gitea
tags: [gitea-package-registry, gitea, package-owner, link-package-to-repo, package-access-rules, package-token-scope, disable-packages]
level: intro
status: docs-checked
description: "Gitea Package Registry basics: supported package managers, owner-based ownership, linking to a repository, read and write access rules, token scope and deleting packages."
sources: ["https://gitea.com/gitea/docs/src/branch/main/docs/usage/packages/overview.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Gitea Package Registry overview

Available since Gitea **1.17** as a public or private registry. Supported types: Alpine (`apk`), Arch (`pacman`), Cargo, Chef (`knife`), Composer, Conan, Conda, Container (any OCI client), CRAN, Debian (`apt`), Generic (any HTTP client), Go, Helm (HTTP client or `cm-push`), Maven (`mvn`, `gradle`), npm (`npm`, `yarn`, `pnpm`), NuGet, Pub (`dart`, `flutter`), PyPI (`pip`, `twine`), RPM (`yum`, `dnf`, `zypper`), RubyGems (`gem`, Bundler), Swift, Terraform, Vagrant.
The rest applies only if packages are not globally disabled.

## Ownership and repository link
A package belongs to an **owner** (user or organization), not a repository. To show it in a repository, open the package's settings and pick a repository to link; the whole package is linked, not one version. The repository then lists it, and the package page links back to the repository and its issues.

## Access
- User-owned: read is public if the user is public, otherwise only that user; write is the owner only.
- Organization-owned: read is public if the org is public, otherwise members only; write needs membership of a team with write access to packages.
A team's packages permission covers all of the organization's packages regardless of which repositories the team has.
Package managers need a **personal access token with the `package` permission** set to Read (download) or Read & Write (publish).

## Working with packages
Publish with the native client for the type. View under a repository's **Packages** tab; download from the **Assets** section of a package page. **Packages cannot be edited after publishing**: delete (**Delete package**, permanent) and recreate.

## Disable
The registry is enabled automatically. Per repository: Settings, untick **Enable Repository Packages Registry**. Already published packages are not deleted by that. For tuning disk use see `gitea-package-cleanup`.

## Checked
2026-11-03. Commands, flags, settings, numbers and behaviour were compared line by line with the Gitea docs source page named in `sources` (read in full from the docs repository raw file). Nothing else removed; no unconfirmed claim remained.
Method: documentation only; no commands were run.
