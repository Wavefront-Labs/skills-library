---
id: computing-software.devops-ci-cd.dagger.function-arguments-host-resources
name: function-arguments-host-resources
category: computing-software
field: devops-ci-cd
product: dagger
tags: [dagger, functions, arguments, directory, file, container, service, socket]
level: practitioner
status: docs-checked
description: "Pass host directories, files, git refs, container images, TCP/UDP services and Unix sockets into Dagger Functions as typed arguments."
sources: [https://docs.dagger.io/0.21/extending/modules/arguments]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Pass host resources to Dagger Functions

Goal: hand files, directories, images, services and sockets to a Function (Dagger 0.21 docs). Functions run sandboxed with no default host access; resources only arrive as argument values.

## Accepted forms

| Argument type | Value on the CLI |
|---|---|
| `Directory`, `File` | local path or remote Git reference (HTTPS or `ssh://git@github.com/dagger/dagger`) |
| `Container` | OCI image address (CLI pulls it) |
| `Service` | `tcp://HOST:PORT` or `udp://HOST:PORT` |
| `Socket` | path of a host Unix socket (Linux/macOS clients) |
| env var | shell convention `$ENV_VAR_NAME` |

## Directory

```go
func (m *MyModule) Tree(ctx context.Context, src *dagger.Directory, depth string) (string, error) {
	return dag.Container().From("alpine:latest").
		WithMountedDirectory("/mnt", src).WithWorkdir("/mnt").
		WithExec([]string{"apk", "add", "tree"}).
		WithExec([]string{"tree", "-L", depth}).Stdout(ctx)
}
```

Python: `src: dagger.Directory`; TypeScript: `src: Directory`.

```shell
dagger call tree --src=mydir --depth=2
dagger -c 'tree mydir 2'
```

Remote repositories work in core calls too, for example `with-directory --path=/src --source=https://github.com/dagger/dagger`. SSH needs SSH authentication configured on the Dagger host. Default paths and filters for Directory/File arguments are covered in the getting-started Directory type docs, not on this page.

## File

```go
func (m *MyModule) ReadFile(ctx context.Context, source *dagger.File) (string, error) { ... WithFile("/src/myfile", source) ... }
```

```shell
dagger call read-file --source=/my/file/path/README.md
dagger call read-file --source=https://github.com/dagger/dagger.git#main:README.md
```

## Container

```go
func (m *MyModule) OsInfo(ctx context.Context, ctr *dagger.Container) (string, error) {
	return ctr.WithExec([]string{"uname", "-a"}).Stdout(ctx)
}
```

```shell
dagger call os-info --ctr=ubuntu:latest
```

A default image can be set with the `defaultAddress` pragma (documented under the Container type, not on this page).

## Services and sockets

```shell
dagger -m github.com/kpenfound/dagger-modules/postgres@v0.1.0 call \
  client --db=postgres --user=postgres --password=postgres --server=tcp://localhost:5432

dagger -m github.com/sipsma/daggerverse/docker-client@v0.0.1 call \
  --sock=/var/run/docker.sock version
```

## Related

computing-software.devops-ci-cd.dagger.function-arguments-basic-types; computing-software.devops-ci-cd.dagger.function-arguments-secrets

## Checked

2026-11-07

Read in full from the docs source: extending/modules/arguments.mdx and the directory, file and container snippets. Confirmed accepted forms (tcp/udp services, Unix socket paths on Linux and macOS, env vars), the directory, file and container examples, the remote Git and SSH examples, the kpenfound postgres and sipsma docker-client examples, and that default paths, filters and the defaultAddress pragma are documented elsewhere. No corrections needed.

Method: documentation only; no commands were run.
