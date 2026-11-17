---
id: computing-software.devops-ci-cd.dagger.function-return-types
name: function-return-types
category: computing-software
field: devops-ci-cd
product: dagger
tags: [dagger, functions, return-types, directory, file, container, chaining]
level: practitioner
status: docs-checked
description: "Return strings, numbers and just-in-time Directory, File or Container values from Dagger Functions, and build your own chainable with- methods."
sources: [https://docs.dagger.io/0.21/extending/return-types]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Function return types

Goal: choose and write the right return type (Dagger 0.21 docs). Functions can return basic types or any Dagger core type (`Directory`, `Container`, `Service`, `Secret`, ...). A function with no return annotation becomes the API `Void` type.

## Scalars

`string`, integer (`int`/`number`), float (`float64`/`float`). TypeScript floats need `import type { float } from "@dagger.io/dagger"`. Examples: `dagger call add-integer --a=1 --b=2` prints `3`; `dagger call add-float --a=1.4 --b=2.7` prints `4.1`.

## Just-in-time Directory

Build and return the output directory (Go):

```go
func (m *MyModule) GoBuilder(ctx context.Context, src *dagger.Directory, arch string, os string) *dagger.Directory {
	return dag.Container().From("golang:1.21").
		WithMountedDirectory("/src", src).WithWorkdir("/src").
		WithEnvVariable("GOARCH", arch).WithEnvVariable("GOOS", os).
		WithEnvVariable("CGO_ENABLED", "0").
		WithExec([]string{"go", "build", "-o", "build/"}).
		Directory("/src/build")
}
```

```shell
dagger call go-builder --src=https://github.com/golang/example#master:/hello --arch=amd64 --os=linux
```

Output shows `_type: Directory` with `entries: - hello`.

## Just-in-time File

Return `*dagger.File` (`dagger.File` / `File`), e.g. an archiver that zips a directory and returns `.File("/src/out.zip")`. Output shows `_type: File`, `name: out.zip` and a `size`.

## Container

Return a built `*dagger.Container`; treat it like a Dockerfile build stage (each operation yields a new immutable state, exportable as an OCI image).

```go
func (m *MyModule) AlpineBuilder(ctx context.Context, packages []string) *dagger.Container {
	ctr := dag.Container().From("alpine:latest")
	for _, pkg := range packages {
		ctr = ctr.WithExec([]string{"apk", "add", pkg})
	}
	return ctr
}
```

`dagger call alpine-builder --packages=curl,openssh` prints `_type: Container` metadata. Then keep chaining in the CLI (inspect, export, publish).

## Chainable custom objects

If the returned object is JSON-serializable, its state is kept and passed to the next call. Return the receiver:

```python
@object_type
class MyModule:
    greeting: str = "Hello"
    name: str = "World"

    @function
    def with_greeting(self, greeting: str) -> Self:
        self.greeting = greeting
        return self
```

Go returns `(*MyModule, error)` from `WithGreeting`/`WithName` on a struct with public `Greeting`/`Name`; TypeScript returns `this` from `@func()` methods over `@func()` fields.

```shell
dagger call with-name --name=Monde with-greeting --greeting=Bonjour message   # Bonjour, Monde!
```

## Gotcha

The TypeScript `alpineBuilder` snippet in the docs iterates with `for (const pkg in packages)`; `in` iterates indices in JavaScript, so use `of` in real code. (Observation from reading the snippet, not stated by the page.)

## Related

computing-software.devops-ci-cd.dagger.chaining-container-operations; computing-software.devops-ci-cd.dagger.chaining-export-publish-services

## Checked

2026-11-07

Read extending/modules/return-types.mdx in full (live slug /extending/return-types; the old /extending/modules/return-types URL returned 404, fixed in sources). Confirmed the Void note, scalar examples and outputs (3, 4.1), the TypeScript float note, the go-builder, archiver and alpine-builder calls with their _type outputs, the Dockerfile build-stage description of Container, and the Chaining section. Opened the Go return-values-directory, return-values-container, return-values-file and return-values-chaining snippets, the Python and TypeScript chaining snippets, the TypeScript container snippet (confirms the for-in loop remark) and the TypeScript float snippet (confirms import type { float }); PHP and Java tabs not opened. The remark that the page does not state the for-in problem is kept as a labelled observation. No claims removed.

Method: documentation only; no commands were run.
