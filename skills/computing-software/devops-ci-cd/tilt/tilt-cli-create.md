---
id: computing-software.devops-ci-cd.tilt.tilt-cli-create
name: tilt-cli-create
category: computing-software
field: devops-ci-cd
product: tilt
tags: [cli-create, tilt, tilt-cli, extensions]
level: advanced
status: docs-checked
description: "Create objects in a running Tilt session with tilt create, create cmd, create filewatch, create repo and create ext."
sources:
  - "https://docs.tilt.dev/cli/tilt_create.html"
  - "https://docs.tilt.dev/cli/tilt_create_cmd.html"
  - "https://docs.tilt.dev/cli/tilt_create_ext.html"
  - "https://docs.tilt.dev/cli/tilt_create_filewatch.html"
  - "https://docs.tilt.dev/cli/tilt_create_repo.html"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# tilt create

All forms act on a running Tilt session. If it was started with a non-default address, pass `--host` (env `TILT_HOST`) and `--port` (env `TILT_PORT`, default 10350).

## tilt create -f

Create a resource from a file or stdin: `tilt create -f FILENAME`. Options: `--dry-run` (none, server or client), `--edit` (edit before creating), `-k` kustomize dir, `-R` recursive, `-l` selector, `--save-config`, `--validate` (default strict).

## tilt create cmd

```
tilt create cmd NAME COMMAND [ARG...]
```

Creates a local command, meant to compose with other Tilt APIs that restart it or monitor its status. COMMAND must be an executable; a shell script will not work, so use `sh -c`.

```
tilt create cmd my-cmd echo hello world
tilt create cmd my-cmd sh -c "echo hi && echo bye"
```

Options: `-e, --env NAME=VALUE`, `--filewatch` (re-run when the named filewatches fire), `-w, --workdir` (default current directory).

## tilt create filewatch

```
tilt create filewatch [NAME] [PATHS] --ignore [IGNORES]
tilt create fw src-and-web src web --ignore=web/node_modules
```

A FileWatch watches paths recursively and records the most recent file changed in its status; it combines with other Tilt objects to trigger events. `--ignore` uses `.dockerignore` syntax, relative to the current directory.

## tilt create repo

```
tilt create repo NAME URL [ARG...]
tilt create repo default https://github.com/tilt-dev/tilt-extensions
tilt create repo default https://github.com/tilt-dev/tilt-extensions --ref=SHA
```

Registers an extension repository (git-hosted or local filesystem). `--ref` is the git reference to sync.

## tilt create ext

```
tilt create ext NAME [ARG...]
tilt create ext cancel
tilt create ext my-kubefwd --path=./kubefwd -- --namespaces=default
tilt create ext cancel --repo=dev
```

Registers an extension, which loads services into your dev environment. The repo must already exist (via `tilt create repo` or the Tiltfile). `--repo` defaults to `default` (list with `tilt get repo`); `--path` defaults to the extension name.

## Checked

Date: 2026-11-07

Every command, parameter, default, name and figure in this skill was matched line by line against the page text of https://docs.tilt.dev/cli/tilt_create.html, https://docs.tilt.dev/cli/tilt_create_cmd.html, https://docs.tilt.dev/cli/tilt_create_ext.html, https://docs.tilt.dev/cli/tilt_create_filewatch.html, https://docs.tilt.dev/cli/tilt_create_repo.html (read in full, including its code blocks and the page source in the tilt-dev/tilt.build docs repo; linked example-repo files and screenshots were not opened). No change was needed.

Method: documentation only; no commands were run.
