---
id: computing-software.devops-ci-cd.dagger.writing-dagger-functions
name: writing-dagger-functions
category: computing-software
field: devops-ci-cd
product: dagger
tags: [dagger, functions, modules, sandboxing, dagger-call]
level: practitioner
status: docs-checked
description: "Write and call a Dagger Function in Go, Python or TypeScript, and understand the container sandbox it runs in (root user, empty working directory)."
sources: [https://docs.dagger.io/0.21/extending/functions]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Write a Dagger Function

Goal: add a callable Function to a module (Dagger 0.21 docs). Functions are units of computation combining Dagger API operations with your own logic, packaged in modules.

## Method

Replace the module's source with a Function. The docs example calls a remote API from an alpine container.

Go (`main.go`; the context is an input and error an output):

```go
func (m *MyModule) GetUser(ctx context.Context) (string, error) {
	return dag.Container().
		From("alpine:latest").
		WithExec([]string{"apk", "add", "curl"}).
		WithExec([]string{"apk", "add", "jq"}).
		WithExec([]string{"sh", "-c", "curl https://randomuser.me/api/ | jq .results[0].name"}).
		Stdout(ctx)
}
```

Python (`src/my_module/main.py`): methods decorated `@function` on a class decorated `@object_type`. The first class must be named after the module in PascalCase (`dagger init --name=my-module` gives `MyModule`); this is the "main object".

```python
@object_type
class MyModule:
    @function
    async def get_user(self) -> str:
        return await (dag.container().from_("alpine:latest")
            .with_exec(["apk", "add", "curl"]).with_exec(["apk", "add", "jq"])
            .with_exec(["sh", "-c", "curl https://randomuser.me/api/ | jq .results[0].name"])
            .stdout())
```

TypeScript (`src/index.ts`): `@object()` class with `@func()` method `async getUser(): Promise<string>`. Java: Functions must be public, annotated `@Function`, in a class annotated `@Object`.

Call it:

```shell
dagger call get-user
dagger -c 'get-user'
```

The docs show a JSON name object (title, first, last) as output. The module name in samples must match the name used at `dagger init`.

## Sandbox facts (from the page)

- Functions run in containers spawned by the Dagger Engine, giving reproducibility, cacheability and security: no default access to host files, directories or environment variables; host resources must be passed as argument values.
- Code currently runs as `root` without a full set of Linux capabilities and other standard `runc` sandboxing.
- Working directory starts as an empty directory; you may read and write there, including via `Container.export()`, `Directory.export()` and `File.export()`.
- You may use the Dagger API, other modules you depend on, the language standard library and third-party libraries.

## Related

- computing-software.devops-ci-cd.dagger.function-arguments-basic-types
- computing-software.devops-ci-cd.dagger.function-return-types

## Checked

2026-11-07

Read extending/modules/functions.mdx (live slug /extending/functions; the cited /extending/modules/functions URL is a file path that 404s, fixed in sources) in full, plus all five functions-complex snippets (Go, Python, TypeScript, PHP, Java) and the sandbox section. The imported _dagger_module_init partial is not rendered on this page body and was not opened. Confirmed the example code, the Python main-object naming rule, the Java public/@Function/@Object rule, the TypeScript @object()/@func() shape, the call forms, the JSON output, the module-name caution, the three sandbox purposes, host-access-by-argument, root user without full capabilities, and the empty working directory with the three export APIs. Softened the root statement to the page's 'currently'.

Method: documentation only; no commands were run.
