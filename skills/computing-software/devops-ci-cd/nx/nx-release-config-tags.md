---
id: computing-software.devops-ci-cd.nx.nx-release-config-tags
name: nx-release-config-tags
category: computing-software
field: devops-ci-cd
product: nx
tags: [nx, nx-release, releasetag, git-tags, projectsrelationship, semver]
level: practitioner
status: docs-checked
description: "Configure nx release: first dry run, release.projects filters, projectsRelationship fixed or independent, nested releaseTag pattern and options, Nx 22/23 changes."
sources:
  - https://raw.githubusercontent.com/nrwl/nx/master/astro-docs/src/content/docs/features/manage-releases.mdoc
  - https://raw.githubusercontent.com/nrwl/nx/master/astro-docs/src/content/docs/reference/nx-json.mdoc
  - https://raw.githubusercontent.com/nrwl/nx/master/astro-docs/src/content/docs/guides/Nx%20Release/release-groups.mdoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: set up `nx release` safely and control which projects release and how git tags look.

Phases: version, changelog, publish. First run (no prior release to diff):
```shell
nx release --first-release --dry-run
```
Always dry-run first; publishing is hard to undo. By default it prompts for major/minor/patch or a custom version. Phase-only commands: `nx release version`, `nx release changelog`, `nx release publish`, `nx release plan` (version plan files).

Basic `nx.json`:
```jsonc
{ "release": {
  "projects": ["*", "!ignore-me"],
  "projectsRelationship": "independent"
} }
```
- `projects`: string or array; names, globs, directories, tag references, anything `--projects` accepts.
- `projectsRelationship`: `"fixed"` (default, lock-step) or `"independent"`.

Tags, nested `releaseTag` (flat `releaseTagPattern*` properties removed in Nx 23; a Nx 22 migration moves them):
```jsonc
{ "release": { "releaseTag": {
  "pattern": "{releaseGroupName}-v{version}",
  "requireSemver": true, "strictPreid": true,
  "preferDockerVersion": false,
  "checkAllBranchesWhen": ["main", "release/*"] } } }
```
Defaults: `pattern` is `v{version}` (fixed) or `{projectName}@{version}` (independent); `requireSemver` true (set false for custom schemes such as calendar versions); `strictPreid` true; `preferDockerVersion` false. Placeholders: `{version}`, `{projectName}`, `{releaseGroupName}`; no `??` fallbacks.

`checkAllBranchesWhen`: unset = look on the current branch, fall back to all; `true` = always all branches; `false` = current branch only; `string[]` = all branches when the current branch matches a name/glob.

Release groups: `release.groups.<name>` with own `projects`, `projectsRelationship`, `docker`, `changelog`. Fixed-group tag default is `{releaseGroupName}-v{version}` (Nx 22).

## Checked

2026-11-07. Confirmed against Manage Releases (first-release with dry-run, three phases, default prompt, requireSemver false for custom schemes) and the nx.json reference (release.projects matchers, projectsRelationship default fixed, nested releaseTag table with defaults, checkAllBranchesWhen behaviours, placeholders with no ?? fallbacks, flat releaseTagPattern properties removed in Nx 23 with a Nx 22 migration, fixed-group default tag pattern in Nx 22). Group keys confirmed on the Release Groups page, added to sources. Removed: the invented dry-run Verify step.

Method: documentation only; no commands were run.
