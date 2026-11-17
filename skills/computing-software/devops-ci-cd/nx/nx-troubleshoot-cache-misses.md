---
id: computing-software.devops-ci-cd.nx.nx-troubleshoot-cache-misses
name: nx-troubleshoot-cache-misses
category: computing-software
field: devops-ci-cd
product: nx
tags: [nx, caching, troubleshooting, cache-miss, nx-cloud, inputs]
level: practitioner
status: docs-checked
description: "Diagnose why an Nx task re-runs instead of replaying cache: cacheable flag, outputs altering inputs, graph file listing, and Nx Cloud Compare to similar tasks."
sources:
  - https://raw.githubusercontent.com/nrwl/nx/master/astro-docs/src/content/docs/kb/troubleshoot-cache-misses.mdoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Problem: a task executes when you expected a cache replay.

Check 1, is the task cacheable?
- `nx show project <project-name> --web` should show a "Cacheable" label on the task (Nx Console project details shows the same).
- The target must have `"cache": true`, in the project's `project.json` or in `nx.json#targetDefaults`.

Check 2, does the task's own output change its inputs?
- Review `inputs` and `namedInputs` in project config and root `nx.json`; inputs decide execute vs replay (see nx-input-types, nx-named-inputs).
- `outputs` only controls which files are restored, not whether the cache is used, but an output file not captured by `outputs` could be modifying one of the task's inputs.
- List the files each project hashes: `nx graph --file=output.json`, or click a task in the `nx graph` task graph.

Check 3, Nx Cloud troubleshooting tools (the repo must be connected to Nx Cloud):
1. Open the run details link printed in the terminal; filter tasks by cache status to find the miss.
2. Open the task and click "Compare to similar tasks".
3. Pick a similar task, or paste a run URL for a specific run.
4. Nx Cloud diffs the hash inputs and highlights differences.

Limitation: Nx Cloud cannot see your source, so it reports which inputs differ by saved content hash, not a git diff.

## Checked

2026-11-07. Confirmed against Troubleshoot Cache Misses: the three checks, the Cacheable label via nx show project --web or Nx Console, cache true in project.json or nx.json#targetDefaults, inputs and namedInputs deciding execute versus replay, outputs only controlling replayed files, nx graph --file=output.json and the task graph, the Nx Cloud run details link, filter by cache status, Compare to similar tasks, choosing a run or pasting a URL, hash input diff, and the note that Nx Cloud cannot see source and shows saved content hashes. Removed: the claim about files generated inside an input glob (not on the page), the stated consequence of a miss on the next run, and the invented Verify step.

Method: documentation only; no commands were run.
