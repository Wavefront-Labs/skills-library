---
id: computing-software.software-engineering.go.example-tests-and-testmain
name: example-tests-and-testmain
category: computing-software
field: software-engineering
product: go
tags: [go, golang, example-tests, testmain, testing-m, godoc, package-setup, testing]
level: practitioner
status: verified
description: "Write runnable Go Example functions that are verified and shown in godoc, and use TestMain for package-wide setup and teardown without breaking test flags."
sources: ["https://pkg.go.dev/testing#hdr-Examples", "https://pkg.go.dev/testing#hdr-Main", "https://go.dev/blog/examples"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Example tests and TestMain

**Goal:** documentation examples that are compiled and checked on every test run, and one
place for expensive package-level setup.

## Example functions
In a `_test.go` file (often package `foo_test` to use only the public API):
```go
func ExampleParse() {
    v, _ := semver.Parse("1.2.3")
    fmt.Println(v.Major, v.Minor)
    // Output: 1 2
}
```
`go vet` (run automatically by `go test`) fails the build when the suffix names no real identifier, e.g. `ExampleNoSuchFunc` is `refers to unknown identifier`; use `Example_suffix` for a package-level variant.
- `go test` runs examples that have an `// Output:` comment and compares stdout exactly
  (leading/trailing whitespace trimmed). Without the comment they are compiled but not run.
- `// Unordered output:` for map iteration or concurrent output.
- Naming controls where godoc attaches it: `Example` (package), `ExampleParse` (func),
  `ExampleVersion` (type), `ExampleVersion_String` (method), plus a lowercase suffix for variants:
  `ExampleParse_prerelease`.
- A test file is shown whole as the example when it holds a single example function, at least one other
  function/type/variable/constant declaration, and no test or benchmark functions.
- Examples cannot take parameters (`*testing.T` fails vet: `should be niladic`); keep them deterministic (no timestamps, random IDs, map order).

## TestMain
```go
func TestMain(m *testing.M) {
    // m.Run parses flags; call flag.Parse() yourself first if setup reads flags or testing.Short()
    // (testing.Short() before flag.Parse() panics)
    flag.Parse()
    pool, cleanup := startPostgres()
    testDB = pool
    code := m.Run()
    cleanup()           // runs before exit; a deferred call would NOT run if you call os.Exit
    os.Exit(code)
}
```
- One `TestMain` per package. It replaces the generated main, so it must call `m.Run()`.
- Since Go 1.15 you may simply `return` after `m.Run()` and the exit code is still used, which lets
  `defer cleanup()` work.
- Use it for expensive shared resources (container, compiled helper binary, golden server), not for
  per-test state - that belongs in helpers with `t.Cleanup`.
- Skip heavy setup under `-short` or when only examples/benchmarks run: check `testing.Short()`
  after `flag.Parse()`.
- Re-exec trick: TestMain can detect an env var and act as a helper subprocess (the pattern used for
  testing `os/exec` callers).

## Verify
- [ ] `go test -run Example -v` lists every example as PASS.
- [ ] `go doc` / pkg.go.dev shows examples attached to the right identifiers.
- [ ] Setup resources are released even when tests fail.

## Checked
2026-10-21 on Go 1.27.3 (Windows), scratch module: `ExampleParse`, `ExampleParse_prerelease`, `ExampleVersion_String`, `ExampleVersion` with `// Unordered output:` passed under `go test -v` (padding whitespace trimmed); an example without `// Output:` was compiled but not run (its panic never fired); `ExampleNoOutput` failed the vet step inside `go test` (`refers to unknown identifier`) and `ExampleParse_bad(t *testing.T)` failed it (`should be niladic`); `TestMain` that returns after `m.Run()` ran its deferred cleanup and a failing test still gave `FAIL` (exit code used); `testing.Short()` before `flag.Parse()` panicked (`Short called before Parse`) and worked after; a helper subprocess selected by an env var exited 3 as expected. Whole-file example rule and 'flag.Parse has not been run' from https://pkg.go.dev/testing.
