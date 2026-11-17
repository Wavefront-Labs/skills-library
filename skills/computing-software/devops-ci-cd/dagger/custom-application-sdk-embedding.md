---
id: computing-software.devops-ci-cd.dagger.custom-application-sdk-embedding
name: custom-application-sdk-embedding
category: computing-software
field: devops-ci-cd
product: dagger
tags: [dagger, sdk, custom-applications, go, python, typescript, php, dagger-run]
level: practitioner
status: docs-checked
description: "Embed a Dagger SDK in a Go, Python, TypeScript or PHP program: install commands, version requirements, client connection and running it under dagger run."
sources: [https://docs.dagger.io/0.21/extending/custom-applications/go, https://docs.dagger.io/0.21/extending/custom-applications/python, https://docs.dagger.io/0.21/extending/custom-applications/typescript, https://docs.dagger.io/0.21/extending/custom-applications/php]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Embed a Dagger SDK in your own application

Goal: run Dagger API calls from a standalone program (Dagger 0.21 docs). Every variant is launched with `dagger run <command>`, which runs the command in a Dagger session and shows live progress.

## Go (requires Go 1.22+)

```shell
go get dagger.io/dagger@latest
go mod tidy
```

The docs example builds a project for OS/arch/Go-version matrices. Core shape:

```go
import "dagger.io/dagger/dag"
...
defer dag.Close()
src := dag.Host().Directory(".")
golang := dag.Container().From(fmt.Sprintf("golang:%s", version)).WithDirectory("/src", src).WithWorkdir("/src")
build := golang.WithEnvVariable("GOOS", "linux").WithEnvVariable("GOARCH", "arm64").
    WithExec([]string{"go", "build", "-o", path})
outputs = outputs.WithDirectory(path, build.Directory(path))
...
_, err := outputs.Export(ctx, ".")
```

Run: `dagger run go run multibuild/main.go`. Builds are concurrent because they do not depend on each other.

## Python (requires Python 3.10+)

```shell
uv add dagger-io
# or, self-contained script:
uv add --script test.py dagger-io
dagger run uv run test.py
```

Pattern: `async with dagger.connection(dagger.Config(log_output=sys.stderr)):`, use `dag.host().directory(".")`, build a container per version, `await python.sync()`, and fan out with an `anyio` task group so versions test concurrently.

## TypeScript (requires TypeScript 5.0+; Node.js stable, Bun experimental)

```shell
npm install @dagger.io/dagger@latest --save-dev
dagger run node --loader ts-node/esm ./build.mts
```

A TypeScript executor such as `ts-node` or `tsx` is needed. Pattern: `await dagger.connection(async () => { ... }, { LogOutput: process.stderr })`, then `dag.host().directory(".", { exclude: ["node_modules/"] })`, chained container calls ending in `.sync()` or `.directory("build/").export(...)`.

## PHP (requires PHP 8.2+)

```shell
composer require dagger/dagger
dagger run php test.php
```

Pattern: `use function Dagger\dag;` then `dag()->host()->directory('.')` and `dag()->container()->from("php:$version")->withDirectory(...)->withExec([...])`; read output with `->stdout()`.

## Gotchas

- The docs state the Python and PHP examples run per-version tests concurrently/with live results, while the TypeScript example processes versions in sequence.
- Host access works here because this is an application, not a module (see extending-overview-modules-vs-sdk).

## Checked

2026-11-07

Read in full from the docs source: extending/custom-applications pages and their snippets. Confirmed the client setup and module-shape claims. Corrected the Go core-shape snippet to use the version variable in the image tag, as the page snippet does.

Method: documentation only; no commands were run.
