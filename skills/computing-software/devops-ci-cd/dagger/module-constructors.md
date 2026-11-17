---
id: computing-software.devops-ci-cd.dagger.module-constructors
name: module-constructors
category: computing-software
field: devops-ci-cd
product: dagger
tags: [dagger, constructors, modules, default-values, dataclasses]
level: practitioner
status: docs-checked
description: "Write a custom Dagger module constructor with defaults, including complex-typed defaults and the Python async create factory; know the public-field rule."
sources: [https://docs.dagger.io/0.21/extending/constructors]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Custom module constructors

Goal: accept module-wide configuration (Dagger 0.21 docs). Every module has a constructor; the generated default has no arguments. A custom one exposes its parameters as flags directly on the `dagger` command. A module has only one constructor: constructors of custom types are not registered, they are built by the function that chains them.

## Simple constructor

Go: a package-level `New` function with pragma defaults.

```go
func New(
	// +default="Hello"
	greeting string,
	// +default="World"
	name string,
) *MyModule {
	return &MyModule{Greeting: greeting, Name: name}
}

type MyModule struct {
	Greeting string
	Name     string
}
```

Python: `@object_type` classes are dataclasses, so fields become constructor arguments.

```python
@object_type
class MyModule:
    greeting: str = "Hello"
    name: str = "World"
```

TypeScript: `constructor(greeting = "Hello", name = "World")` assigning `this.greeting`/`this.name`. PHP: the magic method `__construct` (only public methods with `#[DaggerFunction]` are registered). Java: a public constructor, plus a public empty constructor needed for deserialization.

```shell
dagger call --name=Foo message        # Hello, Foo!
dagger -c '. --name=Foo | message'
```

**Public fields rule**: constructor fields used by other functions must be public (Go, TypeScript). Dagger serializes state and omits private fields, producing unexpected results.

## Defaults for complex types

Declare the type explicitly even if inferable so the SDK extends the GraphQL schema correctly.

Go: `ctr *dagger.Container` with `// +optional`; if nil, `ctr = dag.Container().From("alpine:3.14.0")`. Python: `ctr: dagger.Container = dataclasses.field(default_factory=lambda: dag.container().from_("alpine:3.14.0"))`. TypeScript must use `??`, not a classic default argument:

```typescript
constructor(ctr?: Container) {
  this.ctr = ctr ?? dag.container().from("alpine:3.14.0")
}
```

`dagger call version` then prints `VERSION_ID=3.14.0` for the docs example.

## Python extras

- `__post_init__` runs at the end of the generated constructor; use it with `field(init=False)` for values derived from other fields (the field is still required to be initialized).
- `dagger.field()` exposes the attribute as a getter Function and keeps it as object state; it takes a single `default` for values or factories, unlike `dataclasses.field` (separate `default`/`default_factory`).
- Mutable or dynamic defaults: `dataclasses.field(default_factory=list)` or `dagger.field(default=...)`.
- Async default: replace `__init__` with a classmethod that must be named `create`:

```python
@classmethod
async def create(cls, parallelize: Annotated[int | None, Doc("Number of parallel processes to run")] = None):
    if parallelize is None:
        parallelize = int(await dag.container().from_("alpine").with_exec(["nproc"]).stdout())
    return cls(parallelize=parallelize)
```

## Related

computing-software.devops-ci-cd.dagger.custom-object-types

## Checked

2026-11-07

Read extending/modules/constructors.mdx in full (live slug /extending/constructors; the cited /extending/modules/constructors URL is a file path that 404s, fixed in sources). Also read the partial _complex_constructor_output.mdx and the Go simple and default-object snippets, Python simple, default-object, complex, factory and async snippets, TypeScript simple and default-object snippets and the PHP simple snippet. The Java snippet is not a constructor example, so the Java statement rests on the page's info box only. Confirmed the single-constructor note, the public-fields rule for Go and TypeScript, the +default pragmas, dataclass behaviour, __post_init__ and field(init=False), dagger.field versus dataclasses.field, factory functions, the create classmethod requirement, the TypeScript ?? rule, and the VERSION_ID=3.14.0 output. No claim removed.

Method: documentation only; no commands were run.
