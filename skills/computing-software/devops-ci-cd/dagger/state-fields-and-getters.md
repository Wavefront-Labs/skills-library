---
id: computing-software.devops-ci-cd.dagger.state-fields-and-getters
name: state-fields-and-getters
category: computing-software
field: devops-ci-cd
product: dagger
tags: [dagger, state, getters, fields, constructors, private-fields, modules]
level: practitioner
status: docs-checked
description: "Expose or hide Dagger module object state as functions: Go public/+private fields, Python dagger.field, TypeScript @func(), PHP attributes and Java rules."
sources: [https://docs.dagger.io/0.21/extending/state]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# State and getters in Dagger modules

Goal: expose object state as Dagger Functions without hand-writing getters, and keep some state private. Dagger 0.21 docs.

## Per-language rules
- Go: only public struct fields are exposed. Mark a public field private with `// +private`. Constructor defaults: `// +default="Hello"`.
- Python: `dagger.field(default=...)` is a wrapper of `dataclasses.field` that also creates the getter. It supports only `init: bool`, and puts both `default` and `default_factory` in a single `default` parameter. A plain `name: str = "World"` attribute is the non-exposed constructor argument case in the docs' example.
- TypeScript: only members decorated with `@func()` are exposed, regardless of `private`/`protected`/`public`.
- PHP: only `public` fields with the `#[DaggerFunction]` attribute.
- Java: all public fields are exposed; others can be exposed with `@Function`; mark `transient` to prevent serialization entirely.

## Go example
```go
type MyModule struct {
	// The greeting to use
	Greeting string
	// Who to greet
	// +private
	Name string
}

func New(
	// The greeting to use
	// +default="Hello"
	greeting string,
	// Who to greet
	// +default="World"
	name string,
) *MyModule { return &MyModule{Greeting: greeting, Name: name} }

func (m *MyModule) Message() string { return fmt.Sprintf("%s, %s!", m.Greeting, m.Name) }
```

## TypeScript example
```typescript
@object()
class MyModule {
  @func() greeting: string
  name: string   // not exposed
  constructor(greeting: string = "Hello", name: string = "World") { ... }
  @func() message(): string { return `${this.greeting}, ${this.name}!` }
}
```

## Verify
`dagger call --help` (or `.help my-module` in Dagger Shell) should list FUNCTIONS `greeting` ("The greeting to use") and `message`, with ARGUMENTS `--greeting string (default "Hello")` and `--name string (default "World")`: only `greeting` is a function, `name` stays a constructor argument only.

Related: module-inline-documentation.

## Checked

2026-11-07

Read extending/modules/state.mdx in full (live slug /extending/state matches the cited URL) and all five state-functions snippets it embeds (Go, Python, TypeScript, PHP and Java). Confirmed the Go public-field rule and the +private and +default pragmas, the dagger.field wrapper description and its limits, the plain attribute case, the TypeScript @func() rule, the PHP public field plus #[DaggerFunction] rule, the Java public-field, @Function and transient rules, and the expected dagger call --help output. No corrections needed.

Method: documentation only; no commands were run.
