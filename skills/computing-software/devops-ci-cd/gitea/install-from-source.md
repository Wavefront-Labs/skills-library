---
id: computing-software.devops-ci-cd.gitea.install-from-source
name: install-from-source
category: computing-software
field: devops-ci-cd
product: gitea
tags: [gitea-build-tags, gitea, make-build, bindata, sqlite-unlock-notify, ldflags-custompath, cross-compile]
level: advanced
status: docs-checked
description: "Build Gitea from source: required tools, git tags or PR refs, TAGS (bindata, sqlite, pam), backend/frontend targets, LDFLAGS paths, cross and Zig builds."
sources: ["https://gitea.com/gitea/docs/src/branch/main/docs/installation/from-source.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Building Gitea from source

The docs page is marked outdated in favour of build-source.md in the Gitea repository, so check that for current requirements. Tools: `go` (minimum version per release), `node` with npm (frontend), `make`, and `git clone https://github.com/go-gitea/gitea`. Use `git checkout <tag>` for releases, `main` for development, and `git fetch origin pull/<id>/head:pr-<id>` then checkout to test a PR.

## Build tags
- `bindata`: single binary with all assets; required for production.
- `sqlite sqlite_unlock_notify`: SQLite3 support (tiny installs only).
- `pam`: PAM authentication on Linux.
- `gogit`: experimental go-git variants of Git commands.

CI's release build uses `TAGS="bindata sqlite sqlite_unlock_notify"`:
```bash
TAGS="bindata sqlite sqlite_unlock_notify" make build
```
`build` = `make backend` (Go) + `make frontend` (Node). With prebuilt frontend files: `TAGS="bindata" make backend`. Test with `./gitea web`. A source-built binary has no SELinux label (see `gitea-selinux`).

## Changing default paths at build time
Defaults: `CustomPath` = `custom/` in the working directory, config at `$(CustomPath)/conf/app.ini`, `AppWorkPath` = working directory, `StaticRootPath` = `AppWorkPath`. Override through `LDFLAGS` with `-X` settings such as `-X "code.gitea.io/gitea/modules/setting.CustomPath=custom-path"`, `...setting.CustomConf=`, `...setting.AppWorkPath=`, `...setting.StaticRootPath=`, and `-X "code.gitea.io/gitea/cmd.PIDFile=/run/gitea.pid"`. `gitea help` prints the computed values.

## Cross-compiling
Tags use cgo, so you need a C cross compiler for the target when `TAGS` is set:
```bash
CC=aarch64-unknown-linux-gnu-gcc GOOS=linux GOARCH=arm64 TAGS="bindata sqlite sqlite_unlock_notify" make build
```
Without tags `GOOS=linux GOARCH=arm64 make build` needs no cross compiler. Static: `LDFLAGS="-linkmode external -extldflags '-static' $LDFLAGS" TAGS="netgo osusergo $TAGS" make build`. Zig works as the C compiler, e.g. `CC="zig cc -target x86_64-windows-gnu" CGO_ENABLED=1 CGO_CFLAGS="-O2 -g -pthread" GOOS=windows GOARCH=amd64`.

Source maps: `ENABLE_SOURCEMAP=true|reduced|false` (production default reduced).

## Checked
2026-11-03. Commands, flags, settings, numbers and behaviour were compared line by line with the Gitea docs source page named in `sources` (read in full from the docs repository raw file). Nothing else removed; no unconfirmed claim remained.
Method: documentation only; no commands were run.
