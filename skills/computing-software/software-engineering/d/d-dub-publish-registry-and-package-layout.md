---
id: computing-software.software-engineering.d.d-dub-publish-registry-and-package-layout
name: d-dub-publish-registry-and-package-layout
category: computing-software
field: software-engineering
product: d
tags: [d-dub-publish-registry-and-package-layout, dub-commands, code-dlang-org, dub-registry, publish-package, semver-tags, ddox, dub-fetch, package-metadata, license, d]
level: practitioner
status: docs-checked
description: "Publish a DUB package: git repository with semver tags (vX.Y.Z), register on code.dlang.org, required recipe fields, webhooks, documentation (ddox) and deprecation."
sources:
  - https://dub.pm/dub-guide/publishing/
  - https://dub.pm/dub-reference/package_settings/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Publishing to code.dlang.org: tags, semver, docs and the registry

Goal: make a library available to others.

1. Complete the recipe: `name` (lower case ASCII alphanumerics, `-` or `_`), `description`, `authors`, `copyright`, `license` (a standard identifier such as "MIT" or "BSL-1.0"; SPDX identifiers are recommended for new packages), `homepage`; `targetType "library"` (or `sourceLibrary`).
2. Put it on GitHub/GitLab/Bitbucket and tag versions `v1.2.3` (SemVer). The repository is polled about twice per hour for new tags; named branches appear as rolling `~master`-style versions, which should only be used in `dub.selections.json` or overrides, never in dependencies.
3. Register an account on code.dlang.org, then register the package using your GitHub/GitLab/Bitbucket user name (or organization) and the project name.
4. Consumers: `dub add yourpkg` or `dependency "yourpkg" version="~>1.0.0"`; `dub fetch yourpkg` downloads.
5. Version numbers follow the SemVer specification.
6. Private registry: run your own dub-registry instance and add `"registryUrls": ["http://dubregistry.example.com/"]` to the dub settings file (or pass `--registry`); git dependencies via `repository` also work.

Verify: from a clean project run `dub add yourpkg && dub build`.

## Checked

Date 2026-11-02. Confirmed publishing steps, tag polling, ~master use and registry configuration (dub publishing guide). Error fixed: package names allow lower case alphanumerics, - and _. Removed webhook and ddox claims.

Method: documentation only; no commands were run.
