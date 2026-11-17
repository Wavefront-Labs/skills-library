---
id: computing-software.web-development.vitepress.site-metadata-title-description-titletemplate
name: site-metadata-title-description-titletemplate
category: computing-software
field: web-development
product: vitepress
tags: [vitepress, title, titletemplate, description, site-metadata, seo, meta-description]
level: practitioner
status: docs-checked
description: "Set site and per-page title, titleTemplate (with :title) and description, and know how the final page title is composed."
sources:
  - https://raw.githubusercontent.com/vuejs/vitepress/main/docs/en/reference/site-config.md
  - https://raw.githubusercontent.com/vuejs/vitepress/main/docs/en/reference/frontmatter-config.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
- `title` (default `VitePress`): the site title shown in the nav bar (default theme) and the default suffix for page titles. A page title is its first `<h1>` text plus the suffix: `title: 'My Awesome Site'` with `# Hello` yields `Hello | My Awesome Site`.
- `titleTemplate` (`string | boolean`): customizes the suffix or the entire title.
  - `titleTemplate: 'Custom Suffix'` yields `Hello | Custom Suffix`.
  - Use the `:title` token for full control: `titleTemplate: ':title - Custom Suffix'` yields `Hello - Custom Suffix`.
  - `false` disables suffixes.
- `description` (default `A VitePress site`): rendered as a `<meta>` tag in the page HTML.

All three can be overridden per page in frontmatter, or per directory:

```yaml
---
title: VitePress
titleTemplate: Vite & Vue powered static site generator
description: A custom description for this page
---
```

Practical advice:

- Give each page a unique, front-loaded `title` in frontmatter when the first `<h1>` is generic.
- Set `titleTemplate: false` on a page where the suffix would repeat the site name (`false` disables suffixes).
- Read the resolved values in components via `useData()` (`title`, `description`).

Verify: view-source and check `<title>` and the meta description for a page with and without overrides.

## Checked

2026-11-08. Read the VitePress docs source pages site-config (title, titleTemplate, description) and frontmatter-config. Confirmed defaults, the Hello | My Awesome Site and Custom Suffix examples, the :title token, false disabling suffixes, per-page and directory overrides, and the frontmatter example. Removed an unsourced claim about search engines and loosened the description tag wording.

Method: docs-only read of cited pages, 2026-11-08
