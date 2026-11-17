---
id: computing-software.software-engineering.go.vendoring-dependencies
name: vendoring-dependencies
category: computing-software
field: software-engineering
product: go
tags: [go, go-mod-vendor, vendoring, mod-vendor-flag, airgapped-builds, go-modules]
level: practitioner
status: verified
description: "Vendor Go dependencies with go mod vendor: when it is worth it, how -mod=vendor is selected automatically, keeping vendor/ in sync, workspaces, and reviewing vendored diffs."
sources: ["https://go.dev/ref/mod#vendoring", "https://go.dev/ref/mod#go-mod-vendor", "https://go.dev/ref/mod#build-commands"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Vendoring dependencies

**Goal:** builds that need no network or proxy, with dependency source reviewable in
the repo - without vendor/ drifting from go.mod.

## When to vendor
- Air-gapped or locked-down build environments with no module proxy access.
- Policy requires dependency source to be reviewed/stored in the repo.
- Protection against upstream deletion when you don't run a private proxy (Athens, Artifactory).
Otherwise prefer the module cache + `GOPROXY` + `go.sum` (already reproducible and verified);
vendoring bloats the repo and PR diffs.

## Create and update
```bash
go mod tidy
go mod vendor            # writes vendor/ and vendor/modules.txt
git add vendor go.mod go.sum
```
Re-run `go mod vendor` after every dependency change. `vendor/modules.txt` records which
module versions and packages are vendored; the go command checks it against go.mod.

## How builds use it
Since Go 1.14, if `vendor/modules.txt` exists and go.mod's `go` version is >= 1.14, build
commands default to `-mod=vendor` (no network, no module cache). Override:
```bash
go build -mod=mod ./...       # ignore vendor, use the module cache
go build -mod=vendor ./...    # force vendor
```
Inconsistency error ("go: inconsistent vendoring ...", with the hint to use `-mod=readonly` or `-mod=mod` to ignore vendor; tested) means go.mod changed
without re-vendoring - fix in the same commit.

## Workspaces
Go 1.22+ supports `go work vendor` for multi-module workspaces, producing a single vendor
directory at the workspace root.

## CI check
```bash
go mod tidy && go mod vendor
git diff --exit-code -- go.mod go.sum vendor/    # fails if someone forgot to vendor
```

## Reviewing
Vendored diffs can be huge; review go.mod/go.sum changes and the dependency's changelog, and
run `govulncheck ./...` (works on vendored builds). Never hand-edit files under vendor/ - they
are overwritten on the next `go mod vendor`; use a `replace` directive to a fork instead.

## Gotchas
- Only packages actually imported (plus their deps) are vendored, not whole modules. Packages imported by your own
  module's tests are included (tested: a `go-cmp` import used only in `_test.go` was vendored); tests of the dependencies themselves are not.
- Non-Go files in vendored packages (C sources for cgo, embed targets) are copied only when
  inside vendored package directories.
- `go mod vendor -e` continues past errors; `-o dir` writes elsewhere.

## Verify
- [ ] `go build -mod=vendor ./...` works with `GOFLAGS= GOPROXY=off`.
- [ ] CI fails when vendor/ is out of sync with go.mod.
