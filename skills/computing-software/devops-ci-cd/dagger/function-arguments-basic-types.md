---
id: computing-software.devops-ci-cd.dagger.function-arguments-basic-types
name: function-arguments-basic-types
category: computing-software
field: devops-ci-cd
product: dagger
tags: [dagger, functions, arguments, optional-arguments, default-values, primitives]
level: practitioner
status: docs-checked
description: "Declare string, boolean, integer, float and array arguments on a Dagger Function, make them optional or give defaults, and pass them from the CLI."
sources: [https://docs.dagger.io/0.21/extending/modules/arguments]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Primitive, optional and default arguments

Goal: give a Dagger Function typed scalar arguments (Dagger 0.21 docs). From the CLI each argument becomes a flag; in Dagger Shell required arguments are positional and flags can go anywhere.

## Types

```go
func (m *MyModule) GetUser(ctx context.Context, gender string) (string, error)   // string
func (m *MyModule) Hello(shout bool) string                                     // boolean
func (m *MyModule) AddInteger(a int, b int) int                                 // integer
func (m *MyModule) AddFloat(a float64, b float64) float64                       // float
func (m *MyModule) Hello(names []string) string                                 // array
```

```python
def hello(self, shout: bool) -> str: ...
def add_integer(self, a: int, b: int) -> int: ...
def add_float(self, a: float, b: float) -> float: ...
def hello(self, names: list[str]) -> str: ...
```

```typescript
hello(shout: boolean): string
addInteger(a: number, b: number): number
hello(names: string[]): string
```

TypeScript floats: import the `float` type (`import type { float } from "@dagger.io/dagger"`) and use it for arguments and returns; it is a `number` underneath. Java accepts primitives or boxed types (`int`/`Integer`, `float`/`Float`, `boolean`/`Boolean`). PHP array arguments need `#[ListOfType]` to declare the item type.

Python/PHP: define type annotations even though the runtime does not enforce them; the SDK needs the typing information at runtime to report the schema. A Python function without a return annotation is declared `None`, i.e. the API `Void` type, and returning a string from it raises "cannot convert string to Void".

## Calling

```shell
dagger call get-user --gender=male
dagger call hello --shout=true
dagger call add-integer --a=1 --b=2        # 3
dagger call add-float --a=1.4 --b=2.7      # 4.1
dagger call hello --names=John,Jane         # arrays: comma-separated
```

Optional boolean flags: `--foo` or `--foo=true` sets true, `--foo=false` sets false. A host environment variable can be passed with shell syntax, e.g. `--greeting=$GREETING`.

## Optional arguments

An optional argument may be omitted without a CLI error.

- Go: add the pragma comment `// +optional` above the parameter.
- Python: `name: str | None`.
- TypeScript: `name?: string`.
- PHP: make the parameter nullable (omitted becomes `null`). PHP "optional" (has a default) differs from Dagger "optional" (can be omitted entirely).
- Java: use `Optional`; primitives cannot be optional, use boxed types. Non-optional arguments get an `Objects.requireNonNull` check.

## Default values

- Go: `// +default="world"` above the parameter.
- Python: `name: str = "world"`.
- TypeScript: `hello(name = "world")`.
- Java: `@Default("123")` must hold a JSON representation of the value; for strings `@Default("world")` is accepted and quotes added automatically.

`dagger call hello` then prints `Hello, world`. Passing null to an optional argument signals that no default should be used.

## Related

computing-software.devops-ci-cd.dagger.function-arguments-host-resources; computing-software.devops-ci-cd.dagger.function-arguments-secrets

## Checked

2026-11-07

Read in full from the docs source: extending/modules/arguments.mdx and the string, boolean, integer, float, array, optional and default-string snippets (Go, Python, TypeScript). Confirmed types, the TypeScript float import, PHP ListOfType, Java boxed types, Optional, Objects.requireNonNull and the @Default JSON rule, boolean flag forms, comma-separated arrays, the Python "cannot convert string to Void" error and the null-optional note. Reworded "annotations are mandatory" to match the page ("important to define them"). PHP and Java snippets were not read; PHP and Java claims rest on the prose notes.

Method: documentation only; no commands were run.
