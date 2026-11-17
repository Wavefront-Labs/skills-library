---
id: computing-software.web-development.astro.cli-check-sync-info
name: cli-check-sync-info
category: computing-software
field: web-development
product: astro
tags: [astro-check, astro-sync, astro-info, astro-preferences, telemetry]
level: practitioner
status: docs-checked
description: "Use astro check in CI, astro sync for generated types, astro info for bug reports, plus preferences, telemetry and create-key commands."
sources:
  - https://raw.githubusercontent.com/withastro/docs/main/src/content/docs/en/reference/cli-reference.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`astro check` runs diagnostics (including type-checking in `.astro` files) and exits with code 1 on errors; it is intended for CI. Flags: `--watch`, `--root <path-to-dir>`, `--tsconfig <path-to-file>`, `--minimumFailingSeverity <error|warning|hint>` (default `error`), `--minimumSeverity <error|warning|hint>` (default `hint`), `--preserveWatchOutput`, `--noSync`.

```shell
astro check --minimumFailingSeverity warning
```

`astro sync` generates TypeScript types for Astro modules: `.astro/types.d.ts`, `astro:content`, `astro:env`, `astro:actions`. `astro dev`, `astro build` and `astro check` run it too.

`astro info` prints environment information (Astro, Vite, Node, system, package manager, output, adapter, integrations), useful for issues. `--copy` copies the output to the clipboard.

`astro add` adds an integration to your config. `astro docs` opens the docs.

`astro preferences` manages per-user settings, scoped to the current project by default (stored in `.astro/settings.json`), or machine-wide with `--global`. Available: `devToolbar`, `checkUpdates`.

```shell
astro preferences list
astro preferences disable devToolbar
astro preferences disable --global devToolbar
astro preferences reset devToolbar
```

`astro telemetry disable|enable|reset` configures anonymous telemetry. To disable in CI, add the disable command to scripts or set `ASTRO_TELEMETRY_DISABLED`.

`astro create-key` generates a key for `ASTRO_KEY`, used to encrypt server island props.

## Checked

2026-11-04. Confirmed against the Astro CLI reference: astro check flags and defaults, sync outputs, info --copy, preferences scope and names, telemetry and create-key. Clarified the preferences storage scope.

Method: documentation only; no commands were run.
