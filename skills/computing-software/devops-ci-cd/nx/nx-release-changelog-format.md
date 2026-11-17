---
id: computing-software.devops-ci-cd.nx.nx-release-changelog-format
name: nx-release-changelog-format
category: computing-software
field: devops-ci-cd
product: nx
tags: [nx, nx-release, changelog, renderer, renderoptions]
level: practitioner
status: docs-checked
description: "Trim or customise nx release changelogs: renderOptions (authors, commitReferences, versionTitleDate) and a custom renderer extending DefaultChangelogRenderer."
sources:
  - https://raw.githubusercontent.com/nrwl/nx/master/astro-docs/src/content/docs/guides/Nx%20Release/configure-changelog-format.mdoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: change what the default changelog renderer emits for each released project or the workspace.

`renderOptions` apply identically to `release.changelog.workspaceChangelog` and `release.changelog.projectChangelogs`. All four default to `true`:

```json
{ "release": { "changelog": { "projectChangelogs": { "renderOptions": {
  "authors": true,
  "applyUsernameToAuthors": true,
  "commitReferences": true,
  "versionTitleDate": true
} } } } }
```

- `authors`: "Thank You" section of commit authors (bots and known AI coding agents are excluded).
- `applyUsernameToAuthors`: maps authors to GitHub usernames via https://ungh.cc using commit emails. Set `false` to avoid external requests. Before Nx v21 it was `mapAuthorsToGitHubUsernames`.
- `commitReferences`: commit/PR links.
- `versionTitleDate`: date in the version title (YYYY-MM-DD).

Set all four to `false` for a minimal changelog: heading `## 7.9.0` and bullets without links or authors.

Custom renderer (Nx 22+): point `renderer` at a module whose export (module.exports in CommonJS, or a default ESM export) is a class extending `DefaultChangelogRenderer`. Workspace paths must start with `{workspaceRoot}`; plain relative paths like `./tools/x.js` do not resolve.

```jsonc
{ "release": { "changelog": { "projectChangelogs": { "renderer": "{workspaceRoot}/tools/custom-changelog-renderer.js" } } } }
```

```javascript
const DefaultChangelogRenderer = require('nx/release/changelog-renderer').default;
module.exports = class CustomRenderer extends DefaultChangelogRenderer {
  renderVersionTitle() { return `# Release ${this.changelogEntryVersion}`; }
};
```

Override a protected method to change one stage (`renderVersionTitle`, `renderChangesByType`, `renderBreakingChanges`, `renderDependencyBumps`, `renderAuthors`, `formatChange`), or override `render()` (call `super.render()` to extend, or skip it to replace). The breaking/dependency/author sections only run when `hasBreakingChanges()`, `hasDependencyBumps()`, `shouldRenderAuthors()` return true. The programmatic `ReleaseClient` (Nx 22+) can take the class directly.

## Checked

2026-11-07. Confirmed against Configure Changelog Format: the four renderOptions and their true defaults, the Nx v21 rename from mapAuthorsToGitHubUsernames, ungh.cc lookup, bot and AI-agent exclusion, the minimal-changelog example, the Nx 22+ custom renderer, the {workspaceRoot} path rule, the protected method names, the gate methods and the ReleaseClient note. Removed: the invented dry-run Verify step.

Method: documentation only; no commands were run.
