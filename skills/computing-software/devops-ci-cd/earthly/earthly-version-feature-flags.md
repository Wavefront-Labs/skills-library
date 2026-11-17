---
id: computing-software.devops-ci-cd.earthly.earthly-version-feature-flags
name: earthly-version-feature-flags
category: computing-software
field: devops-ci-cd
product: earthly
tags: [earthly, version, feature-flags, referenced-save-only, use-copy-include-patterns, for-in, wait-block, try]
level: advanced
status: docs-checked
description: "Declare the Earthfile VERSION with feature flags, check binary versus Earthfile compatibility, upgrade to VERSION 0.8 safely, and understand key flags like --referenced-save-only."
sources:
  - https://github.com/earthly/earthly/blob/main/docs/earthfile/features.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Earthfile VERSION and feature flags

Goal: pin an Earthfile to a version and opt into features safely.

```Dockerfile
VERSION [<flags>...] <version-number>
```
`VERSION` was introduced in 0.5 and is required as of 0.7. Feature flags are for testing experimental features; using them opts out of forwards/backwards semver guarantees, so the same script may behave differently on another Earthly version. Avoid them for critical workflows.

## Binary vs Earthfile versions
| Earthly binary | Supported Earthfile VERSIONs |
|---|---|
| 0.8.x | 0.6, 0.7, 0.8 |
| 0.7.x | 0.5, 0.6, 0.7 |
| 0.6.x | none specified (0.5 implied), 0.5, 0.6 |
| 0.5.x | none specified (0.5 implied), 0.5 |
| below 0.5 | `VERSION` not supported |

Newer Earthfiles cannot run on older binaries.

## Safe upgrade to VERSION 0.8
1. If still on `VERSION 0.5`, move those Earthfiles to 0.6 or 0.7.
2. Upgrade the Earthly binary to 0.8 in CI and across the team.
3. Then upgrade Earthfiles one by one to `VERSION 0.8`; mixing 0.6, 0.7 and 0.8 Earthfiles in a project is fine.

Expect backwards-incompatible changes between versions; read each release change log.

## Selected flags (status column = version where enabled by default)
- `--use-copy-include-patterns` (0.6): send only the files listed in each `COPY`, instead of the whole directory minus `.earthlyignore`.
- `--referenced-save-only` (0.6): outputs from `SAVE ARTIFACT ... AS LOCAL`, `SAVE IMAGE` and `RUN --push` happen only if connected to the main target through a chain of `BUILD` commands (main -> BUILD -> SAVE works; main -> FROM -> SAVE or main -> COPY -> SAVE does not).
- `--for-in` (0.6): enables `FOR ... IN ...`.
- `--wait-block` (0.7): `WAIT` / `END`. `--use-cache-command`, `--use-host-command` (0.7).
- `--arg-scope-and-set` (0.8): `LET` / `SET` and nested `ARG` scoping. `--pass-args`, `--global-cache`, `--use-function-keyword` (0.8).
- Experimental: `--try` (`TRY` / `FINALLY` / `END`), `--wildcard-copy`, `--wildcard-builds`, `--run-with-aws`, `--raw-output`.

## Gotcha
Flags are disabled by default in Earthly versions lower than the one in the status column.

## Checked

2026-11-07. Read docs/earthfile/features.md in full. The compatibility table, upgrade steps, VERSION requirement and feature-flag version table match. Nothing removed.
Method: documentation only; no commands were run.
