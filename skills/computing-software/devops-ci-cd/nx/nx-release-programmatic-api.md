---
id: computing-software.devops-ci-cd.nx.nx-release-programmatic-api
name: nx-release-programmatic-api
category: computing-software
field: devops-ci-cd
product: nx
tags: [nx, nx-release, programmatic-api, releaseclient, node, scripting]
level: advanced
status: docs-checked
description: "Script releases with the nx/release Node API: releaseVersion, releaseChangelog, releasePublish, the releaseGraph hand-off, dryRun caveats and ReleaseClient config."
sources:
  - https://raw.githubusercontent.com/nrwl/nx/master/astro-docs/src/content/docs/guides/Nx%20Release/programmatic-api.mdoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: compose versioning, changelog and publish phases in a custom Node script instead of the `nx release` CLI.

```ts
import { releaseChangelog, releasePublish, releaseVersion } from 'nx/release';
```

These are the exact functions the CLI uses and read the same `release` config in `nx.json`. All are async and accept `dryRun` and `verbose`. If you filter with `projects` or `groups`, pass the same filters to all three.

```ts
const { workspaceVersion, projectsVersionData, releaseGraph } =
  await releaseVersion({ specifier: '1.0.0', dryRun: true, verbose: true });
await releaseChangelog({ releaseGraph, versionData: projectsVersionData, version: workspaceVersion, dryRun: true });
const publishResults = await releasePublish({ releaseGraph, dryRun: true });
process.exit(Object.values(publishResults).every((r) => r.code === 0) ? 0 : 1);
```

Return values:
- `releaseVersion`: `workspaceVersion` (non-null only when all projects share one version in one group), `projectsVersionData` (per project `currentVersion`, `newVersion`, `dockerVersion`, `dependentProjects`), `releaseGraph` (reuse to skip recomputation). `specifier` is unnecessary when using conventional commits.
- `releaseChangelog`: `workspaceChangelog` and `projectChangelogs`, each with `releaseVersion` and `contents`. One of `version` or `versionData` is required.
- `releasePublish`: map of project to `{ code }` exit code. Optional `versionData` is passed to custom executors as `nxReleaseVersionData`.

Gotcha: `dryRun` on `releasePublish` does not stop execution. It is forwarded to the `nx-release-publish` executor and sets `NX_DRY_RUN=true`. The built-in `@nx/js:release-publish` honours it; custom executors must check `dryRun` or `NX_DRY_RUN` themselves.

`ReleaseClient`: the standalone functions are bound methods of a pre-built instance. Build your own to override or replace config:

```ts
new ReleaseClient({ projects: ['project-1'] }, false); // merge with nx.json
new ReleaseClient({ projects: ['project-1'] }, true);  // ignore nx.json
```

## Checked

2026-11-07. Confirmed against Programmatic API: the nx/release imports, async functions with dryRun and verbose, the same-filters caution, releaseVersion return fields (workspaceVersion null rule, projectsVersionData with currentVersion, newVersion, dockerVersion, dependentProjects, releaseGraph reuse), releaseChangelog fields and the version or versionData requirement, releasePublish result map of { code }, the dryRun behaviour (forwarded to nx-release-publish, NX_DRY_RUN=true, built-in @nx/js:release-publish honours it, custom executors must), nxReleaseVersionData, and ReleaseClient constructor merge versus ignore flag. Removed: the invented Verify step (the page's tsx command belongs to its own yargs script, not the snippets here).

Method: documentation only; no commands were run.
