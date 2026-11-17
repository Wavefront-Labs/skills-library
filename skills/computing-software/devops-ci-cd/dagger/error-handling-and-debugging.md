---
id: computing-software.devops-ci-cd.dagger.error-handling-and-debugging
name: error-handling-and-debugging
category: computing-software
field: devops-ci-cd
product: dagger
tags: [dagger, error-handling, debugging, terminal, exec-error, tracing, opentelemetry, concurrency]
level: practitioner
status: docs-checked
description: "Handle Dagger Function errors, keep using a container after a failed command, debug with terminal breakpoints, run steps concurrently and emit custom spans."
sources: [https://docs.dagger.io/0.21/extending/error-handling, https://docs.dagger.io/0.21/cookbook/errors, https://docs.dagger.io/0.21/cookbook/builds]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Error handling and debugging in Dagger modules

Goal: fail clearly, recover when you must, and inspect broken builds. Dagger 0.21 docs.

## Ordinary errors
Modules use the host language's error mechanism, which also validates user input. Go example:
```go
func (*MyModule) Divide(a, b int) (int, error) {
	if b == 0 { return 0, fmt.Errorf("cannot divide by zero") }
	return a / b, nil
}
```
`dagger call divide --a=4 --b=2` prints `2`; with `--b=0` it prints `cannot divide by zero`. Python raises `ValueError`, TypeScript throws `Error`.

## Catch a failed command
In Go, `errors.As` into `*dagger.ExecError` gives access to `Stderr`:
```go
out, err := dag.Container().From("alpine").WithExec([]string{"cat", "/"}).Stdout(ctx)
var e *dagger.ExecError
if errors.As(err, &e) { return fmt.Sprintf("Test pipeline failure: %s", e.Stderr), nil } else if err != nil { return "", err }
```

## Keep going after a failure
Allow any exit code, sync, then read the report and the exit code:
```go
ctr, err := dag.Container().From("alpine").
	WithNewFile("/run-tests", script, dagger.ContainerWithNewFileOpts{Permissions: 0o750}).
	WithExec([]string{"/run-tests"}, dagger.ContainerWithExecOpts{Expect: dagger.ReturnTypeAny}).
	Sync(ctx)
report := ctr.File("report.txt")
exitCode, err := ctr.ExitCode(ctx)
```
Return both in a custom type; `dagger call test exit-code` and `dagger call test report contents` read them. Caveat from the page: forcing a zero exit code caches the failure.

## Debug interactively
`Terminal()` opens an interactive shell on a container at that point; several terminals in one function open in sequence, and one also opens at the failure point. Example: `dag.Container().From("alpine:latest").Terminal().WithExec(...).Terminal()` run with `dagger call container`. Directories have `Terminal()` too (default container `alpine`); customise it: `Terminal(dagger.DirectoryTerminalOpts{Container: dag.Container().From("ubuntu"), Cmd: []string{"/bin/bash"}})`.

## Run steps concurrently
Use language concurrency (errgroup in Go, task groups in Python, promises in TypeScript). If one fails the rest are cancelled:
```go
eg, gctx := errgroup.WithContext(ctx)
eg.Go(func() error { _, err := m.Lint(gctx); return err })
eg.Go(func() error { _, err := m.Typecheck(gctx); return err })
eg.Go(func() error { _, err := m.Test(gctx); return err })
return eg.Wait()
```
Run: `dagger call --source=. run-all-tests`.

## Custom OpenTelemetry spans
`Tracer().Start(ctx, "running unit tests with Node "+version)` with `defer telemetry.End(span, func() error { return rerr })` (import `dagger/my-module/internal/telemetry`) adds spans to the TUI and Traces. Marked experimental and possibly replaced. Do not wrap lazily evaluated calls: their span duration will be zero, so the docs' snippet forces evaluation with `Sync(ctx)` inside the span.

Related: services-bind-expose-lifecycle.

## Checked

2026-11-07

Read in full from the docs source: extending/modules/error-handling.mdx, cookbook/errors.mdx and cookbook/builds.mdx with snippets. Added cookbook/builds as a source (the concurrency recipe). Reworded the span caveat to say the docs' snippet forces evaluation with Sync(ctx) inside the span.

Method: documentation only; no commands were run.
