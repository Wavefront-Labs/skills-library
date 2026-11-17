---
id: computing-software.web-development.storybook.vitest-addon-options
name: vitest-addon-options
category: computing-software
field: web-development
product: storybook
tags: [storybooktest-plugin, vitest-config, test-tags, configdir, storybookurl]
level: advanced
status: docs-checked
description: "Configure the storybookTest Vitest plugin options: configDir, storybookScript, storybookUrl, tags and more."
sources:
  - https://storybook.js.org/docs/writing-tests/integrations/vitest-addon
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# storybookTest plugin options

Goal: tune how Vitest turns stories into tests.

`storybookTest` is exported from `@storybook/addon-vitest/vitest-plugin`. Options:

- `configDir` (default `.storybook`): location of the Storybook config relative to the working directory. Required if yours is elsewhere.
- `storybookScript`: script Vitest runs to start Storybook in watch mode, only if Storybook at `storybookUrl` is not already available.
- `storybookUrl` (default `http://localhost:6006`): used for internal checks and links to the story on failures.
- `tags`: `{ include, exclude, skip }`. Defaults `include: ['test']`, `exclude: []`, `skip: []`.
  - `include`: stories tested
  - `exclude`: not tested and not counted
  - `skip`: not tested but counted as skipped
- `disableAddonDocs` (default `true`): MDX imports are mocked during tests; set `false` only if stories need to parse MDX.
- `initialGlobals`: globals applied in tests.

```ts
storybookTest({
  configDir: '.storybook',
  tags: { include: ['test'], exclude: ['experimental'], skip: ['flaky'] },
})
```

If the same tag is in both `include` and `exclude`, `exclude` takes precedence. The tags are annotations defined in a story, meta or preview. `initialGlobals` mirrors `initialGlobals` in `.storybook/preview.*` but is applied per Vitest project, and the plugin's own values take precedence over Storybook's.

## Checked

Method: 2026-11-08 compared against the Storybook docs source mdx for the Vitest addon (writing-tests/integrations/vitest-addon), Options and tags sections. All option names, defaults and tag semantics match the page. Replaced an unsupported `!test` tag claim and an invented "Verify" step with the page's exclude-precedence note.
