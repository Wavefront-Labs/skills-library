---
id: computing-software.devops-ci-cd.dagger.platform-overview-use-cases
name: platform-overview-use-cases
category: computing-software
field: devops-ci-cd
product: dagger
tags: [dagger, overview, use-cases, sandbox, modules, portable-ci, monorepo, agentic-ci]
level: practitioner
status: docs-checked
description: "Decide whether Dagger fits a task and explain its platform pieces, sandbox model, module reuse and the portable, monorepo and agentic CI use cases."
sources: [https://docs.dagger.io/0.21/, https://docs.dagger.io/0.21/use-cases, https://docs.dagger.io/0.21/features/sandbox, https://docs.dagger.io/0.21/features/reusability, https://docs.dagger.io/0.21/examples]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Dagger platform overview and use cases

Goal: decide if Dagger suits a delivery-automation problem, and explain its parts to a team (based on the Dagger 0.21 docs).

## What it is

Dagger automates software delivery (build, test, ship). It runs locally, in a CI server or in the cloud; the only dependency is a container runtime such as Docker. The docs frame it as programmable, local-first, repeatable (tools run in containers, operations incremental by default) and observable (OpenTelemetry traces for every operation).

Platform components named by the docs: Types (the overview names containers, directories, files and LLMs), Functions (units of computation written with a typed SDK), Modules (packaged functions that dynamically extend the API when loaded), the CLI (with a terminal UI), the Engine and its GraphQL-based API, SDKs (client generator and server generator), and Dagger Cloud (Checks, Traces, Modules).

## Use cases

- Portable CI: workflows run identically on a laptop and in CI because each step runs in an isolated container; this removes "push and pray" and CI vendor lock-in.
- Monorepo CI: split CI into modules, share a build environment across projects, model cross-language dependencies (the docs cite a TypeScript docs builder depending on a Go CLI builder).
- Agentic CI: the `LLM` type gives native LLM integration with tool use; MCP support exposes modules as MCP servers; Dagger Shell has a natural-language prompt mode; OpenAI, Anthropic, Google, Docker Model Runner and Ollama are supported. See `computing-software.devops-ci-cd.dagger.llm-agent-environments`.

## Sandbox model

Functions are sandboxed with no direct access to the host environment, filesystem, services or SSH agent. Host resources reach a function only as typed arguments (`Directory`, `Socket`, `Service`, `Secret`), introduced at the top-level call; there is no implicit sharing to other modules.

## Reusability

Modules are source code, versioned by Git tags, with pinned dependencies; containerized functions avoid dependency conflicts; any number of modules may live in one repo. A Python function can call Go or TypeScript functions. The Daggerverse (daggerverse.dev) indexes public modules.

## Where to study real pipelines

The Examples page lists real repositories for portable CI, monorepos and agents, plus the Dagger Cookbook for filesystem, build, service, secret and error recipes.

Related: `computing-software.devops-ci-cd.dagger.install-dagger-cli`, `computing-software.devops-ci-cd.dagger.ci-workflow-quickstart`.

## Gaps

The overview pages do not give a decision matrix against other CI tools.

## Checked

2026-11-07

Read index.mdx (overview), introduction/use-cases.mdx, introduction/features/sandbox.mdx, introduction/features/reusability.mdx and introduction/examples.mdx in full; none embeds snippets or partials. Live slugs are /, /use-cases, /features/sandbox, /features/reusability and /examples; four of the cited URLs used the introduction/ file path and are corrected in sources. Confirmed the local-first and container runtime statement, the four framing words, OpenTelemetry traces, the platform components and Dagger Cloud features, the three use cases with their benefits and the TypeScript docs builder and Go CLI builder example, the LLM, MCP, prompt mode and provider statements, the sandbox model and typed argument list, the reusability bullets and Python-calls-Go example, the Daggerverse description, and the examples page contents. Trimmed the Types list, since the overview names only containers, directories, files and LLMs. Links to the cookbook pages and the other skills were not followed.

Method: documentation only; no commands were run.
