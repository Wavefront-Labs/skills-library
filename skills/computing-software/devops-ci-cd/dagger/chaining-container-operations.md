---
id: computing-software.devops-ci-cd.dagger.chaining-container-operations
name: chaining-container-operations
category: computing-software
field: devops-ci-cd
product: dagger
tags: [dagger, chaining, container, with-exec, terminal, with-directory, with-file, cli]
level: practitioner
status: docs-checked
description: "Extend a Dagger Function's returned container from the CLI: with-exec, interactive terminal, with-directory, with-file, and inspecting directories and files."
sources: [https://docs.dagger.io/0.21/extending/modules/chaining]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Chain follow-up operations onto a returned artifact

Goal: continue a workflow from the command line by chaining core API calls onto what a module Function returned (Dagger 0.21 docs). The page uses a Wolfi container builder module, `github.com/dagger/dagger/modules/wolfi@v0.16.2`.

## Run commands in the container

```shell
dagger -m github.com/dagger/dagger/modules/wolfi@v0.16.2 call \
  container \
  with-exec --args="ls","/etc/" \
  stdout
```

Dagger Shell equivalent:

```shell
github.com/dagger/dagger/modules/wolfi@v0.16.2 | container | with-exec ls /etc/ | stdout
```

Chain several `with-exec` calls to modify state (`with-exec rm /etc/os-release | with-exec ls /etc`). Install packages through the builder's argument, then run: `container --packages="curl" with-exec --args="curl","-L","dagger.io" stdout`. In Shell, use `--` before a command with its own flags: `with-exec -- curl -L dagger.io`.

## Debug interactively

Chain `terminal` to open an ephemeral interactive session at that point of the build:

```shell
dagger -m github.com/dagger/dagger/modules/wolfi@v0.16.2 call container --packages="cowsay" terminal
```

The default shell is `sh`; override with `--cmd`, e.g. `container --packages=cowsay,zsh | terminal --cmd=zsh`.

## Add host data to a container

Warning from the page: `with-directory` with `.` uploads the whole current directory, which can be slow; run from a small directory.

```shell
dagger -m github.com/dagger/dagger/modules/wolfi@v0.16.2 call container \
  with-directory --path=/src --source=. \
  with-exec --args="ls","/src" stdout

dagger -m ... call container \
  with-file --path=/README.md --source=./README.md \
  with-exec --args="cat","/README.md" stdout
```

Shell form: `with-file /README.md $(host | file ./README.md)`.

## Inspect results

- Directory listing: `... call build --source=https://github.com/golang/example#master:/hello --args=. directory --path=. entries` (module `github.com/kpenfound/dagger-modules/golang@v0.2.1`).
- File text: `dagger -m github.com/dagger/dagger/modules/ruff call lint --source=https://github.com/dagger/dagger report contents`.
- File size: chain `size`, as in the `arc` module example `archive-directory --name=dagger-cli '--directory=https://github.com/dagger/dagger#main:cmd/dagger' create --format=zip size`.

## Related

computing-software.devops-ci-cd.dagger.chaining-export-publish-services; computing-software.devops-ci-cd.dagger.function-return-types

## Checked

2026-11-07

Read in full from the docs source: extending/modules/chaining.mdx. Confirmed the wolfi@v0.16.2 module, with-exec, --packages, terminal and its --cmd option, the sh default, the with-directory upload warning, with-file, the golang@v0.2.1, ruff and arc examples. No corrections needed.

Method: documentation only; no commands were run.
