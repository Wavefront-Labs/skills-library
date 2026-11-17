---
id: computing-software.software-engineering.go.go-toolchain-directive-and-gotoolchain
name: go-toolchain-directive-and-gotoolchain
category: computing-software
field: software-engineering
product: go
tags: [go, go-modules, go-toolchain-directive, toolchain, gotoolchain, go-version]
level: practitioner
status: docs-checked
description: "Pin and upgrade Go toolchains with the go and toolchain directives, GOTOOLCHAIN modes and CI-safe settings."
sources:
  - https://go.dev/doc/toolchain
  - https://go.dev/ref/mod#go-mod-file-toolchain
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# go and toolchain directives (GOTOOLCHAIN)

**Goal:** make every developer and CI runner build with the same Go.

Since Go 1.21 the `go` line in `go.mod` is a **minimum** required version and is enforced. The optional `toolchain go1.23.4` line records the preferred toolchain. If the local `go` command is older than required, it downloads the needed toolchain (verified through the checksum DB) and re-executes.

```bash
go get go@1.23.0 toolchain@go1.23.4  # set the go and toolchain lines
go get go@1.24.0 toolchain@none     # bump minimum, drop the toolchain line
go env GOTOOLCHAIN                  # standard toolchains: auto (set in $GOROOT/go.env)
GOTOOLCHAIN=local go build ./...    # forbid switching/download (hermetic CI)
GOTOOLCHAIN=go1.22.7+path go test ./...
```

Values (`<name>` is `local` or a toolchain such as `go1.21.0`): `local` always runs the bundled toolchain; `auto` = `local+auto`, `path` = `local+path`; the `+auto` and `+path` forms may switch to a newer toolchain named by the `toolchain` or `go` line. `+path` only searches PATH (no download fallback); `auto` downloads. Downloads come from module `golang.org/toolchain` and are checked against the Go checksum database; with `GOSUMDB=off` they fail. Go 1.24+ can trace selection with `GODEBUG=toolchaintrace=1`.

## Gotchas
- With no `toolchain` line, the toolchain is implicitly `go` plus the version on the `go` line.
- Toolchain names are `go1.21.0` style: `go1.21` is not a toolchain name, the first release is `go1.21.0`. Write full `1.23.0`.
- Libraries should set the lowest `go` version they truly need; raising it forces all consumers to upgrade.
- Air-gapped builders must pre-install the toolchain or set `GOTOOLCHAIN=local` and fail loudly.
- `go get` and `go mod tidy` keep the `go` line at or above those of required dependencies.

## Verify
In a clean container run `go version` and `go env GOTOOLCHAIN`; the build log should show no download when the pinned version is installed.

## Checked
2026-11-03. Confirmed against go.dev/doc/toolchain: GOTOOLCHAIN forms and default, `go get ... toolchain@none`, download module and checksum DB, toolchaintrace, implicit toolchain line. Removed: wrong "default: local" (standard default is auto), unconfirmed `go mod edit -toolchain`, `go version -m` and loop-variable claims, the "go 1.21 means 1.21.0" gotcha.
Method: documentation only; no commands were run.
