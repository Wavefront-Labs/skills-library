---
id: computing-software.devops-ci-cd.turborepo.editor-integration-schema-eslint-and-lsp
name: editor-integration-schema-eslint-and-lsp
category: computing-software
field: devops-ci-cd
product: turborepo
tags: [turborepo, editor-integration, json-schema, turbo-json-schema, eslint-config-turbo, turborepo-lsp, vscode-extension, node-modules-schema]
level: practitioner
status: docs-checked
description: "Get auto-complete for turbo.json with a versioned or node_modules $schema, lint env vars with eslint-config-turbo, and install the Turborepo LSP."
sources:
  - https://raw.githubusercontent.com/vercel/turborepo/main/apps/docs/content/docs/getting-started/editor-integration.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
**JSON Schema.** Add `$schema` to `turbo.json` for documentation and linting of invalid configuration.

Sourcing from the web: starting with Turborepo 2.5.7, versioned schemas exist as subdomains in the form `https://v<version>.turborepo.dev/schema.json` (the version uses a dash separator). The unversioned `https://turborepo.dev/schema.json` works with older versions or if you prefer it. A web schema needs no package-manager install for validation, and the versioned form matches your installed `turbo` version.

Sourcing from `node_modules`: starting in Turborepo 2.4, `schema.json` is in `node_modules` after installing:

```json
{ "$schema": "./node_modules/turbo/schema.json" }
```

Install `turbo` at the repository root so the path points at the root `node_modules`. In Package Configurations you may need `../../node_modules/turbo/schema.json`.

**Environment variable linting.** `eslint-config-turbo` extends your ESLint setup to check that environment variables are accounted for.

**Turborepo LSP.** Gives more auto-complete and linting than the schema: hints for invalid globs, references to non-existent tasks or packages, and extra repository visibility tools. Install it from the VS Code marketplace (`Vercel.turbo-vsc`). It can be used with any editor supporting the Language Server Protocol; the docs ask you to log a request in the issue tracker for other editors.

## Checked

2026-11-04. Read in full from the vercel/turborepo docs source (apps/docs/content/docs/: getting-started/editor-integration); commands, flags, key names, defaults and example values were matched against it. Removed: the Verify step the page does not support.

Method: documentation only; no commands were run.
