---
id: computing-software.software-engineering.go.cobra-command-trees-and-completions
name: cobra-command-trees-and-completions
category: computing-software
field: software-engineering
product: go
tags: [go, go-cli-config, go-cobra, cobra, spf13, completions]
level: practitioner
status: docs-checked
description: "Structure a Go CLI with cobra: root and sub-commands, persistent flags, RunE error handling, args validation and shell completions."
sources:
  - https://pkg.go.dev/github.com/spf13/cobra
  - https://cobra.dev/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Cobra command trees and completions

**Goal:** kubectl-style CLIs with good help and shell completion.

```go
var rootCmd = &cobra.Command{
    Use:           "mytool",
    Short:         "Manage things",
    SilenceUsage:  true,   // do not print usage on runtime errors
    SilenceErrors: true,   // print errors yourself in main
}
var verbose bool

func init() {
    rootCmd.PersistentFlags().BoolVarP(&verbose, "verbose", "v", false, "verbose output")
    rootCmd.AddCommand(serveCmd)
}

var serveCmd = &cobra.Command{
    Use:   "serve [addr]",
    Args:  cobra.MaximumNArgs(1),
    RunE: func(cmd *cobra.Command, args []string) error {
        ctx := cmd.Context()
        return serve(ctx, args)
    },
    ValidArgsFunction: func(*cobra.Command, []string, string) ([]string, cobra.ShellCompDirective) {
        return []string{"localhost:8080"}, cobra.ShellCompDirectiveNoFileComp
    },
}

func main() {
    if err := rootCmd.ExecuteContext(ctx); err != nil { fmt.Fprintln(os.Stderr, "error:", err); os.Exit(1) }
}
```

Cobra creates a default `completion` command (disable it with `CompletionOptions.DisableDefaultCmd`); cobra.dev lists Bash, Zsh, Fish and PowerShell completion. `RunE` returns an error to the caller, so use it instead of `Run` when errors should flow to `main`. `MarkFlagRequired` makes the command report an error if the flag is missing and prioritises it in completion. `ValidArgsFunction` supplies completions for non-flag arguments (only one of `ValidArgs` and `ValidArgsFunction` can be used), and `ShellCompDirectiveNoFileComp` turns off the default file completion. Persistent flags are inherited by subcommands. `cobra.MaximumNArgs(n)` returns an error if there are more than n args. To test, build the command in a function, call `cmd.SetArgs([]string{...})` and `cmd.SetOut(&buf)`, then `Execute()`.

## Gotchas
- Package-level command variables share state between tests; construct a fresh command tree per test.
- `SilenceUsage` and `SilenceErrors` suppress cobra's own usage and error output; if you set `SilenceErrors`, print the returned error yourself.
- `PersistentPreRun` and `PersistentPreRunE` exist as separate hooks; check the `Command` docs for which hooks run for child commands before relying on inheritance.

## Checked
2026-11-09. Confirmed on pkg.go.dev/github.com/spf13/cobra (`Command` fields `RunE`, `ValidArgsFunction`, `SilenceUsage`, `SilenceErrors`, `PersistentPreRun`, `CompletionOptions.DisableDefaultCmd`, `MaximumNArgs`, `MarkFlagRequired`, `ExecuteContext`, `Context`, `SetArgs`, `SetOut`, `ShellCompDirectiveNoFileComp`) and cobra.dev (persistent flags, shells supported).
Removed: the `EnablePersistentRunBeforeChildren` claim, Viper precedence order, and the `bash -n` and "nosuch" suggestion checks, none of which the pages state.
Method: documentation only; no commands were run.

## Verify
Run `mytool completion --help` to see the generated completion subcommands, and test the command tree with `SetArgs` and `SetOut`.
