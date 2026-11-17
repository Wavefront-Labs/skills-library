---
id: computing-software.software-engineering.go.test-helpers-cleanup-parallel-and-testdata
name: test-helpers-cleanup-parallel-and-testdata
category: computing-software
field: software-engineering
product: go
tags: [go, golang, testing, t-parallel, t-cleanup, t-helper, t-tempdir, testdata, t-context, go-test, go-golden-files]
level: practitioner
status: docs-checked
description: "Write Go test helpers with t.Helper, t.Cleanup, t.TempDir, t.Setenv and t.Context, run tests in parallel safely, and keep fixtures in testdata/."
sources: ["https://pkg.go.dev/testing", "https://pkg.go.dev/cmd/go#hdr-Test_packages", "https://go.dev/doc/go1.24#testing"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Test helpers, cleanup, parallelism and testdata

**Goal:** short tests with reusable setup that cleans up after itself, failure lines that
point at the caller, and parallel runs that do not interfere.

## Helpers
```go
func newTestDB(t *testing.T) *sql.DB {
    t.Helper()                          // failures report the caller's line, not this one
    db, err := sql.Open("sqlite", filepath.Join(t.TempDir(), "test.db"))
    if err != nil {
        t.Fatalf("open: %v", err)       // Fatal is fine in helpers that take t
    }
    t.Cleanup(func() { db.Close() })    // runs after the test and all its subtests
    return db
}
```
- `t.Cleanup` functions run LIFO after the test (and its parallel subtests) complete. Prefer it
  over returning a `teardown func()` the caller must remember to defer.
- `t.TempDir()` creates a unique directory removed automatically.
- `t.Setenv("KEY", "v")` restores the old value afterwards; it cannot be used in a test that called
  `t.Parallel()` because the environment is process-wide.
- `t.Chdir(dir)` (Go 1.24) changes directory for the test and restores it; also not parallel-safe.
- `t.Context()` (Go 1.24) returns a context cancelled just before Cleanup functions run - pass it
  to code under test instead of `context.Background()`.
- Never call `t.Fatal` from a goroutine other than the test's own; use `t.Error` and return, or send
  the error back on a channel.

## Parallel tests
```go
func TestParse(t *testing.T) {
    t.Parallel()
    for _, tc := range cases {
        t.Run(tc.name, func(t *testing.T) {
            t.Parallel()     // Go 1.22+: tc is per-iteration, no tc := tc needed
            ...
        })
    }
}
```
- Parallel tests pause until the sequential part of every top-level test finishes, then run up to
  `-parallel` (default GOMAXPROCS) at once.
- Shared fixtures (a database, a port, a global var) must be isolated per test or the test must not
  be parallel. Use unique schema/table names or temp dirs.
- A Cleanup on the parent runs only after all its parallel subtests finish, so parent-level setup
  is safe to share read-only.

## testdata/
- Keep fixtures in a `testdata/` directory beside the test files and load them by relative path.
- Golden files: compare output to `testdata/name.golden`; regenerate with an `-update` flag:
```go
var update = flag.Bool("update", false, "update golden files")
if *update { os.WriteFile(golden, got, 0o644) }
```
- `fstest.MapFS` for code that takes an `fs.FS`.

## Useful go test flags
`-run 'TestParse/empty'`, `-count=1` (bypass cache), `-shuffle=on`, `-failfast`, `-v`,
`-timeout 2m`, `-short` (check `testing.Short()` to skip slow tests).

## Verify
- [ ] `go test -shuffle=on -count=3 -race ./...` passes (order and parallelism independent).
- [ ] No leftover files or env changes after the run.
- [ ] Helper failures point at the calling test line.

## Checked

- Date: 2026-10-28
- Confirmed on pkg.go.dev/testing, cmd/go test flags and the Go 1.22/1.24 release notes: t.Cleanup order (last added, first called), t.Context (1.24), t.Chdir (1.24), t.Setenv not usable in parallel tests, -parallel default GOMAXPROCS, -shuffle, -count, per-iteration loop variables (1.22), testing/fstest.MapFS.
- Removed: claim that the go tool ignores testdata and the working-directory remark, os.DirFS.
Method: documentation only; no commands were run.
