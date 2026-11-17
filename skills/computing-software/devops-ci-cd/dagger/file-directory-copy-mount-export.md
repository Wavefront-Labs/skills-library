---
id: computing-software.devops-ci-cd.dagger.file-directory-copy-mount-export
name: file-directory-copy-mount-export
category: computing-software
field: devops-ci-cd
product: dagger
tags: [dagger, file, directory, mount, copy, export, http, git]
level: practitioner
status: docs-checked
description: "Move files and directories in Dagger: mount or copy into a container, fetch over HTTP, take a Git tree, and export results back to the host explicitly."
sources: [https://docs.dagger.io/0.21/getting-started/types/file, https://docs.dagger.io/0.21/getting-started/types/directory]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Copy, mount and export files and directories (Dagger 0.21 docs)

Goal: choose between mount and copy, load from local, Git or HTTP, and get output back to the host.

`File` has `contents` and `export`. `Directory` has `entries`, `file`, `withFile`/`withFiles`, `dockerBuild`, `export`.

## Mount vs copy (Go)

```go
// mount: exists only during the call, not in the final image
dag.Container().From("alpine:latest").WithMountedDirectory("/src", source)
// copy: becomes part of the image
dag.Container().From("alpine:latest").WithDirectory("/src", source)
```

Rule of thumb from the docs: prefer mounts (smaller image, more efficient). For files: `WithMountedFile(fmt.Sprintf("/src/%s", name), f)` or `WithFile(...)` where `name, _ := f.Name(ctx)`.

Sources accepted as the argument: a host path, a Git URL (`https://github.com/dagger/dagger#main`, `ssh://git@github.com/user/foo#main` for private repos with SSH auth configured), or a file in a repo (`https://github.com/dagger/dagger.git#main:README.md`).

```shell
dagger call mount-directory --source=./myapp/
dagger call mount-file --f=https://github.com/dagger/dagger.git#main:README.md file --path=/src/README.md contents
```

## Modify, then export

Modifications inside a container never flow back to the host; data moves one way through the DAG. Return a `Directory` or `File` and export it:

```go
func (m *MyModule) GetDir() *dagger.Directory { return m.Base().Directory("/src") }
func (m *MyModule) GetFile() *dagger.File { return m.Base().File("/src/foo") }
```

```shell
dagger call get-dir export --path=/path/to/export
dagger call get-file export --path=/path/to/myfile
```

## Clone a Git repository

```go
d := dag.Git(repository).Ref(ref).Tree()
return dag.Container().From("alpine:latest").WithDirectory("/src", d).WithWorkdir("/src")
```

For SSH forward the agent: `dag.Git(repository, dagger.GitOpts{SSHAuthSocket: sock})` and `--sock=$SSH_AUTH_SOCK`.

## HTTP file

```go
file := dag.HTTP(url)
return dag.Container().From("alpine:latest").WithFile("/src/myfile", file)
```

## Copy into the module runtime

`source.Export(ctx, "foo.txt")` inside the function writes the file into the module runtime container for custom Go processing; call with `dagger call copy-file --source=../data.json`.

## Default path for File

`File` arguments take defaults like `Directory`; see computing-software.devops-ci-cd.dagger.directory-paths-and-filters.

## Checked

2026-11-07

Read in full from the docs source: getting-started/types/file.mdx and directory.mdx with partials. Every claim matched. No corrections needed.

Method: documentation only; no commands were run.
