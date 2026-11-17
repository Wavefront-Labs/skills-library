---
id: computing-software.devops-ci-cd.dagger.module-inline-documentation
name: module-inline-documentation
category: computing-software
field: devops-ci-cd
product: dagger
tags: [dagger, documentation, modules, docstrings, cli-help, annotations]
level: practitioner
status: docs-checked
description: "Document Dagger modules, functions, arguments and object fields in Go, Python, TypeScript, PHP and Java so descriptions appear in dagger functions and --help."
sources: [https://docs.dagger.io/0.21/extending/documentation]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Inline documentation for Dagger modules

Goal: have module, function and argument descriptions show in the API and CLI (`dagger functions`, `dagger call ... --help`, `.help`). The same text is later handed to LLMs as tool docs (see llm-integration-environments). Dagger 0.21 docs.

## Go
Plain comments. A comment block above `package main` documents the module; comments above methods document functions; comments above parameters document arguments:
```go
// A simple example module to say hello.

// Further documentation for the module here.

package main

// Return a greeting.
func (m *MyModule) Hello(
	// Who to greet
	name string,
	// The greeting to display
	greeting string,
) string { ... }
```
Objects: comment on the struct documents the type; constructor parameter comments document fields (`// The name of the user.`).

## Python
Use docstrings for the module (top of file), the `@object_type` class and each `@function`. Annotate arguments and fields with `Annotated[str, Doc("Who to greet")]` using `dagger.Doc` (an alias of `typing_extensions.Doc`):
```python
@object_type
class MyModule:
    """Simple hello functions."""

    @function
    def hello(
        self,
        name: Annotated[str, Doc("Who to greet")],
        greeting: Annotated[str, Doc("The greeting to display")],
    ) -> str:
        """Return a greeting."""
```
Object fields: `name: Annotated[str, Doc("The name of the user.")]`.

## TypeScript, PHP, Java
TypeScript: a doc comment above the imports documents the module; a doc comment on each `@func()` method documents the function, with `@param name description` lines for arguments. Object fields are documented by doc comments on the constructor parameters.

PHP: `#[Doc('...')]` attributes (from `Dagger\Attribute\Doc`) on the class, on each `#[DaggerFunction]` method and on each parameter.

Java: javadoc on each `@Function` method with `@param` lines. The module doc goes in `package-info.java` as a javadoc above `@Module` on the package declaration `io.dagger.modules.mymodule` (importing `io.dagger.module.annotation.Module`). Object fields: javadoc `@param` lines on the constructor.

## Result
`dagger functions` lists `hello  Return a greeting.` and `loud-hello  Return a loud greeting.`. `dagger call hello --help` shows the description, USAGE `dagger call hello [arguments]`, and ARGUMENTS such as `--greeting string   The greeting to display [required]`. For objects, `dagger call --help` shows `--age int   The age of the user. [required]`.

## Gaps
The TypeScript, PHP and Java snippet bodies are not reproduced here; check the page for exact syntax.

## Checked

2026-11-07

Read extending/modules/documentation.mdx in full (live slug /extending/documentation matches the cited URL) and every snippet it embeds: Go main.go and object.go, Python main.py and object.py, TypeScript index.ts and object.ts, PHP main MyModule.php, and Java main and object MyModule.java (PHP object snippet not opened). Confirmed the Go comment placement, the Python docstring and Doc annotations and the dagger.Doc alias note, the Java package-info.java example, the dagger functions and dagger call --help sample outputs. Corrected the TypeScript/PHP/Java paragraph, which wrongly said all three use doc comments on the same pattern and that Java method docs go on the class: PHP uses #[Doc] attributes, TypeScript uses TSDoc with @param, Java uses javadoc on methods. The LLM tool-docs remark is not on this page; it rests on the llm page read for another skill.

Method: documentation only; no commands were run.
