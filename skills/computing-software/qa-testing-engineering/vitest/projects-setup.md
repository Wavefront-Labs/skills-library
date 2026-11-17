---
id: computing-software.qa-testing-engineering.vitest.projects-setup
name: projects-setup
category: computing-software
field: qa-testing-engineering
product: vitest
tags: [test-projects, workspace-deprecated, project-globs, define-project]
level: practitioner
status: docs-checked
description: "Split one Vitest run into projects with test.projects using globs, config files or inline configs, with unique names, negation globs and the deprecated workspace file."
sources:
  - https://raw.githubusercontent.com/vitest-dev/vitest/main/docs/guide/projects.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Put `projects` in the root config. Entries can be globs, config file paths or inline configs.

```ts
import { defineConfig } from 'vitest/config'

export default defineConfig({
  test: {
    projects: [
      'packages/*',
      '!packages/excluded',
      { test: { name: 'unit', include: ['tests/unit/**/*.test.ts'], environment: 'node' } },
    ],
  },
})
```

- A glob that matches a folder makes it a project; a matched config file must be named `vitest.config*`, `vite.config*` or `vitest.<name>.config.*`.
- Project `name` values must be unique.
- Select projects on the CLI with `--project`, which supports `*` and `!` patterns.
- Nested projects get prefixed names such as `app (unit)`.
- The old workspace feature is deprecated since 3.2; use `projects`.
- Debug resolution with `DEBUG=vitest:projects`.

By default `process.cwd()` stays the directory you started Vitest from, not the project root.

## Checked

2026-11-04. Confirmed against guide/projects.md: projects as globs, files or inline configs, config file name rules, negation globs, unique names, `--project` with `*` and `!`, nested project prefixes, workspace deprecation since 3.2, `DEBUG=vitest:projects`, and the cwd note.

Method: documentation only; no commands were run.
