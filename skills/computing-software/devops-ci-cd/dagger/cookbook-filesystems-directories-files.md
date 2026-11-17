---
id: computing-software.devops-ci-cd.dagger.cookbook-filesystems-directories-files
name: cookbook-filesystems-directories-files
category: computing-software
field: devops-ci-cd
product: dagger
tags: [dagger, cookbook, filesystems, directories, mount, copy, filters, git-clone, export, default-path]
level: practitioner
status: docs-checked
description: "Dagger cookbook recipes to clone repos, mount or copy directories and files, filter them, fetch HTTP files, set a default path and export results to the host."
sources: [https://docs.dagger.io/0.21/cookbook/filesystems]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Dagger cookbook: working with files and directories

Goal: move source into containers and results back to the host. Go snippets from the Dagger 0.21 cookbook.

## Clone a remote Git repo into a container
```go
d := dag.Git(repository).Ref(ref).Tree()
return dag.Container().From("alpine:latest").WithDirectory("/src", d).WithWorkdir("/src")
```
`dagger call clone --repository=https://github.com/dagger/dagger --ref=<commit>`. For SSH add `dagger.GitOpts{SSHAuthSocket: sock}` with a `*dagger.Socket` and pass `--sock=$SSH_AUTH_SOCK` (see remote-repositories-authentication). Append `terminal` to inspect the result.

## Mount vs copy
- Mount: `WithMountedDirectory("/src", source)`; applies only within the invocation, is not in the final image, and changes stay in the mount target, not the source.
- Copy: `WithDirectory("/src", source)`.
The docs' rule of thumb: use mounts where possible (smaller image, more efficient). Directory arguments accept a local path or a remote Git repo (`https://github.com/dagger/dagger#main`, `ssh://git@github.com/user/foo#main`). Files work likewise: `WithMountedFile("/src/<name>", f)` or `WithFile`, with refs like `https://github.com/dagger/dagger.git#main:README.md`.

## Modify after copying, and export
Data flows one way: modifications in the container never go back to the host automatically. Return a `Directory` or `File` and export: `dagger call get-dir export --path=/path/to/export`, `dagger call get-file export --path=/path/to/myfile`.

## Filter what is copied
- Pre-call (declarative): `// +ignore=["*", "!**/*.md"]` on the argument, so everything except Markdown files is excluded.
- Post-call (run time): `exclude []string` argument passed to `WithDirectory("/src", source, dagger.ContainerWithDirectoryOpts{Exclude: exclude})`. Call: `dagger call copy-directory-with-exclusions --source=. --exclude=dagger*`.

## Other recipes
- HTTP file: `dag.HTTP(url)` then `WithFile("/src/myfile", file)`; `dagger call read-file-http --url=<url>`.
- File into the module runtime container: `source.Export(ctx, "foo.txt")` then read it with normal Go file APIs; `dagger call copy-file --source=../data.json`.
- Module-wide default path: constructor with `// +defaultPath="."` on a `*dagger.Directory` stored in the struct; override with `dagger call --source=/src/myapp foo`.

Related: remote-repositories-authentication, services-bind-expose-lifecycle.

## Checked

2026-11-07

Read in full from the docs source: cookbook/filesystems.mdx with its partials and snippets. Confirmed the recipes and commands. Corrected the filter description: the exclude pattern uploads everything except Markdown files, not only Markdown.

Method: documentation only; no commands were run.
