---
id: computing-software.devops-ci-cd.dagger.extending-overview-modules-vs-sdk
name: extending-overview-modules-vs-sdk
category: computing-software
field: devops-ci-cd
product: dagger
tags: [dagger, modules, sdk, custom-applications, extending-dagger]
level: practitioner
status: docs-checked
description: "Decide whether to extend the Dagger API with a module or embed a Dagger SDK in your own application, using the capability trade-offs the docs list."
sources: [https://docs.dagger.io/0.21/extending/index]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Choose between a Dagger module and a custom application

Goal: pick the right way to extend Dagger (Dagger 0.21 docs).

## Method

Two routes exist:

1. **Dagger module**: custom Dagger Functions and custom types. Loading a module dynamically extends the Dagger API, so a client can call the core functions plus the module's functions. Modules can be shared and reused; the Daggerverse (daggerverse.dev) indexes public modules and Functions.
2. **Custom application**: embed a Dagger SDK (Go, TypeScript, Python, PHP) in your own program. Steps: install the SDK, initialize a Dagger client, call Dagger API methods to implement the workflow, run the program with `dagger run`.

Capability comparison from the docs:

| Capability | Module | Custom app |
|---|---|---|
| Pre-initialized Dagger API client | yes | no |
| Direct host access | no | yes |
| Direct third-party module access | yes | no |
| Cross-language interoperability | yes | no |

Rule of thumb that follows from the table: choose a module for reusable, shareable, cross-language Functions; choose a custom application when the program itself needs direct host access.

## Related skills

- computing-software.devops-ci-cd.dagger.custom-application-sdk-embedding
- computing-software.devops-ci-cd.dagger.module-layout-and-runtime
- computing-software.devops-ci-cd.dagger.writing-dagger-functions

## Checked

2026-11-07

Read in full from the docs source: extending/index.mdx. Every claim matched. No corrections needed.

Method: documentation only; no commands were run.
