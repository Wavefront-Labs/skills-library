---
id: computing-software.devops-ci-cd.dagger.dagger-shell-basics
name: dagger-shell-basics
category: computing-software
field: devops-ci-cd
product: dagger
tags: [dagger, dagger-shell, shell, pipelines, chaining, modules, repl, kebab-case]
level: practitioner
status: docs-checked
description: "Use Dagger Shell to chain API functions with pipes: input modes, variables, loading modules, .help, terminal, and how shell names map to SDK function names."
sources: [https://docs.dagger.io/0.21/introduction/features/shell, https://docs.dagger.io/0.21/getting-started/quickstarts/basics]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Dagger Shell basics

Goal: build and run containerized workflows interactively with Bash-like syntax (Dagger 0.21 docs).

## Semantics

Dagger Shell looks like Bash but runs Dagger Functions: `foo | bar` means `foo().bar()`, values passed are typed objects, execution happens in containers, and shell builtins are prefixed with `.` (for example `.help`, `.wait`). Bash features available: variables, shell functions, job control (`frontend | test & backend | test & .wait`) and quoting. Commands are sandboxed; host files, secrets and services must be passed as arguments.

## Input modes

```shell
dagger -c 'container | from alpine | terminal'     # inline
dagger                                              # interactive REPL
dagger <<EOF
container | from alpine | terminal
EOF
```
A script can start with `#!/usr/bin/env dagger`.

## First commands

```shell
container | from alpine | with-exec uname | stdout
container | from alpine | with-exec apk add curl | with-exec curl https://dagger.io | stdout
container | from alpine | with-directory /src https://github.com/dagger/dagger
container | from alpine | with-new-file /hi.txt "Hello from Dagger!" | terminal
container | from alpine | .help with-exec       # context-sensitive help
```
Publish in one chain:
```shell
container | from alpine | with-new-file /hi.txt "Hello from Dagger!" |
  with-entrypoint cat /hi.txt | publish ttl.sh/hello
```
The docs put `--` before command arguments that look like flags: `with-exec -- go build -o hello .` (the page does not explain the separator in prose).

## Variables and sub-pipelines

```shell
repo=$(git https://github.com/dagger/hello-dagger | head | tree)
env=$(container | from node:23 | with-directory /app $repo | with-workdir /app)
build=$($env | with-exec npm install | with-exec npm run build | directory ./dist)
container | from nginx | with-directory /usr/share/nginx/html $build | terminal --cmd=/bin/bash
```

## Loading modules

`dagger -m github.com/dagger/dagger/docs@v0.18.5` loads a module; `.help` then lists its commands, and `server | up` runs the docs server as an ephemeral service. A module name is its constructor: `.help MODULE`, `MODULE --foo=bar`, `foo=$(MODULE)`, `MODULE | foo | bar`. Several modules can be combined in one session.

## Names

Function, argument and field names become kebab-case: Go `FooBar`, Python `foo_bar` and TypeScript/PHP/Java `fooBar` are all `foo-bar`. A module function `build-and-publish` can be called by name; `dagger -c build-and-publish` is equivalent to chaining its parts.

Related: `computing-software.devops-ci-cd.dagger.ci-workflow-quickstart`, `computing-software.devops-ci-cd.dagger.debug-observability`.

## Checked

2026-11-07

Read in full from the docs source: introduction/features/shell.mdx and getting-started/quickstarts/basics. Confirmed semantics, input modes, variables, module loading and naming. Reworded the "--" sentence: the docs only show `with-exec -- go build -o hello .` and do not explain the separator.

Method: documentation only; no commands were run.
