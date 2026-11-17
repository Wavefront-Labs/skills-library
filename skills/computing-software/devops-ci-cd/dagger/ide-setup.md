---
id: computing-software.devops-ci-cd.dagger.ide-setup
name: ide-setup
category: computing-software
field: devops-ci-cd
product: dagger
tags: [dagger, ide, go, python, typescript, php, java, vscode, autocomplete]
level: practitioner
status: docs-checked
description: "Get IDE autocomplete for Dagger modules in Go, Python, TypeScript, PHP and Java after dagger develop, including go.work and virtualenv setup."
sources: [https://docs.dagger.io/0.21/reference/ide-setup]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# IDE setup for Dagger modules

Goal: have the IDE resolve the generated SDK and dependency bindings. Run `dagger develop` first. Dagger 0.21 docs.

## Go

Add the module to `go.work`, or delete the module's generated `go.mod`/`go.sum` to reuse a parent one (not advisable if the Dagger module has unrelated dependencies). Workspace setup in the repo root:

```shell
go work init
go work use ./
go work use ./path/to/mod
echo go.work >> .gitignore
echo go.work.sum >> .gitignore
```

Restart the IDE. The local Go files from `dagger develop` can be left out of version control.

## Python

Dependencies (including `./sdk`) must be in an activated virtualenv such as `.venv` next to `pyproject.toml`. With uv: `dagger develop` then `uv sync` and `uv run code .`. For an older module without `uv.lock`: `uv add --editable ./sdk` and `rm requirements.lock`. uv.lock needs `dagger-io` as a production dependency; other tools use it as a dev dependency. With `requirements.lock`: `uv venv` then `uv pip install -r requirements.lock -e ./sdk -e .` (pin 3.12 with `echo 3.12 > .python-version`; default is 3.13), or `python -m venv .venv` + `pip install -r requirements.lock -e ./sdk -e .`. Hatch: add `dagger-io @ {root:uri}/sdk` to a `dev` env with `allow-direct-references = true`; Poetry: `poetry add --group=dev -e ./sdk`. Open VS Code or PyCharm in the directory holding `.venv` and `pyproject.toml`. If `.venv` is inside the module, add it to `.gitignore` and `"include": ["!.venv"]` in `dagger.json`.

## TypeScript

The default template's `tsconfig.json` maps `@dagger.io/dagger` to `./sdk` (with `experimentalDecorators: true`), so no install is needed.

## PHP

`composer.json` needs a path repository `./sdk` and `"dagger/dagger": "*@dev"`. Open PhpStorm or VS Code (Intelephense or Phpactor) at the directory with `composer.json`; Emacs can use Eglot with Phpactor.

## Java

`dagger develop` generates a Maven `pom.xml`; import it as a Maven project. Generated code is in `target/generated-sources` (git-ignored, refresh with `dagger develop`). Do not modify the compiler, shade and build-helper plugin configuration.

## Source maps

Go and TypeScript SDKs attach `./path/to/filename:line` comments so IDEs can jump between inter-dependent modules (VS Code may need the Open file plugin).

Related: computing-software.devops-ci-cd.dagger.cli-module-lifecycle.

## Checked

2026-11-07

Read reference/ide-setup.mdx in full (all five language tabs and the Python uv, uv pip, pip, Hatch and Poetry sub-tabs; the page's embedded _ide partial was not needed). Confirmed the go.work and go.mod advice, the .gitignore lines, the uv.lock production-dependency note, the Python 3.13 default and the .python-version pin to 3.12, the Hatch and Poetry commands, the .venv and dagger.json include tip, the tsconfig paths mapping with experimentalDecorators, the PHP composer.json repositories entry, the Eglot and Phpactor remark, the Java pom.xml, target/generated-sources and plugin remarks, and the Go and TypeScript source-map comments. No corrections needed.

Method: documentation only; no commands were run.
