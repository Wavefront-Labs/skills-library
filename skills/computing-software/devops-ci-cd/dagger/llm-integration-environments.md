---
id: computing-software.devops-ci-cd.dagger.llm-integration-environments
name: llm-integration-environments
category: computing-software
field: devops-ci-cd
product: dagger
tags: [dagger, llm, agents, environments, prompts, env, ai, coding-agent]
level: practitioner
status: docs-checked
description: "Use Dagger's LLM and Env types to prompt a model, attach typed inputs and outputs (string, container, directory, file) and build a coding agent."
sources: [https://docs.dagger.io/0.21/extending/llm, https://docs.dagger.io/0.21/cookbook/agents]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# LLM integration and environments in Dagger

Goal: drive an LLM from Dagger with typed inputs and outputs. Dagger 0.21 docs.

## Prompts and replies (Dagger Shell)
- `llm | with-prompt "What tools do you have available?"`
- Long prompts: `llm | with-prompt-file ./prompt.txt`
- Read results with `LLM.lastReply()` / `last-reply` or the whole `LLM.history()`.
- Rate limits: Dagger detects them and retries with exponential backoff.
- Variables can interpolate other results:
```
source=$(container | from alpine | with-directory /src https://github.com/dagger/dagger | directory /src)
environment=$(env | with-directory-input 'source' $source 'a directory with source code')
llm | with-env $environment | with-prompt "Use the tools in the directory to read the first paragraph of the README.md file in the directory." | with-prompt "Reply with only the selected text." | last-reply
```
From a system shell wrap this in `dagger <<EOF ... EOF` and escape `$` as `\$`.

## Environments
An `Env` declares inputs and desired outputs. Any Dagger module given to the `LLM` becomes tools: every Dagger Function is callable by the model. Module documentation is passed to the model, so write good function docs (see module-inline-documentation); the page says not to over-describe the objects in prompts because that duplicates the automatic documentation.

Pattern (Go; Python/TypeScript/PHP/Java equivalents exist in the quickstart):
```go
environment := dag.Env().
	WithStringInput("assignment", assignment, "the assignment to complete").
	WithContainerInput("builder", dag.Container().From("golang").WithWorkdir("/app"), "a container to use for building Go code").
	WithContainerOutput("completed", "the completed assignment in the Golang container")

work := dag.LLM().WithEnv(environment).WithPrompt(`... Your assignment is: $assignment`)
return work.Env().Output("completed").AsContainer()
```
Reference inputs in the prompt as `$name`.

## Typed variants from the cookbook
- Strings: `WithStringInput("question", ...)`, `WithStringOutput("answer", ...)`, read `Output("answer").AsString(ctx)`; call `dagger call agent --question="what is an ion?"`.
- Containers: `WithContainerInput` plus `WithContainerOutput("result", ...)`, `AsContainer()`; inspect with `dagger call agent terminal`.
- Directories: `WithDirectoryInput("source", dir, ...)` plus `WithDirectoryOutput("result", ...)`, `AsDirectory()`; save with `dagger call agent export --path=/tmp/out`.
- Mixed: container and directory inputs, `WithFileOutput("file", ...)`, `AsFile()`; export the binary with `dagger call agent export --path=/tmp/out/myfile`.

## Gaps
The page does not list how to configure the model provider or credentials.

## Checked

2026-11-07

Read extending/modules/llm.mdx (live slug /extending/llm, returns 200) and cookbook/agents.mdx in full. The cookbook page only imports partials, so I also read the five cookbook/agents partials and the Go snippets env-use-strings, env-use-containers, env-use-directories, env-use-multiple-types and quickstart part1 main.go; other language tabs not opened. Confirmed with-prompt and with-prompt-file, lastReply and history, the rate-limit retry statement, the variable interpolation example, the module-to-tool statement, the Go env pattern and the four typed variants with their dagger call commands. Reworded the 'keep prompts short' advice to what the page actually says.

Method: documentation only; no commands were run.
