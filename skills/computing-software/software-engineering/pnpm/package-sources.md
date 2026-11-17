---
id: computing-software.software-engineering.pnpm.package-sources
name: package-sources
category: computing-software
field: software-engineering
product: pnpm
tags: [package-sources, jsr-registry, named-registries, git-dependencies, exotic-subdeps, tool-protocol, local-tarball-link, git-subdirectory]
level: practitioner
status: docs-checked
description: "Install packages from npm, JSR, named registries, tool: runtimes, local paths, tarballs and Git repositories with pnpm add, and know which sources are exotic and blockable."
sources:
  - https://pnpm.io/package-sources
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Trusted sources: npm registry (`pnpm add express@nightly`, `@1.0.0`, `@2`), JSR (`pnpm add jsr:@hono/hono@4`), named registries (`pnpm add work:@corp/lib@^2.0.0`; `gh:` and `npmjs:` need no setup, other aliases go under `namedRegistries`), workspace packages, and local paths. Provisioned tools use `tool:` (v12.13.0+): `pnpm add node@tool:24`, `pnx yarn@tool:4 --version`; `runtime:` is an alias. `crate:` and `pypi:` (v12.4.0+) need that ecosystem enabled in `pnpm-workspace.yaml`.

Local: `pnpm add ./package.tar.gz`; `pnpm add ./some-directory` records `link:` (symlink, same as `pnpm link`); `pnpm add file:./some-directory` copies the directory and installs its dependencies.

Exotic (set `blockExoticSubdeps: true` to forbid them in transitive dependencies): remote tarball URLs and Git.

```sh
pnpm add kevva/is-positive#master
pnpm add kevva/is-positive#semver:^2.0.0
pnpm add RexSkz/test-git-subfolder-fetch#path:/packages/simple-react-app
pnpm add gitlab:pnpm/git-resolver
```

Combine parameters with `&`. For GitHub, GitLab, Bitbucket and Gist, `owner/repo`, `github:` and https or ssh URLs are one identity resolved through the HTTPS URL (v12.0.0+). For private repos, rewrite with `git config --global url."git@github.com:".insteadOf https://github.com/`.

## Checked

2026-11-04. Confirmed trusted and exotic sources, jsr:, named registries, tool: and runtime:, crate: and pypi: gates, local path behaviour, Git forms and the v12.0.0 identity rule against pnpm.io/package-sources. Replaced one semver example with the page's own. Removed the unsourced closing Check line.

Method: documentation only; no commands were run.
