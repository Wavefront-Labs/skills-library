---
id: computing-software.devops-ci-cd.nx.nx-ultracache-target-config
name: nx-ultracache-target-config
category: computing-software
field: devops-ci-cd
product: nx
tags: [nx, nx-cloud, ultracache, ignorereads, ignorewrites, cache-inputs]
level: advanced
status: docs-checked
description: "Per-target ultracache settings: mode on/warn/error/off, collectStats, ignoreReads/ignoreWrites glob limits, always inputs, merge with spread token."
sources:
  - https://raw.githubusercontent.com/nrwl/nx/master/astro-docs/src/content/docs/reference/project-configuration.mdoc
  - https://raw.githubusercontent.com/nrwl/nx/master/astro-docs/src/content/docs/reference/inputs.mdoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: adjust how Nx Cloud Ultracache hashes one target from the files it actually read.

Mode table (`"ultracache": { "mode": "..." }`, default `on`):
| mode | records IO | reports undeclared access | applies recording |
| on | yes | no | yes |
| warn | yes | warns | no (hash from declared inputs) |
| error | yes | fails CI run | no |
| off | no | no | no |
Use `warn` for targets with dynamic behaviour or external state; `error` to fail when a target reads outside `inputs` or writes outside `outputs`; `off` to stop recording.

Other keys:
- `collectStats: true` includes successful stat metadata accesses in recorded inputs (default `false`); toggling reruns the task.
- `ignoreReads` / `ignoreWrites`: globs relative to workspace root; an excluded read does not count toward the hash even if the target declares the path with `includeIgnored`; an `always` input keeps its files in the hash either way. Changing `ignoreReads` reruns the task.
- Unsupported glob syntax is silently ineffective: no `*` in the first path segment (`**/generated/**` fails), no `?`, `!`, `[`, `]` or extglobs. Anchor instead: `libs/*/generated/**`.
- A target defining `ultracache` replaces inherited settings; merge with `"ultracache": { "...": true, "ignoreReads": ["...", "tmp/**"] }` (keys after `...` override).

`"always": true` on an input keeps its files in the hash: `{ "input": "production", "projects": ["checkout"], "always": true }`; works on `fileset`, `json`, `input` forms. With `always`, a `projects` pattern that matches nothing is an error.

Scope: only Nx Cloud records or applies IO; without it every mode behaves as `off`. Workspace-wide exclusions go in `.nx/workflows/ultracache-config.yaml` and combine with per-target patterns. Continuous tasks never get an Ultracache config. Env `NX_CLOUD_USE_ULTRACACHE=false` disables it for a run.

## Checked

2026-11-07. Confirmed against the Ultracache section of the project configuration reference and the inputs reference: the mode table and default on, the guidance for warn, error and off, collectStats default false and the rerun on change, ignoreReads and ignoreWrites as workspace-root globs, the ignoreReads rerun, the unsupported glob list and the libs/*/generated/** anchor, replacement versus spread merge with keys after the token overriding, always on inputs for fileset, json and input forms with the projects error, the Nx Cloud only note, .nx/workflows/ultracache-config.yaml combining with per-target patterns, continuous tasks never getting an Ultracache configuration, and NX_CLOUD_USE_ULTRACACHE. Removed: the wording that only always inputs survive an excluded read (page says an always input keeps its files either way), and the invented Verify step.

Method: documentation only; no commands were run.
