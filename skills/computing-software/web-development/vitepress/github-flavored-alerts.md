---
id: computing-software.web-development.vitepress.github-flavored-alerts
name: github-flavored-alerts
category: computing-software
field: web-development
product: vitepress
tags: [vitepress, github-alerts, gfm-alerts, note-tip-important-warning-caution, gradedcontainers, callouts]
level: intro
status: docs-checked
description: "Write GitHub-style alerts (NOTE, TIP, IMPORTANT, WARNING, CAUTION), custom titles, and enable graded severity colours."
sources:
  - https://raw.githubusercontent.com/vuejs/vitepress/main/docs/en/guide/markdown.md
  - https://raw.githubusercontent.com/vuejs/vitepress/main/docs/en/reference/default-theme-config.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
VitePress renders GitHub-flavored alerts the same as custom containers:

```md
> [!NOTE]
> Highlights information users should take into account, even when skimming.

> [!TIP]
> Optional information to help a user be more successful.

> [!IMPORTANT]
> Crucial information necessary for users to succeed.

> [!WARNING]
> Critical content demanding immediate user attention due to potential risks.

> [!CAUTION]
> Negative potential consequences of an action.
```

Differences from GitHub:
- Text after the marker becomes the title: `> [!NOTE] Custom Title`.
- Containers you registered yourself (`customContainers`) work as alert types too.
- `[!DANGER]` is a VitePress extension; on GitHub it renders as a plain blockquote.

**Colours.** By default the colours match GitHub's, so caution and danger are both red and warning is yellow. Set `themeConfig.gradedContainers: true` (default `false`) to colour containers, alerts and badges on a graded severity scale: danger red, warning orange, caution yellow.

## Checked

2026-11-04. Confirmed against the VitePress Markdown guide (GitHub-flavored Alerts, Registering New Containers) and the default-theme-config page (gradedContainers: boolean, default false, colours containers, alerts and badges). Removed: the README-compatibility remark and the Verify step.

Method: documentation only; no commands were run.
