---
id: computing-software.software-engineering.go.flag-package-subcommands-and-usage
name: flag-package-subcommands-and-usage
category: computing-software
field: software-engineering
product: go
tags: [go, go-cli-config, go-flag-package, flag, subcommands, cli]
level: practitioner
status: docs-checked
description: "Build small Go CLIs with the flag package: FlagSet subcommands, custom Value types, usage text and exit codes."
sources:
  - https://pkg.go.dev/flag
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# flag package patterns and subcommands

**Goal:** a dependency-free CLI with subcommands and predictable exit codes.

```go
func main() { os.Exit(run(os.Args[1:], os.Stdout, os.Stderr)) }

func run(args []string, out, errw io.Writer) int {
    if len(args) == 0 { fmt.Fprintln(errw, "usage: tool <serve|migrate> [flags]"); return 2 }
    switch args[0] {
    case "serve":
        fs := flag.NewFlagSet("serve", flag.ContinueOnError)
        fs.SetOutput(errw)
        addr := fs.String("addr", ":8080", "listen address")
        var tags stringList
        fs.Var(&tags, "tag", "repeatable tag")
        if err := fs.Parse(args[1:]); err != nil { return 2 }
        return serve(*addr, tags, out)
    }
    return 2
}

type stringList []string
func (s *stringList) String() string     { return strings.Join(*s, ",") }
func (s *stringList) Set(v string) error { *s = append(*s, v); return nil }
```

Using `ContinueOnError` and injected writers makes `run` unit-testable; the default `ExitOnError` of the global `flag.CommandLine` calls `os.Exit(2)`. Flags must come **before** positional arguments (parsing stops at the first non-flag); use `fs.Args()` for the rest. Both `-x` and `--x` work; `-x=1`, `-x 1` for non-bool flags; booleans need `-b=false`.

## Gotchas
- One or two dashes are equivalent, so `-addr` and `--addr` behave the same.
- `flag.Duration` and `flag.TextVar` (added in 1.19) cover durations and `encoding.TextMarshaler`/`TextUnmarshaler` types; custom flags implement `flag.Value` (`String` and `Set`, with pointer receivers).
- Parse environment variables yourself as defaults: `os.LookupEnv`.

## Verify
Table-test `run` with args such as `serve -addr :0` and with an unknown flag, checking the exit code and what was written to the injected writers.

## Checked
2026-11-03. Confirmed on pkg.go.dev/flag: `NewFlagSet`, `ContinueOnError`/`ExitOnError`, `SetOutput`, `Var` and the `Value` interface, `Args`, `Duration`, `TextVar` (go1.19), the `-flag=x` / `-flag x` / `--flag` forms, boolean `-flag=false`, parsing stops at the first non-flag argument. Removed: claim that flag has no aliases or grouping and the cobra/kong recommendation, "unknown flag returns 2 with usage on stderr" (the code, not the package, picks the exit code). `os.LookupEnv` from pkg.go.dev/os.
Method: documentation only; no commands were run.
