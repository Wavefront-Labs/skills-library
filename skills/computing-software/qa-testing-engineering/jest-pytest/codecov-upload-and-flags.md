---
id: computing-software.qa-testing-engineering.jest-pytest.codecov-upload-and-flags
name: codecov-upload-and-flags
category: computing-software
field: qa-testing-engineering
product: jest-pytest
tags: [codecov-upload, codecov, coverage-reporting-service, codecov-flags, codecov-yml]
level: practitioner
status: verified
description: "Upload coverage to Codecov from CI with the action/CLI, use flags and components for monorepos, configure codecov.yml project/patch status checks and fix missing uploads."
sources:
  - https://docs.codecov.com/docs/quick-start
  - https://docs.codecov.com/docs/codecovyml-reference
  - https://docs.codecov.com/docs/flags
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Uploading coverage to Codecov

## GitHub Actions
```yaml
- run: pytest --cov=src --cov-report=xml:coverage.xml
- uses: codecov/codecov-action@v5      # v5 tag exists; latest release at review time was v7.1.1, check the current major
  with:
    files: coverage.xml
    flags: backend
    token: ${{ secrets.CODECOV_TOKEN }}     # tokenless upload is unsupported except fork PRs to public repos (action README)
    fail_ci_if_error: true
```
Inputs `files`, `flags`, `token`, `fail_ci_if_error` and `override_commit` all exist in the action's `action.yml`. Accepted report formats are listed in the Codecov docs.

## codecov.yml
```yaml
coverage:
  status:
    project:
      default: { target: auto, threshold: 1% }      # don't drop overall by >1%
    patch:
      default: { target: 80% }                      # new/changed lines must be 80% covered
comment: { layout: "diff, flags, files", require_changes: true }
flags:
  backend: { paths: [services/api/], carryforward: true }
  frontend: { paths: [web/], carryforward: true }
ignore: ["**/migrations/**", "**/*.generated.ts"]
```
- **carryforward**: if a flag isn't uploaded in a commit (monorepo partial CI), reuse the last value instead of showing a drop.
- Validate: `curl --data-binary @codecov.yml https://codecov.io/validate` (ran it on the YAML above including `codecov.notify.after_n_builds` and `fixes`: `Valid!`).

## Multiple uploads
Upload per job/shard with the same commit SHA; Codecov merges them. Set `after_n_builds` in `codecov.notify` so status waits for all shards.

## Troubleshooting
| Problem | Fix |
|---|---|
| Paths don't match repo | coverage file has absolute/container paths: use `fixes:` path mapping in codecov.yml |

## Gotchas
- `fail_ci_if_error` defaults to `false` (checked in `action.yml`), which hides failed uploads: you'll see stale numbers.
- If commit detection picks the wrong SHA (for example on merge-commit checkouts), pass `override_commit` (an input of the action).

## Verify
PR shows Codecov project and patch statuses and the comment lists the flag(s).
