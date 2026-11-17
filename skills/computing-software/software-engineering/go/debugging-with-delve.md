---
id: computing-software.software-engineering.go.debugging-with-delve
name: debugging-with-delve
category: computing-software
field: software-engineering
product: go
tags: [go, golang, delve-debugger, dlv, debugging, breakpoints, core-dumps, remote-debugging, vscode-go]
level: practitioner
status: gated
description: "Debug Go programs and tests with Delve: dlv debug/test/attach/core, breakpoints and conditions, goroutine inspection, headless remote sessions and optimisation flags."
sources: ["https://github.com/go-delve/delve/tree/master/Documentation/usage", "https://github.com/go-delve/delve/blob/master/Documentation/cli/README.md", "https://github.com/golang/vscode-go/wiki/debugging"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Debugging Go with Delve

**Goal:** stop a Go program at the right moment and inspect goroutines and variables, locally,
in tests, in containers, or post-mortem.

## Install and start
```bash
go install github.com/go-delve/delve/cmd/dlv@latest
dlv debug ./cmd/app -- --config dev.yaml      # build with debug flags and run
dlv test ./pkg/store -- -test.run TestSave    # debug a test
dlv attach <pid>                              # running process (needs ptrace permission) (gated: unconfirmed, source is paywalled or blocked)
dlv exec ./app                                # prebuilt binary
dlv core ./app core.1234                      # post-mortem from a core dump
```
`dlv debug/test` build with `-gcflags="all=-N -l"` (no optimisation, no inlining) so variables
are visible. For `dlv exec`/`attach`, build the binary the same way yourself, otherwise you will see
"optimized away" variables and skipped lines.

## Core commands
```
(dlv) break main.go:42            # b; also b pkg.Func, b (*Type).Method
(dlv) condition 1 user.ID == 7    # conditional breakpoint
(dlv) on 1 print req.URL.Path     # run a command each hit
(dlv) trace pkg.Func              # tracepoint: log without stopping
(dlv) continue | next | step | stepout     (c, n, s, so)
(dlv) print x | locals | args | whatis x
(dlv) set x = 5                       # x must already be in scope (declared) at the stop
(dlv) goroutines -with user       # list; filters: -with/-without running, user, label
(dlv) goroutine 18 bt             # stack of another goroutine
(dlv) frame 2 locals
(dlv) restart | exit
```
- `goroutines -group userloc` summarises thousands of goroutines by location: the fastest way to
  diagnose a deadlock or leak in a hung process.
- `config max-string-len 1000` and `config max-array-values 200` to see more data.
- Delve already installs `unrecovered-panic` and `runtime-fatal-throw` breakpoints (see `breakpoints`), so a panic stops the program under the debugger without setting your own.

## Headless and remote
```bash
dlv debug --headless --listen=:2345 --api-version=2 --accept-multiclient ./cmd/app
dlv connect localhost:2345
```
In containers (gated: unconfirmed, source is paywalled or blocked): build with `-gcflags="all=-N -l"`, run under dlv headless, expose the port, and add
`--cap-add=SYS_PTRACE` (and seccomp unconfined if needed) for attach. Never leave a Delve port
exposed in production: it allows arbitrary code execution.

## Editors
VS Code Go extension uses Delve via DAP (`dlv dap`); launch configs: `"mode": "debug" | "test" |
"exec" | "remote"`. GoLand bundles Delve.

## Core dumps
`GOTRACEBACK=crash ./app` makes a fatal error dump core (with `ulimit -c unlimited`), or use
`gcore <pid>` on a hung process, then `dlv core` (gated: unconfirmed, source is paywalled or blocked). Inspect all goroutines without the process
running.

## Gotchas
- Breakpoints in inlined functions may not hit in optimised binaries.
- To debug code inside a goroutine, set a breakpoint inside it; a breakpoint in a `go func(){...}()` body hit in a different goroutine (g7) than the one that started it (g1).
- Timeouts in code under test fire while you sit at a breakpoint; raise them or use `-test.timeout 0`.

## Verify
- [ ] You can list goroutines and print locals in the frame of interest.
- [ ] Remote session connects and breakpoints resolve (`breakpoints` shows addresses, not pending).

## Checked
2026-10-21, Delve 1.27.2 on Go 1.27.3 (Windows): `dlv debug` with an init file ran break, condition (stopped only at `u.ID == 7`), on, trace, continue, args, locals, config, breakpoints, frame, stepout, `goroutines -with user`, `goroutines -group userloc`, `goroutine 1 bt`; `dlv test . -- -test.run TestA` and `dlv exec` on a `-gcflags="all=-N -l"` binary hit breakpoints; headless `--listen --api-version=2 --accept-multiclient` plus `dlv connect` worked (processes stopped afterwards); `dlv core` help says it supports Linux and Windows core dumps; Delve's built-in `unrecovered-panic` breakpoint is listed by `breakpoints`. Not run: attach/ptrace, core dumps with `GOTRACEBACK=crash`/`gcore`, container flags, VS Code DAP (no Linux, no Docker).
