---
id: computing-software.devops-ci-cd.dagger.sdk-module-init-develop
name: sdk-module-init-develop
category: computing-software
field: devops-ci-cd
product: dagger
tags: [dagger, sdk, modules, dagger-init, dagger-develop, go, python, typescript]
level: practitioner
status: docs-checked
description: "Initialise a Dagger module with dagger init and dagger develop for Go, Python, TypeScript, PHP or Java, and write a first Dagger Function using the dag client."
sources: [https://docs.dagger.io/0.21/getting-started/api/sdk]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Create a Dagger module with an SDK (Dagger 0.21 docs)

Goal: scaffold a module and write a Dagger Function in your language.

## Steps

```shell
dagger init --name=my-module
dagger develop --sdk=go        # or python, typescript, php, java
```

- `dagger init` creates `dagger.json` (module name defaults to the directory name unless `--name`).
- `dagger develop --sdk=...` sets up or updates the local dev resources; source goes in the working directory unless `--source` is given.
- Running `dagger develop` regenerates code for the current dependencies and Dagger API version, so check the changelog first, or pass `--compat=skip` to avoid bumping the API version.

## Generated layout

- Go: `main.go`, `go.mod`, `internal/` (generated `dagger`, `querybuilder`, `telemetry`).
- Python: `src/my_module/main.py`, `pyproject.toml`, `uv.lock`, vendored `sdk/`. The first class must be named for the module in PascalCase (`MyModule`).
- TypeScript: `src/index.ts`, `package.json`, `sdk/`.
- PHP: `src/MyModule.php`, `composer.json`, `sdk/`.
- Java: `src/main/java/io/dagger/modules/mymodule/MyModule.java`, `pom.xml`.
- Generated files cannot be edited; changes are not persisted when the module runs.

## Example function (Go)

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

Python uses `@object_type` on the class and `@function` on `async def get_user(self) -> str`; TypeScript uses `@object()` and `@func()` with `dag.container().from("alpine:latest")...`. Call it with `dagger call get-user` (or `dagger -c 'get-user'`). Update the module name in samples to match yours.

## Sandboxing

Every function has the pre-initialised `dag` client. Functions run in engine containers, giving reproducibility, caching and security: no default access to host files, directories or env vars unless passed as arguments.

Related: computing-software.devops-ci-cd.dagger.api-concepts-and-cli.

## Checked

2026-11-07

Read getting-started/api/clients-sdk.mdx in full (live slug /getting-started/api/sdk; the cited /getting-started/api/clients-sdk URL is a file path that 404s, fixed in sources) and the Go, Python and TypeScript functions-complex snippets it embeds (PHP and Java snippet tabs not opened). Confirmed dagger init and dagger develop behaviour, the compat warning, the generated layouts for all five SDKs, the generated-files note, the get-user example in Go, Python and TypeScript, the PascalCase main object rule for Python, the dagger call and dagger -c invocations, the module-name caution, the dag client note and the sandboxing text. No claim removed.

Method: documentation only; no commands were run.
