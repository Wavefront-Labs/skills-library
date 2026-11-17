---
id: computing-software.web-development.appwrite.appwrite-functions-runtimes-specs
name: appwrite-functions-runtimes-specs
category: computing-software
field: web-development
product: appwrite
tags: [appwrite, functions, runtimes, specifications]
level: intro
status: docs-checked
description: "Pick a function runtime and version, and know which build options and specifications need a paid plan."
sources:
  - https://github.com/appwrite/website/blob/main/src/routes/docs/products/functions/runtimes/+page.markdoc
  - https://github.com/appwrite/website/blob/main/src/routes/docs/products/functions/functions/+page.markdoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: choose where your code runs.

Runtimes: the docs list Node.js, Bun, Deno, Go, Python, Python ML, Dart, PHP, Ruby, .NET, Java, Swift, Kotlin, Flutter, C++ and Rust, each with versioned identifiers such as `node-22`, `bun-1.3`, `python-3.12` or `go-1.25`. Not all runtimes are available on Appwrite Cloud (the page has a separate "Available on Cloud" tab, which for example omits .NET, Java, Swift, Kotlin and C++), so check it before choosing. Every deployment of a function uses the same runtime; change it under function > Settings > Runtime > Update, then redeploy.

Creating a function: you select a name, ID and runtime, then set the Entrypoint (the file the executor imports; it must export a valid entrypoint function) and Build settings (terminal commands run in the runtime container during the build; specify them to install dependencies). Entrypoint and build commands run relative to the Root directory when using Git. The Functions page recommends starting from a template.

Compute: under Settings > Resource limits you can set build and runtime specifications independently (CPU and memory tiers; the build spec applies while building, the runtime spec to each execution). On Appwrite Cloud, customizing specifications requires the Pro plan.

Build time limit on Cloud: 15 minutes on Free and 45 minutes on Pro and Scale.

Gotcha: runtime and build configuration changes require a redeploy to take effect.

## Checked

2026-11-04. Confirmed against the Appwrite docs pages Runtimes and Functions: the runtime list and version identifier style, the Cloud availability tab, the runtime-change steps, entrypoint and build settings, resource limits and the Pro requirement, build durations and the redeploy notes. Removed: the claim that Express builds need Pro, the `appwrite.json` CLI remark, the exact create-time field list including install commands, and the Verify step.
Method: documentation only; no commands were run.
