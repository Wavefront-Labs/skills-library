---
id: computing-software.devops-ci-cd.dagger.module-interfaces
name: module-interfaces
category: computing-software
field: devops-ci-cd
product: dagger
tags: [dagger, interfaces, modules, structural-typing, object-ids]
level: practitioner
status: docs-checked
description: "Declare, implement and consume Dagger interfaces in Go, Python and TypeScript so Functions accept any structurally compatible object, plus the object ID notes."
sources: [https://docs.dagger.io/0.21/extending/interfaces]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Dagger interfaces

Goal: let a Function accept or return any object that exposes a required set of functions, independent of concrete type or SDK language (Dagger 0.21 docs). Checking is structural: compatible objects (including from dependencies or other SDKs) satisfy the interface, and interfaces can satisfy other interfaces.

## Declare

Go: embed `DaggerObject`; name the arguments (they become GraphQL argument names). Scalar/array returns need `ctx context.Context` and `error`; chainable object returns must not return `error`.

```go
type Fooer interface {
	DaggerObject
	Foo(ctx context.Context, bar int) (string, error)
}

func (m *MyModule) Foo(ctx context.Context, fooer Fooer) (string, error) {
	return fooer.Foo(ctx, 42)
}
```

Python: a `typing.Protocol` decorated `@dagger.interface`; non-chainable results must be `async`.

```python
@dagger.interface
class Fooer(typing.Protocol):
    @dagger.function
    async def foo(self, bar: int) -> str: ...
```

TypeScript: a plain `interface`; wrap return types in `Promise<T>`; use a method signature (`foo(bar: number): Promise<string>`) or property signature; name the parameters.

## Implement

No Dagger-specific `implements` marker is required: expose every required function with compatible argument and return types. Native `implements` (TypeScript: `class Example implements Fooer`) is optional, for editor/compiler checks.

```go
func (m *Example) Foo(ctx context.Context, bar int) (string, error) {
	return fmt.Sprintf("number is: %d", bar), nil
}
```

## Use

Pass any implementing object to the interface-typed argument. Dagger detects implementations across the current module and dependencies.

- Go: codegen produces local `As<Interface>()` adapters (client-side conversion, no GraphQL call, no network): `dag.MyModule().Foo(ctx, dag.Example().AsMyModuleFooer())`.
- Python / TypeScript: structural typing, pass directly: `dag.my_module().foo(dag.example())` / `dag.myModule().foo(dag.example())`.

## Object IDs

Interfaces are real GraphQL interfaces. All object IDs use the standard `ID` scalar; `@expectedType` directives keep SDK signatures typed, and loading uses `node(id:)` and the built-in `Node` interface instead of per-type `loadFooFromID` fields. For raw IDs in Go use `dagger.Ref[T](client, id)` (lazy) or `dagger.Load[T](ctx, client, id)` (verifies the type); generated Go interface clients have `Concrete(ctx)` returning a `Node` for a type switch. In raw GraphQL use `node(id:)` with an inline fragment.

## Related

computing-software.devops-ci-cd.dagger.custom-object-types

## Checked

2026-11-07

Read extending/modules/interfaces.mdx in full (live slug /extending/interfaces; the cited /extending/modules/interfaces URL is a file path that 404s, fixed in sources) and the Go, Python and TypeScript declaration snippets, the Go and TypeScript implementation snippets and the Go, Python and TypeScript usage snippets (Python implementation snippet not opened). Confirmed structural checking, the Go DaggerObject embedding and context/error rules, the Python Protocol with @dagger.interface and async rule, the TypeScript Promise and signature rules, the optional implements marker, the As<Interface>() adapters, and the object ID section including dagger.Ref, dagger.Load and Concrete(ctx). No claim removed.

Method: documentation only; no commands were run.
