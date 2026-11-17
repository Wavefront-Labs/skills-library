---
id: computing-software.devops-ci-cd.dagger.llm-agent-environments
name: llm-agent-environments
category: computing-software
field: devops-ci-cd
product: dagger
tags: [dagger, llm, agent, env, mcp, prompt, tool-use, quickstart]
level: practitioner
status: docs-checked
description: "Build a Dagger AI agent: an Env with typed inputs and outputs given to dag.LLM with a prompt, MCP exposure and attachment, prompt mode and model configuration."
sources: [https://docs.dagger.io/0.21/features/llm, https://docs.dagger.io/0.21/getting-started/quickstarts/agent]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Build an AI agent with Dagger LLM and Env

Goal: let an LLM complete a task using Dagger objects as tools (Dagger 0.21 docs).

## Concepts

The `LLM` type supports tool use: the model can discover and call Dagger Functions available in its environment. An `Env` declares inputs and outputs; each has a description that acts as declarative prompting. The LLM loops, calling tools, until it sets the output; the loop happens inside the LLM object.

## Setup

```shell
dagger init --sdk=go --name=coding-agent     # python, typescript, php, java also
```
Configure a provider via environment variables or a `.env` file, e.g. `OPENAI_API_KEY`, `ANTHROPIC_API_KEY`, `GEMINI_API_KEY`. Supported: OpenAI, Anthropic, Google, plus local Docker Model Runner and Ollama. Check with `llm | model` in Dagger Shell.

## Agent function (Go, from the quickstart)

```go
func (m *CodingAgent) GoProgram(assignment string) *dagger.Container {
	environment := dag.Env().
		WithStringInput("assignment", assignment, "the assignment to complete").
		WithContainerInput("builder",
			dag.Container().From("golang").WithWorkdir("/app"),
			"a container to use for building Go code").
		WithContainerOutput("completed", "the completed assignment in the Golang container")

	work := dag.LLM().
		WithEnv(environment).
		WithPrompt(`
			You are an expert Go programmer with an assignment to create a Go program
			Create files in the default directory in $builder
			Always build the code to make sure it is valid
			Do not stop until your assignment is completed and the code builds
			Your assignment is: $assignment
			`)

	return work.Env().Output("completed").AsContainer()
}
```
Run in Dagger Shell: `.help go-program`, `go-program "write a curl clone"`, then `go-program "write a curl clone" | terminal` (the result is cached, not recomputed).

## Troubleshooting from the page

If validation fails, add guidance to the prompt. The error "binding value is nil" means the LLM never set `completed`; adjust the prompt so it finishes and returns the container.

## MCP

Expose a module as an MCP server: `dagger -m <module> mcp` (stdio) for clients such as Claude Desktop, Cursor or Goose; only modules with no required constructor arguments are supported. To use external MCP servers, build a `Service` (e.g. a container running `mcp-language-server` with `AsService`) and attach it: `dag.LLM().WithEnv(environment).WithMCPServer("lsp", mcpServer).WithPrompt(...)`.

## Prompt mode

In Dagger Shell type `>` to enter prompt mode and chat; each input builds on previous ones.

Related: `computing-software.devops-ci-cd.dagger.agent-in-project-github`.

## Checked

2026-11-07

Read introduction/features/llm.mdx (live slug /features/llm; the old /introduction/features/llm URL returned 404, fixed in sources) and getting-started/quickstarts/agent/index.mdx in full, plus the Go part1 snippet main.go that both pages embed (the Python, TypeScript, PHP and Java snippet tabs were not opened). Confirmed the tool-use and Env description, the agent loop remark, dagger init with the five SDK names, provider environment variables and .env file, the supported provider list, llm | model, the go-program example and its Go code, the 'binding value is nil' troubleshooting text, the cached terminal run, MCP exposure with its constructor-argument limit, the WithMCPServer example and prompt mode with >. No corrections needed.

Method: documentation only; no commands were run.
