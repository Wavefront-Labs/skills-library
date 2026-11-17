---
id: computing-software.devops-ci-cd.dagger.module-testing-patterns
name: module-testing-patterns
category: computing-software
field: devops-ci-cd
product: dagger
tags: [dagger, testing, modules, test-module, examples, all-function, daggerverse, go, python, typescript]
level: practitioner
status: docs-checked
description: "Test Dagger modules with a sibling tests module, executable examples, a standard error-returning test signature and an all function, then publish."
sources: [https://docs.dagger.io/0.21/reference/best-practices/modules]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Testing and publishing Dagger modules

Goal: verify a reusable module using Dagger itself. Dagger 0.21 docs; examples use a `greeter` module (constructor default `greeting` "Hello", function `hello(name)` returning "Hello, World!" style output).

## Test module

Create a test module in the same directory as the module under test (here a `tests` subdirectory) and depend on it:

```bash
mkdir tests
cd tests
dagger init --name=tests --sdk=go --source=.
dagger install ..
```

Go test function (Python/TypeScript equivalents in docs):

```go
func (m *Tests) Hello(ctx context.Context) error {
	greeting, err := dag.Greeter().Hello(ctx, "World")
	if err != nil {
		return err
	}
	if greeting != "Hello, World!" {
		return errors.New("unexpected greeting")
	}
	return nil
}
```

The name `tests` is arbitrary (some use `dev`).

## Testable examples

Example modules (shown on the Daggerverse) can double as tests. Layout: `mkdir -p examples/go; cd examples/go; dagger init --name=examples/go --sdk=go --source=.; dagger install ../..`. The page's example function is named `GreeterHello` and points to the Daggerverse docs for example function naming (that page was not read). Often this removes the need for a separate test module.

## Standard signature

The page suggests standardizing test signatures: generate inputs inside the function, synchronize any async work there, and return a single value or an error (the examples use Go `error`, Python raising an exception, TypeScript `Promise<void>` that throws). For values like credentials, use module constructors.

## The all function

Run every test with one function, serially (call each in turn) or in parallel: Go uses `pool.New().WithErrors().WithContext(ctx)` from `github.com/sourcegraph/conc/pool` with `p.Go(m.Hello)`; Python `anyio.create_task_group()` with `tg.start_soon(...)`; TypeScript `Promise.all([...])`. Run: `dagger call -m tests all`.

## Publishing for best Daggerverse rank

Give the module a description, document its functions, tag versions with semver, and hand-craft examples.

Related: computing-software.devops-ci-cd.dagger.adopting-dagger-monorepos.

## Checked

2026-11-07

Read reference/best-practices/modules.mdx in full (live slug /reference/best-practices/modules matches the cited URL) and the Go, Python and TypeScript greeter snippets it embeds. Confirmed the tests module commands, the Go/Python/TypeScript test functions, the tests/dev naming tip, the examples module layout and GreeterHello function, the standard signature advice, the serial and parallel all functions (conc pool, anyio task group, Promise.all), dagger call -m tests all, and the four publishing practices. Corrected the module placement wording, softened the standard-signature paragraph from an instruction to the page's suggestion, and removed the claim that the example naming convention is described on this page. The linked Daggerverse example-naming and semver pages were not opened.

Method: documentation only; no commands were run.
