---
id: computing-software.web-development.mkdocs.page-template-key
name: page-template-key
category: computing-software
field: web-development
product: mkdocs
tags: [page-template, template-key, meta-data, main-html]
level: practitioner
status: docs-checked
description: "Render one MkDocs page with a different theme template using the template meta-data key, and the template path requirement."
sources:
  - https://raw.githubusercontent.com/mkdocs/mkdocs/master/docs/user-guide/writing-your-docs.md
  - https://raw.githubusercontent.com/mkdocs/mkdocs/master/docs/dev-guide/themes.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
By default every Markdown page renders with the theme's `main.html`. The predefined meta-data key `template` selects another template for that page:

```text
---
template: landing.html
title: Welcome
---
Page text...
```

Requirement: the template file must be available on the path(s) defined in the theme's environment, for example inside a `theme.custom_dir`:

```yaml
theme:
  name: mkdocs
  custom_dir: custom_theme/
```

with `custom_theme/landing.html` present (the file name is your choice).

Other predefined key: `title` (see `page-title-resolution`). Any other meta keys are available to the template as `page.meta`.

## Checked

2026-11-04. Confirmed against the MkDocs user guide "Writing your docs" (Meta-Data, template key) and the Developing Themes page (`main.html`, `theme.custom_dir`, `page.meta`). Removed the Gotcha and Verify lines, which the pages do not state.
Method: documentation only; no commands were run.
