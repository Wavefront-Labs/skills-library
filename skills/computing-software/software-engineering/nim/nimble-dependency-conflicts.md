---
id: computing-software.software-engineering.nim.nimble-dependency-conflicts
name: nimble-dependency-conflicts
category: computing-software
field: software-engineering
product: nim
tags: [nimble-dependency-conflicts, nimble-lock-files, nimble-conflict, dependency-resolution, nimble-verbose, stale, troubleshooting, nimble-debug, nim]
level: practitioner
status: docs-checked
description: "Troubleshoot Nimble: refresh, uninstall, dump, nimble.ini proxy settings, SSL and macOS library errors, PATH, and resolver and solver options."
sources:
  - https://github.com/nim-lang/nimble
  - https://github.com/nim-lang/nimble/blob/master/nimble-guide/docs/troubleshooting.md
  - https://github.com/nim-lang/nimble/blob/master/nimble-guide/docs/nimble-reference.md
  - https://github.com/nim-lang/nimble/blob/master/nimble-guide/docs/config.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Nimble troubleshooting

Goal: resolve install and dependency problems.

- `nimble refresh` updates the package list (`--packageListOnly`; other commands accept `--refresh`).
- `nimble uninstall pkg[@ver]` errors if another package depends on it; `-i/--inclDeps` removes dependencies too. `nimble dump` prints package info.
- `nimble.ini`: `httpProxy`, `nimbleDir`, `[PackageList]`; proxies also via `http_proxy`/`https_proxy` environment variables.
- Troubleshooting page: SSL errors need `-d:ssl`; on macOS set `DYLD_LIBRARY_PATH` for missing libraries; "ambiguous identifier 'version'" needs Nim >= 0.16.0; `NIM_LIB_PREFIX` may be needed.
- `$nimbleDir/bin` must be on `PATH` to run installed binaries.
- Options: `--resolver:min|max`, `--solver:sat|pubgrub` (experimental), `--discovery:async|sync`, `--extra-requires`.

Gotchas:
- Conflicting version ranges: read the solver output and adjust `requires`.

Verify: `nimble install` completes.

## Checked

2026-11-03. Confirmed in the Nimble README, troubleshooting, reference and config pages. Removed: `--verbose/--debug`, asdf and choosenim advice, Windows long-path claim, an exact "Unsatisfiable dependency" message, and `nimble install nim@version`.
Method: documentation only; no commands were run.
