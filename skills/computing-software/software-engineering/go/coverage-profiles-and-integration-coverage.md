---
id: computing-software.software-engineering.go.coverage-profiles-and-integration-coverage
name: coverage-profiles-and-integration-coverage
category: computing-software
field: software-engineering
product: go
tags: [go, golang, go-coverage, coverprofile, covdata, gocoverdir, integration-tests, code-coverage]
level: practitioner
status: verified
description: "Measure Go coverage with -coverprofile, -coverpkg and atomic mode, read it with go tool cover, and collect integration coverage from binaries built with -cover."
sources: ["https://go.dev/doc/build-cover", "https://go.dev/blog/cover", "https://pkg.go.dev/cmd/cover", "https://pkg.go.dev/cmd/go#hdr-Testing_flags"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Coverage profiles and integration coverage

**Goal:** know which code your tests exercise, across packages and including end-to-end runs
of the real binary.

## Unit-test coverage
```bash
go test -cover ./...                                   # % per package
go test -coverprofile=cover.out -covermode=atomic ./...
go tool cover -func=cover.out | tail -1                # total: (statements) 78.4%
go tool cover -html=cover.out -o cover.html            # line-by-line view
```
- Modes: `set` (was the statement run), `count` (how often), `atomic` (count, safe with
  goroutines; it is the default when `-race` is enabled, otherwise the default is `set`).
- By default each package only counts coverage of **itself**. A test in `api/` that runs code
  in `store/` adds nothing for `store/`. Use `-coverpkg=./...` to attribute coverage across all
  packages in the module.
- Packages with no test files: since Go 1.22 `go test -cover` reports them as 0% instead of
  skipping, so totals are honest.

## Integration coverage (Go 1.20+)
Build the real binary with instrumentation, run it, and collect counters:
```bash
go build -cover -coverpkg=./... -o app ./cmd/app
mkdir -p covdata                              # GOCOVERDIR must already exist, or nothing is written
GOCOVERDIR=covdata ./app serve &       # run your e2e suite against it, then stop it gracefully
...
go tool covdata percent -i=covdata
go tool covdata textfmt -i=covdata -o integ.out   # legacy profile format
go tool cover -html=integ.out
```
- Counter files are written when the program exits via `os.Exit` or returns from `main`. A process
  killed with SIGKILL, or that ends in an unrecovered panic or fatal error, writes nothing; make the server handle SIGTERM and return from `main`. Long-running servers can flush
  on demand with `runtime/coverage.WriteCountersDir`.
- Merge unit and integration data: run unit tests with `-test.gocoverdir`:
```bash
go test -cover -coverpkg=./... ./... -args -test.gocoverdir=$PWD/unitcov
mkdir -p merged                                    # -o directory must exist
go tool covdata merge -i=unitcov,covdata -o merged
go tool covdata textfmt -i=merged -o all.out
```

## In CI
- Publish `cover.out` to Codecov/Coveralls or a PR comment; gate on **diff coverage** (new lines),
  not an absolute total that punishes legacy code.
- Exclude generated code by filtering the profile (`grep -v '_gen.go\|.pb.go'`) before reporting.

## Reading results well
Coverage shows what ran, not what was asserted. Look at the HTML for uncovered error branches and
boundary cases; 100% is not a goal, untested critical paths are the finding.

## Verify
- [ ] `go tool cover -func` total matches the CI badge.
- [ ] Integration run produces non-empty `covmeta`/`covcounters` files in GOCOVERDIR.
- [ ] Cross-package coverage uses `-coverpkg`.

## Checked
2026-10-21 on Go 1.27.3 (Windows): unit, `-coverpkg`, `-covermode=atomic`, `go tool cover -func/-html`, `go build -cover` + `GOCOVERDIR`, `covdata percent/textfmt/merge` and `-args -test.gocoverdir` all ran; packages without tests print `coverage: 0.0% of statements`; a missing `GOCOVERDIR` directory prints an error and writes nothing; `runtime/coverage.WriteCountersDir` exists (`go doc`). `-race` could not be run (needs cgo, no C compiler here); the atomic default under `-race` is from `go help testflag`. Not-written-on-panic/fatal behaviour is from https://go.dev/doc/build-cover.
