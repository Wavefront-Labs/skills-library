---
id: computing-software.devops-ci-cd.dagger.llm-env-agents
name: llm-env-agents
category: computing-software
field: devops-ci-cd
product: dagger
tags: [dagger, llm, env, agents, ai, prompt]
level: practitioner
status: docs-checked
description: "Build Dagger LLM agents by describing an Env with typed inputs and outputs (string, container, directory, file) and a prompt, then reading the declared output."
sources: [https://docs.dagger.io/0.21/getting-started/types/llm, https://docs.dagger.io/0.21/getting-started/types/env]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# LLM and Env types for agents (Dagger 0.21 docs)

Goal: give an LLM a defined environment of inputs and wanted outputs, and get typed results back.

- `Env`: `withStringInput`, `withContainerInput`, `withDirectoryInput`, `withFileInput`, `with[Object]Input`, matching `with...Output`, plus `input`/`inputs`/`output`/`outputs`.
- `LLM`: `withEnv`, `withPrompt`, `withPromptFile`, `withPromptVar`, `withModel`, `model`, `lastReply`, `history`.
- Inputs are referenced in the prompt as `$name`.

## Pattern (Go)

```go
environment := dag.Env().
	WithStringInput("question", question, "the question").
	WithStringOutput("answer", "the answer to the question")

work := dag.LLM().
	WithEnv(environment).
	WithPrompt(`... Your question is: $question`)

return work.Env().Output("answer").AsString(ctx)
```

Output conversion matches the declared type: `.AsString(ctx)`, `.AsContainer()`, `.AsDirectory()`, `.AsFile()`.

## Variants from the docs

- Container in, container out: `WithContainerInput("base", dag.Container().From("alpine:latest"), "a base container to use")` and `WithContainerOutput("result", "the updated container")`; inspect with `dagger call agent terminal`.
- Directory in, directory out: `WithDirectoryInput("source", dag.Git("github.com/dagger/dagger").Branch("main").Tree(), ...)`, `WithDirectoryOutput("result", ...)`; the prompt asks for translations into a `translations` directory; run `dagger call agent export --path=/tmp/out`.
- Mixed: container (golang) and directory inputs, `WithFileOutput("file", "the built Go executable")`, `.AsFile()`; `dagger call agent export --path=/tmp/out/myfile`.
- Coding agent: a module `CodingAgent` with `GoProgram(assignment string)` giving `$builder` (a `golang` container with `WithWorkdir("/app")`) and output `completed`; the prompt tells it to build the code and not stop until it builds.

## Observed in the examples

The example prompts say what to modify, what not to touch (for example, "Do not modify any other files") and what to return. Inputs take their description as the third argument (`WithStringInput("question", question, "the question")`); outputs take it as the second (`WithStringOutput("answer", "the answer to the question")`).

## Gaps

The pages do not cover provider configuration or model selection credentials.

## Checked

2026-11-07

Read getting-started/types/llm.mdx and types/env.mdx in full (both slugs return 200). Both pages are thin wrappers, so I also read the partials they import: types/_llm.mdx and _env.mdx (the operation tables), and the cookbook/agents partials _build-coding-agent, _env-use-strings, _env-use-containers, _env-use-directories and _env-use-multiple-types, plus the Go snippet files env-use-strings, env-use-containers, env-use-directories, env-use-multiple-types and the quickstart part1 main.go; other language tabs were not opened. Confirmed every LLM and Env operation name, withStringInput and the input/output argument orders from the snippets, the as-type conversions, the four variants with their dagger call commands and the coding agent. Corrected the tip that claimed descriptions go in the third argument for both inputs and outputs: outputs take the description as the second argument. The tips are now labelled as observations from the example prompts.

Method: documentation only; no commands were run.
