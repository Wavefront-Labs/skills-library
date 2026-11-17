---
id: computing-software.web-development.storybook.autodocs-setup
name: autodocs-setup
category: computing-software
field: web-development
product: storybook
tags: [autodocs, docs-page, auto-generated-docs, docs-tag, documentation]
level: practitioner
status: docs-checked
description: "Generate documentation pages from stories with the autodocs tag and customise the page name."
sources:
  - https://storybook.js.org/docs/writing-docs/autodocs
  - https://storybook.js.org/docs/api/main-config/main-config-tags
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Autodocs

Goal: get a docs page per component automatically.

Autodocs is driven by tags. If a CSF file has at least one story tagged `autodocs`, a docs page is created. Enable for everything in the preview file:

```ts
export default definePreview({ tags: ['autodocs'] });
```
or at component (meta `tags`) or single story level. Opt out with `tags: ['!autodocs']` on a component or story.

Options in `main.ts`:

```ts
docs: { defaultName: 'Docs', docsMode: false },
```
`defaultName` renames the page (default `Docs`); `docsMode` shows only documentation in the sidebar (usually set with the `--docs` CLI flag).

Requirements: the docs addon (`@storybook/addon-docs`) registered via `addonDocs()` in the preview `addons`. Storybook infers metadata (args, argTypes, parameters) and builds the page from the Title, Subtitle, Description, Primary, Controls and Stories doc blocks.

Enable a table of contents with `parameters.docs.toc`. Hide tagged stories from docs pages with `hideFromAutodocs` on a tag configured in `main.ts` (`tags: { internal: { hideFromAutodocs: true } }`).

Verify: a `Docs` entry appears under the component in the sidebar.

## Checked
Date: 2026-11-04. Read the Autodocs, main-config docs, main-config tags and Tags pages (storybookjs/storybook main branch docs, commit e4ec607).
Confirmed: tag behavior and opt-out, `defaultName` default, `docsMode` and `--docs`, `hideFromAutodocs`.
Method: documentation only; no commands were run.
