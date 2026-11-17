---
id: computing-software.devops-ci-cd.nx.nx-configure-outputs
name: nx-configure-outputs
category: computing-software
field: devops-ci-cd
product: nx
tags: [nx, caching, outputs, targetdefaults, project-json, task-graph]
level: practitioner
status: docs-checked
description: "Configure which files Nx restores from cache with target outputs: path tokens, {options.x} with ?? fallbacks, targetDefaults vs project-level override semantics."
sources:
  - https://raw.githubusercontent.com/nrwl/nx/master/astro-docs/src/content/docs/kb/configure-outputs.mdoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: make cache hits restore exactly the files a task produced.

Terminal output is always cached and replayed. File outputs come from the target's `outputs`:

```jsonc
"outputs": [
  "{projectRoot}/dist/libs/mylib",         // directory
  "{workspaceRoot}/dist/{projectRoot}",    // by project root
  "{workspaceRoot}/dist/{projectName}",    // by project name
  "{workspaceRoot}/test-results.xml",      // file
  "{projectRoot}/dist/libs/mylib/**/*.js", // glob
  "{options.outputPath}"                   // from task options
]
```

Rules: explicit paths must start with `{projectRoot}` or `{workspaceRoot}` (`{workspaceRoot}` only at the start; `{projectRoot}` and `{projectName}` may appear later). Same glob syntax as inputs (`/` everywhere, `\` escapes). Missing files/directories are ignored.

`{options.<name>}` resolves from the workspace root. If the option is unset or empty the output is dropped; list fallbacks after `??`, the first non-empty wins and the last may be a path: `{options.outputPath ?? {workspaceRoot}/dist/{projectRoot}}` caches `dist/apps/myapp` for a project at `apps/myapp`. Outputs cannot read environment variables, because they resolve once when the task graph is built.

Where to set them:
- `targetDefaults.<target>.outputs` in `nx.json` applies to all same-named targets.
- `targets.<target>.outputs` in `project.json` (or the `nx` key of `package.json`) applies to that project and is more specific.

Overrides replace; nothing merges. Both fully overwrite inferred plugin outputs, and project-level overwrites targetDefaults. So copy the existing array from the project details first, then edit.

Warning: avoid identical output locations across projects; use `{projectRoot}`/`{projectName}` to keep them unique.

To view a task's outputs: `nx build myapp --graph`, click the task, open the project details and read the outputs listed for the target (the page says the details screen refreshes as you edit).

## Checked

2026-11-07. Confirmed: the outputs tokens, defaults and glob rules against the Configure outputs page. Removed: the invented delete-and-rerun Verify step; kept the page-backed graph statement.

Method: documentation only; no commands were run.
