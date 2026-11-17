---
id: computing-software.devops-ci-cd.renovate.post-update-options
name: post-update-options
category: computing-software
field: devops-ci-cd
product: renovate
tags: [post-update-options, go-mod-tidy, npm-dedupe, renovate]
level: advanced
status: docs-checked
description: "Enable extra post-update steps such as bundlerConservative, goGenerate and composer flags with postUpdateOptions."
sources:
  - https://docs.renovatebot.com/configuration-options/
  - https://docs.renovatebot.com/self-hosted-configuration/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

`postUpdateOptions` is an array of extra steps Renovate runs after updating a dependency for certain package managers. Add the options you need:

```json
{
  "postUpdateOptions": ["gomodTidy", "npmDedupe", "bundlerConservative"]
}
```

Options documented include:

- `bundlerConservative`: run bundler in conservative mode, updating only the immediate dependency in the lock file rather than all sub-dependencies.
- `composerNoMinimalChanges`: run `composer update` without the `--minimal-changes` flag (lock file maintenance never uses it).
- `composerWithAll`: use `--with-all-dependencies` instead of `--with-dependencies`.
- `dotnetWorkloadRestore`: run `dotnet workload restore` before `dotnet restore`.
- `goGenerate`: run `go generate ./...` and commit any added or modified files. It runs after vendoring, installs no other tools, and only works if the global `allowedUnsafeExecutions` includes `goGenerate`.
- The full list of allowed values is `bundlerConservative`, `composerWithAll`, `composerNoMinimalChanges`, `dotnetWorkloadRestore`, `gomodMassage`, `gomodTidy`, `gomodTidy1.17`, `gomodTidyAll`, `gomodTidyE`, `gomodUpdateImportPaths`, `gomodSkipVendor`, `gomodVendor`, `goGenerate`, `helmUpdateSubChartArchives`, `kustomizeInflateHelmCharts`, `npmDedupe`, `npmInstallTwice`, `pnpmDedupe`, `yarnDedupeFewer` and `yarnDedupeHighest`.

The option can be set at repository, `packageRules`, manager, update type, vulnerability alert and group scope, and defaults to an empty list.

## Checked

2026-11-09: read the postUpdateOptions section of https://docs.renovatebot.com/configuration-options/ and allowedUnsafeExecutions in https://docs.renovatebot.com/self-hosted-configuration/. Removed the claim that no admin allowlist is needed (`goGenerate` needs `allowedUnsafeExecutions`) and the unsourced `binarySource` remark.

Method: documentation only; no commands were run.
