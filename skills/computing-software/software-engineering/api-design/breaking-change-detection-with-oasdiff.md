---
id: computing-software.software-engineering.api-design.breaking-change-detection-with-oasdiff
name: breaking-change-detection-with-oasdiff
category: computing-software
field: software-engineering
product: api-design
tags: [api-design, oasdiff, breaking-changes, openapi-diff, ci, api-compatibility, changelog]
level: practitioner
status: docs-checked
description: "Catch breaking OpenAPI changes in CI with oasdiff: compare base and head specs, read breaking versus changelog output, and fail pull requests."
sources: ["https://github.com/oasdiff/oasdiff/blob/main/docs/README.md", "https://github.com/oasdiff/oasdiff/blob/main/docs/BREAKING-CHANGES.md", "https://github.com/oasdiff/oasdiff/blob/main/docs/GIT-REVISION.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Breaking-change detection with oasdiff

oasdiff compares two OpenAPI specs and classifies differences. Local files, http/s URLs, YAML or JSON, and git revisions are all accepted as inputs.

## Commands
```bash
# compare the base branch spec with the working copy (git revision syntax: <ref>:<path>)
oasdiff breaking origin/main:openapi.yaml openapi.yaml
oasdiff breaking origin/main:openapi.yaml openapi.yaml --fail-on ERR   # exit code 1 on ERR changes
oasdiff changelog origin/main:openapi.yaml openapi.yaml   # breaking and non-breaking, human-readable
oasdiff diff origin/main:openapi.yaml openapi.yaml        # full diff, including documentation-only edits
```
Run it from inside the git repository that holds the spec. If the base commit is missing (shallow clone), oasdiff prints the `git fetch` to run; `--fetch` does it for you.

## Levels
Each check has a level: `ERR` (definite breaking change), `WARN` (potentially breaking, cannot be confirmed from the definition) or `INFO` (non-breaking). `breaking` reports only ERR and WARN; `changelog` reports at or above `--level` (default `INFO`, everything). `--fail-on` takes `ERR`, `WARN` or `INFO` and exits with code 1 when changes at or above that level are found. `oasdiff checks changelog` lists the rules and their default levels; `--severity-levels FILE` changes a check's level.

## CI sketch
The GitHub Action form (needs full history, so `fetch-depth: 0` on checkout):
```yaml
- uses: oasdiff/oasdiff-action/breaking@v0
  with:
    base: 'origin/${{ github.base_ref }}:openapi.yaml'
    revision: 'HEAD:openapi.yaml'
```
Deliberate breaks go in a new API version with a deprecation period.

## Gotchas
- Breaking depends on direction: adding a required request field breaks callers; changes to response shapes can break strict clients. See the tolerant-reader skill.
- A change inside `allOf` compared without `--flatten-allof` is reported at `WARN` even where its check says `ERR`, because branches are compared one at a time.
- Specs generated from code can reorder or rename components and produce noisy diffs; the docs describe normalisation options (allOf merging, path-prefix, header case).
- It only sees the contract. Behavioural changes (semantics, limits) pass undetected.

Verify: remove a response field in a throwaway copy of the spec and confirm `oasdiff breaking ... --fail-on ERR` exits non-zero and names the change.

## Checked
2026-11-08. Confirmed against the oasdiff docs README, BREAKING-CHANGES.md (read by targeted search only, not in full: levels, `--fail-on`, `--level`, `--severity-levels`, allOf caveat) and GIT-REVISION.md (`<ref>:<path>`, `--fetch`, Action example, `fetch-depth: 0`). Removed: the temp-file `git show` steps, the claim that output rows carry a rule id, the Sunset-header reference, and the oasdiff.com landing page source.
Method: documentation only; no commands were run.
