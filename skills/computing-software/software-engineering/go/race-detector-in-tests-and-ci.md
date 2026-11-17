---
id: computing-software.software-engineering.go.race-detector-in-tests-and-ci
name: race-detector-in-tests-and-ci
category: computing-software
field: software-engineering
product: go
tags: [go, go-sync-memory, go-race-detector, race-detector, go-test-race]
level: practitioner
status: docs-checked
description: "Run the Go race detector in tests and CI, read its reports, budget its overhead and know its blind spots."
sources:
  - https://go.dev/doc/articles/race_detector
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# The race detector in tests and CI

**Goal:** make `-race` a routine gate.

```bash
go test -race mypkg                # test the package
go run -race mysrc.go              # run the source file
go build -race mycmd               # build an instrumented binary
GORACE="halt_on_error=1 history_size=2" ./mycmd
```

A report starts with `WARNING: DATA RACE` and shows the conflicting accesses (for example "Previous write by goroutine 184") with stacks. `GORACE` takes space-separated `option=val` pairs: `halt_on_error` (default 0) exits after the first reported race, and `history_size` (default 1) sets the per-goroutine access history to 32K * 2**history_size elements; raising it avoids "failed to restore the stack" errors at the cost of memory. The race detector requires cgo (and a C compiler on non-Darwin systems) and supports linux/amd64, linux/ppc64le, linux/arm64, linux/s390x, linux/loong64, freebsd/amd64, netbsd/amd64, darwin/amd64, darwin/arm64 and windows/amd64. Typical cost: memory 5-10x and execution time 2-20x.

CI recipe: run your tests with `-race`; because it only reports races that happen at run time, tests with incomplete coverage may miss races, so also run a `-race` binary under a realistic workload. Building with `-race` defines the `race` build tag.

## Gotchas
- It only finds races in code paths that actually execute.
- The detector allocates an extra 8 bytes per `defer` and `recover` statement until the goroutine exits, so a long-running goroutine that keeps calling them can grow memory without bound.
- On Windows, `-race` needs a C compiler with mingw-w64 runtime version 8 or later (as of Go 1.21).

## Verify
Add a test containing an intentional unsynchronised counter in a scratch package to confirm CI fails with "WARNING: DATA RACE", then remove it.

## Checked
2026-11-03. Confirmed on go.dev/doc/articles/race_detector: commands, report format, GORACE options and defaults, platform list, cgo requirement, 5-10x memory and 2-20x time, defer/recover allocation note, Windows compiler note, `race` build tag. Removed: "5 to 10 times the CPU" (page says 2-20x time), 8128-goroutine limit, `-shuffle` and `-count` advice, atomics logic-race claim, no-suppression claim, `go test -race -count=1 ./...` form.
Method: documentation only; no commands were run.
