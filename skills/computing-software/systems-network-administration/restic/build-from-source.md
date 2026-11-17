---
id: computing-software.systems-network-administration.restic.build-from-source
name: build-from-source
category: computing-software
field: systems-network-administration
product: restic
tags: [restic, build, source, golang, cross-compile]
level: practitioner
status: docs-checked
description: "Build restic from source with go run build.go and cross-compile using --goos, --goarch and --goarm."
sources:
  - https://restic.readthedocs.io/en/stable/020_installation.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Build restic from source

The install page requires at least Go 1.25; older versions may work but are not supported. The only tested compiler is the official Go compiler (gccgo may work but is unsupported).

```
git clone https://github.com/restic/restic
cd restic
go run build.go
```

The build script builds the `restic` binary, which is statically linked and needs no libraries.

## Cross-compiling

`build.go` takes target flags:

- `--goos` operating system
- `--goarch` architecture
- `--goarm` ARM version, only for 32-bit ARM

Examples from the docs:

```
go run build.go --goos windows --goarch amd64
go run build.go --goos freebsd --goarch 386
go run build.go --goos linux --goarch arm --goarm 6
go run build.go --goos solaris --goarch amd64
```

## After building

Run `restic version` on the built binary to confirm. Shell completions and man pages can be generated from the same binary with `restic generate` (see the shell-completion skill).

## Checked

2026-11-03. Confirmed in the restic docs page Installation (From source): Go 1.25 minimum, clone and `go run build.go`, the `--goos`/`--goarch`/`--goarm` examples, static linking, tested compiler. The generate and man page note is from the Autocompletion section. Removed: the advice on release checksums, commit tracking and uniform builds (not in the docs).

Method: documentation only; no commands were run.
