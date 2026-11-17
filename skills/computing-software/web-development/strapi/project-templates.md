---
id: computing-software.web-development.strapi.project-templates
name: project-templates
category: computing-software
field: web-development
product: strapi
tags: [strapi, templates, create-strapi, template-path, scaffolding]
level: intro
status: docs-checked
description: "Create a Strapi project from a template with create-strapi --template, and what a template contains."
sources:
  - https://raw.githubusercontent.com/strapi/documentation/main/docusaurus/docs/cms/templates.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Templates

A template is a full Strapi application folder (all the files and folders of a typical Strapi application) used as the starting point of a new project.

```bash
npx create-strapi@latest my-project --template <template-name-or-url>
# or
yarn create strapi my-project --template <template-name-or-url>
```

Related flags: `--template-path` (a subfolder inside the template repo) and `--template-branch` (a branch other than the default).

## Notes
- The value can be a Strapi-maintained template name (for example `website`), a GitHub shorthand such as `strapi/strapi` (optionally with a sub path), or a full repository URL.
- A URL of the form `https://github.com/strapi/strapi/tree/branch/sub/path` does not work with branch names that include a `/`; pass `--template-branch` and `--template-path` explicitly instead.
- Any Strapi 5 application folder can serve as a template. Other install options: `computing-software.web-development.strapi.cli-install-options`.

## Checked

2026-11-04: checked against the Strapi docs page Templates (templates). Confirmed: both create commands, `--template`, `--template-path`, `--template-branch`, the accepted value forms and the branch-with-slash warning, creating a template from any application. Removed: 'meant for the first run' and the 'check the template Strapi version' advice, neither of which the page states.

Method: documentation only; no commands were run.
