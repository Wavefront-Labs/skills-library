---
id: computing-software.software-engineering.go.tool-dependencies-and-go-generate
name: tool-dependencies-and-go-generate
category: computing-software
field: software-engineering
product: go
tags: [go, golang, go-modules, go-generate, go-tool-directive, code-generation, stringer, mockgen, sqlc, tools-go, go-generate-stringer, go-install-tools]
level: practitioner
status: verified
description: "Pin Go dev tools with the go.mod tool directive (Go 1.24+), run code generators via go:generate, and check generated code is up to date in CI."
sources: ["https://go.dev/doc/modules/managing-dependencies#tools", "https://go.dev/blog/generate", "https://pkg.go.dev/cmd/go#hdr-Generate_Go_files_by_processing_source", "https://go.dev/doc/go1.24#tools"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Tool dependencies and go generate

**Goal:** everyone and CI run the same versions of generators and linters, and generated
code never drifts from its source.

## Tool directive (Go 1.24+)
```bash
go get -tool golang.org/x/tools/cmd/stringer@v0.30.0
go get -tool github.com/sqlc-dev/sqlc/cmd/sqlc@v1.28.0
go tool stringer -type=Status     # run the pinned version
go get -tool -u ./...             # (with care) upgrade tools
```
go.mod gets:
```
tool (
    golang.org/x/tools/cmd/stringer
    github.com/sqlc-dev/sqlc/cmd/sqlc
)
```
Tools' dependencies are recorded in go.mod/go.sum like normal deps (they share the
dependency graph, which can force version bumps on your app deps; if that hurts, keep
heavy tools in a separate `tools/go.mod` and run with `go tool -modfile=tools/go.mod`).

Gotchas (tested on Go 1.24.0 and 1.27.2): `go get -tool pkg@latest` can raise the `go` line in go.mod (it went from 1.24 to 1.26.0 with a current x/tools), and an old pin can break on a newer toolchain (stringer v0.30.0 failed on Go 1.27.2 with `package "fmt" without types was imported`, worked on 1.24.0). Re-pin tools when you upgrade Go.

Before 1.24 the convention was a `tools.go` file with `//go:build tools` and blank
imports, then `go run pkg@version` or `go install`.

## go generate
```go
//go:generate go tool stringer -type=Status
//go:generate go tool mockgen -source=store.go -destination=mock_store_test.go -package=billing
type Status int
```
```bash
go generate ./...
```
- Directives run only when you call `go generate`; never automatically by build/test.
- Commands run in the package directory; `$GOFILE`, `$GOPACKAGE`, `$GOLINE` are set.
- No shell: `echo a | cat` printed the pipe literally (tested); pipes and globs need `sh -c "..."` (avoid for portability).
- Commit generated files (so `go install` users don't need generators); they start with
  `// Code generated ... DO NOT EDIT.` which linters and GitHub recognise.

## Drift check in CI
```bash
go generate ./...
git diff --exit-code     # fails if someone edited the source but didn't regenerate
```

## Verify
- [ ] `go version -m "$(go tool -n <name>)"` shows the pinned module version on a clean machine (not every tool has a `-version` flag; stringer does not).
- [ ] CI drift check passes.
