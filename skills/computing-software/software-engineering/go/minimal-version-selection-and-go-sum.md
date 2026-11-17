---
id: computing-software.software-engineering.go.minimal-version-selection-and-go-sum
name: minimal-version-selection-and-go-sum
category: computing-software
field: software-engineering
product: go
tags: [go, go-modules, go-mvs, mvs, go-sum, minimal-version-selection]
level: practitioner
status: docs-checked
description: "Explain how Go module resolution picks versions (MVS), what go.sum verifies, and how to upgrade deliberately."
sources:
  - https://go.dev/ref/mod#minimal-version-selection
  - https://go.dev/ref/mod#go-sum-files
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Minimal version selection and go.sum

**Goal:** predict which dependency versions you get and why builds are reproducible.

MVS starts at the main module and traverses the module graph, tracking the **highest required version of each module**. Those highest required versions form the build list: the minimum versions that satisfy all requirements.

```bash
go list -m all                     # the build list (selected versions)
go mod graph                       # requirement graph, one "module dependency" edge per line
go mod why -m golang.org/x/text    # why is this module needed
go get example.com/lib@v1.4.2      # raise a requirement
go get -u=patch ./...              # upgrade dependencies to the latest patch version
go mod tidy                        # sync go.mod/go.sum with imports
go mod verify                      # cached modules unmodified since download
```

`go.sum` records checksums (lines of `module version h1:...`) used to authenticate downloaded modules. `sum.golang.org` is the public checksum database, run by Google, a transparent (Merkle tree) log of `go.sum` line hashes; `GONOSUMDB` lists path prefixes that should not be checked against it. Commit both `go.mod` and `go.sum`.

## Gotchas
- `replace` and `exclude` directives apply only in the main module's `go.mod` and are ignored in other modules.
- Since Go 1.16 the go command acts as if `-mod=readonly` were set: if `go.mod` needs changes it reports an error and suggests a fix instead of editing the file.
- `go mod tidy` records in `go.sum` the checksums needed by the Go version one below the `go` directive (the `-compat` flag overrides this).
- `go mod verify` prints "all modules verified" or reports which modules changed and exits non-zero.

## Verify
`go mod verify` confirms cached modules still match their recorded hashes; `go build -mod=readonly ./...` in CI fails if `go.mod` would need changes.

## Checked
2026-11-03. Confirmed on go.dev/ref/mod: MVS description, `go mod graph`, `go mod why`, `go mod verify`, `go get -u=patch`, `replace`/`exclude` main-module-only, `-mod=readonly` default since 1.16, checksum database (sum.golang.org, GONOSUMDB), go.sum compat note. Removed: "go.mod acts as the lock" and "adding a dependency never upgrades others" claims, `GOFLAGS=-mod=mod`, `// indirect` and pruning advice, go.sum merge-conflict advice, `h1:` of zip/go.mod split.
Method: documentation only; no commands were run.
