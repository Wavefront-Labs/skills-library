---
id: computing-software.qa-testing-engineering.vitest.config-file-basics
name: config-file-basics
category: computing-software
field: qa-testing-engineering
product: vitest
tags: [vitest-config, vite-config-reuse, define-config, vitest-ide-extension]
level: intro
status: docs-checked
description: "Configure Vitest: it reads vite.config by default, a dedicated vitest.config takes test settings, defineConfig comes from vitest/config, plus the VS Code extension."
sources:
  - https://raw.githubusercontent.com/vitest-dev/vitest/main/docs/guide/index.md
  - https://raw.githubusercontent.com/vitest-dev/vitest/main/docs/guide/projects.md
  - https://raw.githubusercontent.com/vitest-dev/vitest/main/docs/guide/lifecycle.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Vitest reads your `vite.config.*` by default, so existing Vite plugins and configuration work out of the box. For test-specific settings, create a dedicated `vitest.config.*`.

```ts
import { defineConfig } from 'vitest/config'

export default defineConfig({
  test: {
    // test options go under the `test` key
  },
})
```

In a project config file, prefer `defineProject` from `vitest/config`: it flags options that projects do not support. To combine a shared config with a project one, use `mergeConfig` from `vitest/config`.

Config files are loaded in the main process during initialization; the phase can run again if the config file or one of its imports changes.

An official extension for Visual Studio Code adds IDE integration. See the Config Reference for each option.

## Checked

2026-11-04. Confirmed against guide/index.md (vite.config read by default, dedicated vitest.config, VS Code extension), guide/projects.md (`defineProject`, `mergeConfig`) and guide/lifecycle.md (config loaded in the initialization phase, rerun on change). Removed the extension's marketplace display name and a pointer to other skills.

Method: documentation only; no commands were run.
