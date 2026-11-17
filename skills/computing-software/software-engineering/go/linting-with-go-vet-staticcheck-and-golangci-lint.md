---
id: computing-software.software-engineering.go.linting-with-go-vet-staticcheck-and-golangci-lint
name: linting-with-go-vet-staticcheck-and-golangci-lint
category: computing-software
field: software-engineering
product: go
tags: [go, go-tooling, go-vet, staticcheck, golangci-lint, linting, ci]
level: practitioner
status: docs-checked
description: "Lint Go code with go vet, staticcheck and golangci-lint: which analyzers matter, v2 config, nolint discipline, new-code-only adoption and CI integration."
sources:
  - https://pkg.go.dev/cmd/vet
  - https://staticcheck.dev/docs/
  - https://golangci-lint.run/docs/
  - https://golangci-lint.run/docs/configuration/file/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Linting with go vet, staticcheck and golangci-lint

**Goal:** catch real bugs (not just style) on every change, with a configuration the team trusts enough not to `//nolint` everything.

## 1. go vet (always)
```bash
go vet ./...
```
Runs automatically (a subset: atomic, bools, buildtag, directive, errorsas, ifaceassert, nilfunc, printf, slog, stdversion, stringintconv, tests) during `go test`. Catches printf format mismatches, copied locks, unreachable code, struct tag errors, `errors.As` misuse, loop closure issues, `httpresponse` body misuse, and more. Zero config; treat findings as errors.

## 2. staticcheck
```bash
go install honnef.co/go/tools/cmd/staticcheck@latest
staticcheck ./...
```
Checks: `SA` (bugs, e.g. SA1019 deprecated API, SA4006 unused value, SA5011 nil deref), `S` (simplifications), `ST` (style), `QF` (quick fixes).

## 3. golangci-lint (aggregator)
```yaml
# .golangci.yml (v2 format)
version: "2"
linters:
  default: standard            # errcheck, govet, ineffassign, staticcheck, unused
  enable:
    - bodyclose
    - errorlint
    - gosec
    - noctx
    - revive
    - sqlclosecheck
    - contextcheck
    - misspell
  settings:
    errcheck:
      exclude-functions: [fmt.Fprintf]
  exclusions:
    rules:
      - path: _test\.go
        linters: [gosec]
formatters:
  enable: [gofumpt, goimports]
run:
  timeout: 5m
```
```bash
golangci-lint run ./...
golangci-lint run --new-from-rev=origin/main     # only issues in changed code: adopt on legacy repos
golangci-lint fmt
golangci-lint migrate                            # convert v1 config to v2
```
Pin the version in CI (`golangci/golangci-lint-action` with `version: v2.x.y`); new versions add checks.

## 4. Which extra linters earn their keep
- `errcheck`: unchecked errors (the big one).
- `errorlint`: `==` comparisons on wrapped errors, `%v` instead of `%w`.
- `bodyclose`, `sqlclosecheck`, `rowserrcheck`: resource leaks.
- `noctx`: HTTP requests without context.
- `gosec`: security smells (tune; noisy on tests).
Skip purely aesthetic linters until the team asks for them.

## 5. nolint discipline
```go
//nolint:gosec // G404: math/rand fine for jitter, not security
```
Require a linter name and reason (`nolintlint` linter enforces this).

## Gotchas
- Running golangci-lint without the module's build tags misses tagged files (`run.build-tags`).
- Generated code is excluded by default if it has the standard `// Code generated ... DO NOT EDIT.` header.
- The lint cache lives in a `golangci-lint` subdirectory of the user cache directory (override with `GOLANGCI_LINT_CACHE`); cache it in CI for speed.

## Verify
- CI fails on an unchecked error or a `%v`-wrapped error in a test PR, and `golangci-lint run` locally matches CI output (same version and config).

## Checked

2026-10-25. Checked against the Go source (cmd/go test default vet flags; the x/tools vet analyzer suite includes copylock, structtag, unreachable, errorsas, loopclosure, httpresponse), the staticcheck source (SA1019, SA4006 and SA5011 titles; getting-started `go install honnef.co/go/tools/cmd/staticcheck@latest`), and the golangci-lint repository (v2 reference config: `linters.default: standard`, `linters.settings`, `linters.exclusions.rules`, `formatters.enable` with gofumpt and goimports, `run.timeout`, `run.build-tags`, `errcheck.exclude-functions`; standard linters are errcheck, govet, ineffassign, staticcheck, unused; `fmt` and `migrate` commands; `--new-from-rev`; generated-file exclusion default `strict`; cache directory and `GOLANGCI_LINT_CACHE`; action example with `version: v2.13`). Removed unconfirmed opinions about signal quality and put the real list of vet checks that run under `go test`.

Method: documentation only; no commands were run.
