---
id: computing-software.devops-ci-cd.packer.fileset-function
name: fileset-function
category: computing-software
field: devops-ci-cd
product: packer
tags: [fileset, glob, function, scripts, fn-fileset]
level: practitioner
status: docs-checked
description: "List files at parse time with fileset(path, pattern) to feed a shell provisioner's scripts list."
sources:
  - https://developer.hashicorp.com/packer/docs/templates/hcl_templates/functions/file/fileset/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

`fileset(path, pattern)` enumerates a set of regular file names given a path and a pattern. The path is removed from the resulting names, and any result still containing path separators uses forward slash for cross-system compatibility.

Supported patterns:

- `*` matches any sequence of non-separator characters.
- `**` matches any sequence of characters, including separators.
- `?` matches any single non-separator character.
- `{alternative1,...}` matches if one of the comma-separated alternatives matches.
- `[CLASS]` / `[^CLASS]` match a single non-separator character inside / outside a class; classes support sets (`[abc]`) and ranges (`[a-z]`).

Functions are evaluated during configuration parsing, so `fileset` only sees files already on disk before Packer takes any action.

Examples from the docs, for a tree with `linux/files/{hello,world}.txt` and `linux/scripts/script-{1-install,2-setup}.sh` beside `build-linux.pkr.hcl`:

- `fileset(".", "*")` gives `build-linux.pkr.hcl` only.
- `fileset(".", "linux/scripts/*")` gives `linux/scripts/script-1-install.sh` and `linux/scripts/script-2-setup.sh`.
- `fileset("linux", "files/{hello,world}.txt")` gives `files/hello.txt` and `files/world.txt`.
- `fileset("./linux/files", "*")` gives `hello.txt` and `world.txt`.
- `fileset("./linux", "**")` gives all four files, relative to `linux`.

Common use: the `scripts` field of a `shell` provisioner.

```hcl
provisioner "shell" {
  scripts = fileset(".", "linux/scripts/*")
}
```

Provisioners with a `scripts` field: `shell`, `powershell`, `shell-local`, `windows-shell`. To test a pattern, pipe it to `packer console <dir>`, for example `echo 'fileset(".", "linux/scripts/*")' | packer console pkr-consul`.

## Checked

2026-11-08. Read the full fileset function page (Packer 1.16 docs source). Removed unsourced claims about ordering and sort(tolist()).

Method: documentation only; no commands were run.
