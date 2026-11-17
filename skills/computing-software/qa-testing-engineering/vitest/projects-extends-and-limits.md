---
id: computing-software.qa-testing-engineering.vitest.projects-extends-and-limits
name: projects-extends-and-limits
category: computing-software
field: qa-testing-engineering
product: vitest
tags: [projects-extends, merge-config, project-inheritance, unsupported-project-options]
level: advanced
status: docs-checked
description: "Know what a Vitest project inherits from the root config with extends, how arrays and tags merge, and which options projects do not support."
sources:
  - https://raw.githubusercontent.com/vitest-dev/vitest/main/docs/guide/projects.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
For inline projects, `extends: true` is the default since Vitest 5.0 (inherit root config). `extends: false` opts out; a path to another config file extends that one instead. File-based projects do not inherit automatically: combine them with `mergeConfig` from `vitest/config`.

```ts
export default defineConfig({
  test: {
    projects: [
      { extends: false, test: { name: 'isolated' } },
    ],
  },
})
```

Inheritance rules from the docs:
- Arrays are concatenated.
- `name`, `projects` and the root `globalSetup` are not inherited.
- A project's own `tags` replace the inherited ones.

Options not supported inside a project: `coverage`, `reporters`, `resolveSnapshotPath` and `attachmentsDir`. Set them at the root.

Use `defineProject` in project config files so unsupported options show up as type errors.

## Checked

2026-11-04. Confirmed against guide/projects.md: `extends` default since 5.0, `extends: false`, a path value, array concatenation, the not-inherited list, tags replacement, mergeConfig for file-based projects, and the unsupported options list.

Method: documentation only; no commands were run.
