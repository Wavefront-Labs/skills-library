---
id: computing-software.web-development.storybook.docs-mode-and-code-panel
name: docs-mode-and-code-panel
category: computing-software
field: web-development
product: storybook
tags: [docs-mode, code-panel, storysource, source-code, publish-docs]
level: practitioner
status: docs-checked
description: "Preview and publish documentation-only builds with --docs and enable the Code panel for story source."
sources:
  - https://storybook.js.org/docs/writing-docs/build-documentation
  - https://storybook.js.org/docs/writing-docs/code-panel
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Docs mode and the Code panel

Goal: ship docs-only Storybook output and show story code.

Docs mode:

```json
{
  "scripts": {
    "storybook-docs": "storybook dev --docs",
    "build-storybook-docs": "storybook build --docs"
  }
}
```
Storybook shows only documentation. Caveats: the top-level item is the component's primary story, stories are flattened with different icons, and there is no toolbar. The build outputs to `storybook-static`.

Code panel (replaces the Storysource addon, discontinued in Storybook 9):
- Enabled by default when `@storybook/addon-docs` is installed.
- Disable globally with `parameters.docs.codePanel = false` in the preview file; override per component or story with `true` or `false`.
- It renders the same snippet as the Source doc block.

Verify: the Code panel appears under the canvas and docs mode shows no toolbar.

## Checked
Date: 2026-11-04. Read the Build documentation and Code panel pages (storybookjs/storybook main branch docs, commit e4ec607).
Confirmed: scripts, caveats, output folder, Code panel defaults and parameter, Storysource replacement.
Removed: a claim that the panel replaces args with their values; added the Code panel page as a source.
Method: documentation only; no commands were run.
