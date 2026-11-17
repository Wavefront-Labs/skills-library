---
id: computing-software.devops-ci-cd.dagger.directory-paths-and-filters
name: directory-paths-and-filters
category: computing-software
field: devops-ci-cd
product: dagger
tags: [dagger, directory, default-path, ignore, filters, context-directory, monorepo]
level: practitioner
status: docs-checked
description: "Give Dagger Function Directory args a default path, resolve it against the context directory, and cut upload size with pre-call ignore and post-call filters."
sources: [https://docs.dagger.io/0.21/getting-started/types/directory]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Directory default paths and filters (Dagger 0.21 docs)

Goal: load source directories without passing them every call, and keep uploads small.

Functions cannot see the host filesystem; host paths must be passed as arguments (for reproducibility and security).

## Default path

```go
func (m *MyModule) ReadDir(
	ctx context.Context,
	// +defaultPath="/"
	source *dagger.Directory,
) ([]string, error) {
	return source.Entries(ctx)
}
```

Python: `DefaultPath` annotation; TypeScript: `@argument({ defaultPath: "/" })`; PHP: `#[DefaultPath('/')]`. Only for `Directory` and `File` arguments; an explicit value always overrides.

Resolution: in a Git repo (a `.git` exists), absolute paths resolve from the repo root and relative paths from the directory holding `dagger.json`; otherwise everything resolves from the `dagger.json` directory.

| Default | Git repo (module in /my-module) | Non-Git |
|---|---|---|
| `/` | `/` | `/my-module` |
| `/src` | `/src` | `/my-module/src` |
| `.` | `/my-module` | `/my-module` |
| `..` | `/` | error (outside context) |

Files outside the context directory cannot be retrieved. A module-wide default goes in the constructor: `func New(// +defaultPath="." source *dagger.Directory) *MyModule`; override with `dagger call --source=/src/myapp foo`.

Dagger shell re-evaluates default-path sources on every command, so exports into the tree can invalidate cache and rerun the pipeline. Pass the source explicitly once instead: `result=$(test --source=".")`.

## Pre-call filtering (ignore)

Applied before upload to the engine, using `.gitignore` syntax; order matters and `!` negates earlier patterns. Dagger does not read `.gitignore`/`.dockerignore`; copy patterns by hand.

```go
// +ignore=["*", "!**/*.go", "!go.mod", "!go.sum"]
source *dagger.Directory,
```

Useful patterns: `["**_test.go", "**/testdata/**"]`, `["bin"]`, `["**/.venv", "**/__pycache__"]`, `["**/node_modules"]`, `[".git", "**/.gitignore"]`. Python uses `Ignore([...])`, TypeScript `@argument({ ignore: [...] })`, PHP `#[Ignore(...)]`, Java `@Ignore({...})`.

## Post-call filtering (include/exclude)

Applied when copying into a container:

```go
WithDirectory("/src", source, dagger.ContainerWithDirectoryOpts{Exclude: []string{"*.git", "internal"}})
...
WithDirectory("/app", builder.Directory("/src/hello"), dagger.ContainerWithDirectoryOpts{Include: []string{"hello.bin"}})
```

Runtime exclusion as a function argument: `exclude []string` passed to `ContainerWithDirectoryOpts{Exclude: exclude}`, called with `--exclude=*.md`.

## Mount vs copy and debugging

`withMountedDirectory`/`withMountedFile` exist only during the invocation, are not in the final image, and edits do not reach the source; the page says prefer mounts. To inspect what a filter lets through, write a function that takes the filtered `Directory` and returns it (for example `+ignore=["*", "!analytics"]`), then view its entries, open a terminal, or export it. The TUI and Dagger Cloud trace show the upload patterns.

Related: computing-software.devops-ci-cd.dagger.file-directory-copy-mount-export.

## Checked

2026-11-07

Read in full from the docs source: getting-started/types/directory.mdx and partials. Every claim matched. No corrections needed.

Method: documentation only; no commands were run.
