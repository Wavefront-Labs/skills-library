---
id: computing-software.devops-ci-cd.nx.nx-release-docker
name: nx-release-docker
category: computing-software
field: devops-ci-cd
product: nx
tags: [nx, nx-release, docker, versionschemes, calendar-versioning, registry]
level: advanced
status: docs-checked
description: "Release Docker images with nx release (experimental): docker config, versionSchemes placeholders and date tokens, skipVersionActions, skipDefaultTag trap."
sources:
  - https://raw.githubusercontent.com/nrwl/nx/master/astro-docs/src/content/docs/reference/nx-json.mdoc
  - https://raw.githubusercontent.com/nrwl/nx/master/astro-docs/src/content/docs/features/manage-releases.mdoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: version and publish container images with calendar-style tags through `nx release`. Experimental: may break outside semver.

Enable with defaults: `"release": { "docker": true }`. Full form:
```jsonc
{ "release": { "docker": {
  "preVersionCommand": "npx nx run-many -t docker:build",
  "versionSchemes": {
    "production": "{currentDate|YYMM.DD}.{shortCommitSha}",
    "hotfix": "{currentDate|YYMM.DD}.{shortCommitSha}-hotfix",
    "staging": "{currentDate|YYMM.DD}-staging",
    "development": "{currentDate|YYMM.DD}-dev-{shortCommitSha}"
  },
  "skipVersionActions": ["api"],
  "repositoryName": "myorg",
  "registryUrl": "docker.io"
} } }
```
`repositoryName` can be overridden per project. `skipVersionActions` stops other tools (e.g. npm) versioning those projects; only set it if the scheme does not use `{versionActionsVersion}`.

Scheme placeholders:
- `{projectName}`, `{currentDate}` (ISO), `{currentDate|FORMAT}` with tokens `YYYY YY MM DD HH mm ss`
- `{shortCommitSha}` (7 chars), `{commitSha}`, `{versionActionsVersion}` (e.g. 1.2.3)
- `{env.NAME}` reads an environment variable; only Docker `versionSchemes` support it.
Examples: `{currentDate|YYMM.DD}.{shortCommitSha}` gives 2501.30.a1b2c3d; `{projectName}-{versionActionsVersion}` gives api-1.2.3.

Tags: `releaseTag.preferDockerVersion` (default false) prefers a Docker-compatible version format in git tags; `releaseTag.requireSemver` (default true) requires tags to match semantic versioning, and Manage Releases says to set it false for custom versioning schemes (nx-release-config-tags).

Group level (mix Docker with npm/Rust groups in one workspace):
```jsonc
{ "release": { "groups": { "backend": {
  "projects": ["api"], "projectsRelationship": "independent",
  "docker": { "skipVersionActions": true, "groupPreVersionCommand": "echo Preparing backend release" },
  "changelog": true } } } }
```

Trap: `@nx/docker` plugin option `buildTarget.skipDefaultTag: true` with custom `--tag` args opts that project out of nx release versioning and publishing. Leave it false/omitted if you use nx release.

## Checked

2026-11-07. Confirmed against the nx.json reference (Docker section): experimental caution, docker true shorthand, the full docker block, versionSchemes, skipVersionActions comment, repositoryName and registryUrl, placeholder list with the YYYY YY MM DD HH mm ss tokens, 7-character shortCommitSha, the four example patterns, only Docker versionSchemes reading {env.*}, group-level docker block, and the @nx/docker buildTarget skipDefaultTag warning. The releaseTag defaults are in the same page; the requireSemver advice is confirmed on Manage Releases, added to sources. Removed: the unstated claim that calendar schemes are not semver, and the invented dry-run Verify step.

Method: documentation only; no commands were run.
