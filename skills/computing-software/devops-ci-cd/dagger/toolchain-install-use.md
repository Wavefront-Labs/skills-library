---
id: computing-software.devops-ci-cd.dagger.toolchain-install-use
name: toolchain-install-use
category: computing-software
field: devops-ci-cd
product: dagger
tags: [dagger, toolchain, dagger-json, customizations, quickstart, no-code]
level: practitioner
status: docs-checked
description: "Install a Dagger toolchain with dagger toolchain install, call its functions, and customize argument defaults, defaultPath and ignoreChecks in dagger.json."
sources: [https://docs.dagger.io/0.21/core-concepts/toolchains, https://docs.dagger.io/0.21/getting-started/quickstarts/toolchain]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Install and use a Dagger toolchain

Goal: add build/test/lint automation to a project with no Dagger code (Dagger 0.21 docs).

A toolchain is a Dagger module designed for consumption: you install it and call its functions via `dagger call` or `dagger check`, rather than importing it into code.

## Install

```shell
dagger init                                   # new module in the project
dagger toolchain install github.com/kpenfound/blueprints/hello-dagger --name hello
dagger functions
dagger call hello --help
dagger call hello test
dagger call hello build
dagger call hello publish --address=ghcr.io/myorg/hello-dagger:latest
```
Sources may be GitHub paths (`github.com/user/repo/path`), local paths, or Git URLs with optional version tags. `--name` sets a custom namespace; several toolchains can coexist, each in its own namespace. The project directory is used as source code automatically. In the quickstart the example toolchain exposes `build`, `build-env`, `publish` and `test`.

The docs recommend tool-specific toolchains (formatter, linter, test runner separately) over one monolithic per-language toolchain, so each can integrate deeply and update independently.

## Customize via optional arguments

`dagger functions` and `dagger call <fn> --help` list arguments, for example `dagger call build --output-dir=./dist`.

## Customize in dagger.json

Override an argument default:
```json
{
  "name": "my-app",
  "toolchains": [
    {
      "name": "greeter",
      "source": "github.com/example/greeter",
      "customizations": [
        { "function": ["greet"], "argument": "message", "default": "hola" }
      ]
    }
  ]
}
```
Override a `+defaultPath` argument: a customization entry with `"argument": "source", "defaultPath": "/my-subdirectory"`.

Filter out checks: add `"ignoreChecks": ["failing-check", "experimental-*"]` to the toolchain entry (glob patterns are supported). Confirm the active set with `dagger check -l`.

## CI

The same commands run locally and in CI; the docs' GitHub Actions example uses `actions/checkout@v4`, `dagger/dagger-for-github@v6` and `run: dagger check`.

Related: `computing-software.devops-ci-cd.dagger.checks-run-filter`.

## Checked

2026-11-07

Read introduction/core-concepts/toolchains.mdx (live slug /core-concepts/toolchains) and getting-started/quickstarts/blueprint/index.mdx (live slug /getting-started/quickstarts/toolchain) in full; neither embeds snippet files. The two cited URLs were file paths that 404, fixed in sources. Confirmed the toolchain definition, dagger toolchain install and the three source kinds, --name, multiple namespaces, the tool-specific recommendation, --help and example arguments, the customizations default and defaultPath examples, ignoreChecks with glob support and dagger check -l, the hello-dagger quickstart commands and its four listed functions, the automatic use of the project directory, and the GitHub Actions example. Removed the claim that ignoreChecks patterns are scoped to the toolchain, which the page does not state. The linked github-actions page and the kpenfound/blueprints repo were not opened.

Method: documentation only; no commands were run.
