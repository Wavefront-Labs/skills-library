---
id: computing-software.devops-ci-cd.dagger.checks-create
name: checks-create
category: computing-software
field: devops-ci-cd
product: dagger
tags: [dagger, checks, check-annotation, functions, go, python, typescript, lint]
level: practitioner
status: docs-checked
description: "Write a Dagger check function in Go, Python or TypeScript using +check, @check or @check(), with optional arguments and defaultPath, and the rules for what it may take."
sources: [https://docs.dagger.io/0.21/introduction/core-concepts/checks, https://docs.dagger.io/0.21/getting-started/quickstarts/ci/]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Create a Dagger check

Goal: mark a function as a check so `dagger check` discovers it (Dagger 0.21 docs).

## Rules from the docs

- A check must not require arguments; optional arguments (for example severity, test filter) are allowed.
- It may return an error (pass/fail) or a container for tools that produce exit codes; the examples use error, void or None returns.

## Go: the `+check` comment annotation

```go
// Runs linting checks on the code
// +check
func (m *MyModule) LintCode(ctx context.Context) error {
    _, err := dag.Container().
        From("golangci/golangci-lint:latest").
        WithExec([]string{"golangci-lint", "run"}).
        Sync(ctx)
    return err
}

// +check
func (m *MyModule) SecurityScan(
    ctx context.Context,
    // +optional
    // +default="HIGH,CRITICAL"
    severity string,
) error { /* trivy fs --severity ... */ }
```

## Python: `@function` plus `@check` (from dagger import check)

```python
@function
@check
async def lint_code(self) -> None:
    await dag.container().from_("golangci/golangci-lint:latest").with_exec(["golangci-lint", "run"]).sync()
```

## TypeScript: `@func()` plus `@check()` (import check from @dagger.io/dagger)

```typescript
@func()
@check()
async lintCode(): Promise<void> {
  await dag.container().from("golangci/golangci-lint:latest").withExec(["golangci-lint", "run"]).sync()
}
```

## Check that depends on source (CI quickstart)

Give the source argument a default so it is optional:
```go
// +check
func (m *HelloDagger) ValidateBuild(
    ctx context.Context,
    // +optional
    // +defaultPath="/"
    // +ignore=[".git", "node_modules"]
    source *dagger.Directory,
) error {
    _, err := m.Build(source).Sync(ctx)
    return err
}
```
Python uses `Annotated[dagger.Directory, DefaultPath("/"), Ignore([".git", "node_modules"])] = None`; TypeScript uses `@argument({ defaultPath: "/", ignore: [".git", "node_modules"] })`. Then run `dagger check` (and `dagger check -l`).

The docs show only Go, Python and TypeScript for checks.

Related: `computing-software.devops-ci-cd.dagger.checks-run-filter`.

## Checked

2026-11-07

Read in full from the docs source: introduction/core-concepts/checks.mdx, introduction/core-concepts/index.mdx and getting-started/quickstarts/ci/index.mdx (Validate your workflow with checks). Confirmed the +check, @check and @check() forms, the optional-argument rule, the severity example, the ValidateBuild example with defaultPath and ignore, and dagger check and dagger check -l. No corrections needed.

Method: documentation only; no commands were run.
