---
id: computing-software.devops-ci-cd.dagger.typescript-module-runtime
name: typescript-module-runtime
category: computing-software
field: devops-ci-cd
product: dagger
tags: [dagger, typescript, runtime, bun, deno, package-manager, dagger-json, include-filters]
level: practitioner
status: docs-checked
description: "Configure a Dagger module: dagger.json include filters, and for TypeScript the runtime (node, bun, deno), package manager, base image and bundled or vendored SDK."
sources: [https://docs.dagger.io/0.21/reference/configuration/modules]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Module configuration: dagger.json filters and TypeScript runtime

Goal: tune how a module loads and, for TypeScript modules, which runtime and package manager run it. Dagger 0.21 docs.

## dagger.json

Created by `dagger init`/`dagger develop` and kept current by `dagger config`/`dagger install`. Schema: docs.dagger.io/reference/dagger.schema.json. The `include` field adds or excludes files when loading the module (default: `dagger.json` plus the module source dir). Prefix patterns with `!` to exclude, e.g. big caches during local development. Filters apply only to loading the module, not to Directory arguments of functions.

## Runtime (package.json)

Default Node.js (via tsx). Bun and Deno are experimental.

```json
"dagger": { "runtime": "node@20.15.0" }
```

Values: `node`, `node@<version>`, `bun`, `bun@1.0.11`. For Deno there is no field: a `deno.json` (from `deno init`) triggers it. Bun is also auto-detected from `bun.lock`/`bun.lockb`. The module `source` must be the same directory as `bun.lock` or `deno.json`. Auto-detection order: `package-lock.json`, `yarn.lock` or `pnpm-lock.yaml` mean node; else bun lock files mean bun; `deno.json`/`deno.lock` mean deno; otherwise node. The page calls this a fallback, not explicit configuration.

## Package manager

Set `"packageManager": "npm@10.8.2"` (default npm 10.7.0), `"yarn@1.22.21"` (default yarn 1.22.22, the overall default), or `"pnpm@9.9"` (default pnpm 8.15.4). Bun runtime uses bun. Yarn 3+ gets a generated `.yarnrc.yml` with `nodeLinker: node-modules`; pnpm gets a `pnpm-workspace.yml` listing `./sdk`. Defaults can change; set it explicitly.

## Base image

`"dagger": { "baseImage": "node:23.2.0-alpine@sha256:..." }` for advanced needs (extra env vars, auth files, OS packages). Only Alpine-based images are supported; stay close to the default image.

## Bundled vs vendored SDK

Default: bundled SDK mapped in `tsconfig.json` paths to `./sdk/index.ts`. To vendor: `rm -rf ./sdk`, `npm pkg set "dependencies[@dagger.io/dagger]=./sdk"`, `dagger develop` (paths become `./sdk/src`; slower). To revert: `rm -rf ./sdk`, `npm pkg delete "dependencies[@dagger.io/dagger]"`, `dagger develop`.

## Related

computing-software.devops-ci-cd.dagger.cli-module-lifecycle, computing-software.devops-ci-cd.dagger.ide-setup.

## Checked

2026-11-07

Read reference/configuration/modules.mdx in full (live slug /reference/configuration/modules matches the cited URL); it embeds no snippet files. Confirmed the dagger.json include filters and their default and scope, the ! exclude tip, the Node/Bun/Deno runtime values and experimental status, the lock-file and deno.json auto-detection order, the same-directory source requirement, the npm/yarn/pnpm versions and defaults, the generated .yarnrc.yml and pnpm-workspace.yml, the Alpine-only base image note, and the bundled and vendored SDK commands and tsconfig paths. The JSON schema link and the linked Directory filters page were not opened. No corrections needed.

Method: documentation only; no commands were run.
