---
id: computing-software.devops-ci-cd.nx.nx-release-version-references
name: nx-release-version-references
category: computing-software
field: devops-ci-cd
product: nx
tags: [nx, nx-release, package-json, manifestrootstoupdate, dist, workspace-protocol, pnpm]
level: advanced
status: docs-checked
description: "Choose where nx release writes versions: source package.json, a custom dist directory via manifestRootsToUpdate and packageRoot, and workspace:/file: protocol handling."
sources:
  - https://raw.githubusercontent.com/nrwl/nx/master/astro-docs/src/content/docs/guides/Nx%20Release/updating-version-references.mdoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: control which manifest files get the new version and dependency references (Nx v21+ config format).

Scenario 1 (default): `nx release` updates the version and intra-workspace dependency refs in each source `package.json`, then stages and commits unless git operations are disabled.

Scenario 2: publish from a dist directory and update both source and dist manifests. `manifestRootsToUpdate` takes paths (or objects) with `{projectRoot}` and `{projectName}` placeholders; the publish target needs `packageRoot`:

```jsonc
{
  "release": { "version": { "manifestRootsToUpdate": [
    "{projectRoot}",
    { "path": "dist/packages/{projectName}", "preserveLocalDependencyProtocols": false }
  ] } },
  "targetDefaults": { "nx-release-publish": { "options": { "packageRoot": "dist/packages/{projectName}" } } }
}
```
The dist build must exist before versioning (see nx-release-pre-version-command). `packageRoot` is specific to the TS/JS publish implementation.

Scenario 3: update only dist. The source package.json is no longer the version source of truth, so set `"currentVersionResolver": "git-tag"` (or `"registry"`), `"manifestRootsToUpdate": ["dist/packages/{projectName}"]`, and in source use `"dep": "workspace:*"` or `"file:../dep"` for local deps. Unless you use pnpm or bun, also set `"preserveLocalDependencyProtocols": false` so dist gets real version numbers.

Scenario 4: version source files but keep `workspace:*`/`file:` refs. Since v21 `release.version.preserveLocalDependencyProtocols` defaults to `true`. Publishing then must swap the refs, which only pnpm and bun do (Nx calls `pnpm publish` or `bun publish`); npm and yarn error out.

Nx does not mutate packages in memory; publishing is done by the package manager's own publish command.

## Checked

2026-11-07. Confirmed against Updating Version References in Manifest Files: Nx v21+ config format, scenario 1 default behaviour and staging, manifestRootsToUpdate with {projectRoot} and {projectName}, the object form with preserveLocalDependencyProtocols, packageRoot on nx-release-publish via targetDefaults, scenario 3 (currentVersionResolver git-tag or registry, workspace:* or file:../dep refs, preserve false unless pnpm or bun), scenario 4 (default true since v21, only pnpm and bun supported, npm and yarn error), and the no-in-memory-mutation remark. Removed: the invented Verify step.

Method: documentation only; no commands were run.
