---
id: computing-software.qa-testing-engineering.jest-pytest.go-test-coverage
name: go-test-coverage
category: computing-software
field: qa-testing-engineering
product: jest-pytest
tags: [go-coverage, coverprofile, go-test, covermode, code-coverage]
level: practitioner
status: verified
description: "Measure Go test coverage with go test -cover, -coverprofile, -covermode and -coverpkg, view HTML reports, and collect integration coverage with go build -cover and GOCOVERDIR."
sources:
  - https://go.dev/blog/cover
  - https://go.dev/doc/build-cover
  - https://pkg.go.dev/cmd/go#hdr-Testing_flags
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Go test coverage

## Unit coverage
```bash
go test -cover ./...                                   # % per package
go test -coverprofile=cover.out -covermode=atomic ./...
go tool cover -func=cover.out | tail -1                # total: (statements) 82.4%
go tool cover -html=cover.out -o cover.html            # line highlighting
```
Modes: `set` (was it run), `count` (how many times), `atomic` (count, correct in multithreaded tests, more expensive). The default is `set`, or `atomic` when `-race` is on (`go help testflag`). `-race` needs cgo, so it could not be run here.

## Cross-package coverage
By default a package's tests only count coverage for that package. Integration-style tests in `./tests` exercising `./internal/...`:
```bash
go test -coverpkg=./... -coverprofile=cover.out ./...
```

## Integration / binary coverage (Go 1.20+)
```bash
go build -cover -o app ./cmd/app
mkdir -p covdata && GOCOVERDIR=covdata ./app &   # run e2e tests against it, then stop the app gracefully
go tool covdata percent -i=covdata
go tool covdata textfmt -i=covdata -o e2e.out     # convert to legacy profile for tools
mkdir -p merged && go tool covdata merge -i=covdata,unitcov -o merged   # the output directory must already exist
```
Unit tests can also write raw data: `go test -cover ./... -args -test.gocoverdir=$PWD/unitcov`.

## CI gate
```bash
total=$(go tool cover -func=cover.out | awk '/^total:/ {print substr($3, 1, length($3)-1)}')
awk -v t="$total" 'BEGIN { exit (t < 80) }' || { echo "coverage $total% < 80%"; exit 1; }
```

## Gotchas
- Generated code (`*.pb.go`, mocks) inflates or deflates numbers: filter lines from `cover.out` before computing (`grep -v '.pb.go'`).
- Binary coverage data is written only when `main` returns or calls `os.Exit`; an unrecovered panic or fatal error loses it (Go docs, build-cover FAQ). A kill signal will too.
- Statement coverage only: Go has no branch coverage built in.

## Verify
`go tool cover -func` total matches what CI reports; HTML shows red lines where expected. All commands above were run on Go 1.22.5 (merged unit and binary data reported 75% for a package that unit tests alone covered at 50%).
