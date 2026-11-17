---
id: computing-software.devops-ci-cd.dagger.daggerverse-publish-examples
name: daggerverse-publish-examples
category: computing-software
field: devops-ci-cd
product: dagger
tags: [dagger, daggerverse, publishing, semver, modules, monorepo, examples]
level: practitioner
status: docs-checked
description: "Publish a Dagger module to the Daggerverse (manual or on use), tag semver releases in monorepos, and add hand-crafted per-function examples."
sources: [https://docs.dagger.io/0.21/extending/daggerverse]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Publishing a module to the Daggerverse

Goal: make a Dagger module discoverable and give it good examples. Dagger 0.21 docs.

The Daggerverse is a free Dagger-run service that indexes all publicly available Dagger Functions, ranked with a basic score. Modules are not hosted there; it only fetches public information from Git servers.

## Manual publishing
1. Push the module to a public git repository. Layout is free: one module per repo, or many in a catalogue repo (often named "daggerverse").
2. Open daggerverse.dev, click Publish, paste `GITSERVER/USERNAME/REPOSITORY[/SUBPATH][@VERSION]`, e.g. `github.com/shykes/hello@v0.3.0` or `github.com/shykes/daggerverse/termcast@main`.
3. Click Publish; it can take a few minutes to appear.

To remove a module, ask the Dagger team on Discord.

## Publishing on use
Whenever someone runs `dagger ...` and a remote module (URL like `GITSERVER/USERNAME/daggerverse/...`) supplies an invoked function, that module is published automatically. Work-in-progress can therefore appear; once you tag a valid semver version the module is considered released and the latest version is published.

## Semantic versioning
Only tags matching `vMAJOR.MINOR.PATCH` (e.g. `v1.2.3`) are valid. In a monorepo, prefix the tag with the subpath: tag `foo/v1.2.3`, reference `GITSERVER/USERNAME/REPOSITORY/foo@v1.2.3`.

## Hand-crafted examples
Daggerverse shows basic examples automatically. For custom ones, add an example module under `/examples/<lang>` inside your module. For module `Foo` and function `Bar`:

| Language dir | Top-level example "Baz" | Example for function | Named example for function |
|---|---|---|---|
| `/examples/go` | `Foo_Baz` | `FooBar` | `FooBar_Baz` |
| `/examples/python` (module foo, function bar) | `foo__baz` | `foo_bar` | `foo_bar__baz` |
| `/examples/typescript` | `foo_baz` | `fooBar` | `fooBar_baz` |
| `/examples/shell` (scripts) | `foo_baz.sh` | `foo_bar.sh` | `foo_bar_baz.sh` |

Python uses double underscores as the separator because single underscores already denote spaces in snake case. The page points to the `proxy` module (kpenfound/dagger-modules) as a reference.

Related: module-dependencies-install-update, module-inline-documentation.

## Checked

2026-11-07

Read in full from the docs source: extending/modules/daggerverse.mdx. Every claim matched. No corrections needed.

Method: documentation only; no commands were run.
