---
id: computing-software.devops-ci-cd.gitea.package-npm
name: package-npm
category: computing-software
field: devops-ci-cd
product: gitea
tags: [gitea-npm-registry, gitea, npm-scope-registry, npm-auth-token, npm-dist-tag, npm-publish, npm-unpublish]
level: practitioner
status: docs-checked
description: "Use Gitea as an npm registry: scoped and unscoped npm config set commands, auth token, publish, unpublish, dist-tag rules and supported commands."
sources: ["https://gitea.com/gitea/docs/src/branch/main/docs/usage/packages/npm.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Gitea npm registry

Supports scoped and unscoped packages, usable with npm or Yarn (examples use npm and scope `@test`).

## Configure
```shell
npm config set {scope}:registry=https://gitea.example.com/api/packages/{owner}/npm/
npm config set -- '//gitea.example.com/api/packages/{owner}/npm/:_authToken' "{token}"
```
Token: a personal access token with `package` permissions. Without a scope, set the whole registry:
```shell
npm config set registry https://gitea.example.com/api/packages/testuser/npm/
npm config set -- '//gitea.example.com/api/packages/testuser/npm/:_authToken' "personal_access_token"
```

## Publish, unpublish, install
- `npm publish`. A package with the same name and version cannot be published again; delete the old one first.
- `npm unpublish {package_name}[@{package_version}]`, e.g. `npm unpublish @test/test_package@1.0.0`.
- `npm install {package_name}`, e.g. `npm install @test/test_package`.

## Tags
`npm dist-tag add {package_name}@{version} {tag}`, e.g. `npm dist-tag add test_package@1.0.2 release`. The tag name must not parse as a version; such names are rejected.

## Search and commands
`npm search` works but special qualifiers like `author:gitea` do not. Supported: `npm install`, `npm ci`, `npm publish`, `npm unpublish`, `npm dist-tag`, `npm view`, `npm search`.

## Checked
2026-11-03. Commands, flags, settings, numbers and behaviour were compared line by line with the Gitea docs source page named in `sources` (read in full from the docs repository raw file). Nothing else removed; no unconfirmed claim remained.
Method: documentation only; no commands were run.
