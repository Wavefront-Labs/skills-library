---
id: computing-software.devops-ci-cd.turborepo.turbo-json-agent-guidance-setting
name: turbo-json-agent-guidance-setting
category: computing-software
field: devops-ci-cd
product: turborepo
tags: [turborepo, agentguidance, agents-md, ai-coding-agents, root-only-option, turbo-json-option]
level: advanced
status: docs-checked
description: "Opt in with agentGuidance so turbo maintains a managed block in the root AGENTS.md when an AI coding agent is detected."
sources:
  - https://raw.githubusercontent.com/vercel/turborepo/main/apps/docs/content/docs/reference/configuration.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`agentGuidance` (default `false`) lets `turbo` maintain a managed block in the repository-root `AGENTS.md` when an AI coding agent is detected. The block points to documentation bundled with the installed `turbo` package. It is refreshed before repository-scoped commands; only Turborepo's own block is updated and existing instructions and other tools' blocks are preserved.

It is a **root-only option** and cannot be set in package-level `turbo.json` files. Opt in in either `turbo.json` or `turbo.jsonc`:

```json
{ "agentGuidance": true }
```

Opting out does not delete an existing `AGENTS.md` or Turborepo block. Existing repositories only receive or refresh guidance after opting in; new projects from the default starter include it immediately.

## Checked

2026-11-04. Read the `agentGuidance` entry of the configuration reference in full; default, root-only rule, managed block behaviour, opt-out and starter note all match. Removed the unsupported "Context" line about the intro and AI guide pages, the invented Verify step, and a closing paragraph that only restated the above. Thin skill: one option's worth of content.

Method: documentation only; no commands were run.
