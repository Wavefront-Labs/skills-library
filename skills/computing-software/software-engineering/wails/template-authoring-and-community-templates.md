---
id: computing-software.software-engineering.wails.template-authoring-and-community-templates
name: template-authoring-and-community-templates
category: computing-software
field: software-engineering
product: wails
tags: [wails, go, templates, wails-init, community, security, publishing]
level: practitioner
status: docs-checked
description: "Create and publish a Wails project template with wails generate template, and use third-party templates safely with wails init -t."
sources: [https://wails.io/docs/guides/templates, https://wails.io/docs/community/templates]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Authoring, publishing and using Wails templates

Goal: build your own template, or consume a community one without running untrusted code blindly.

## Create a template

`wails generate template -name mytemplate` creates a directory with: `NEXTSTEPS.md` (how to finish the template), `README.md`, `app.tmpl.go`, `main.tmpl.go`, `go.mod.tmpl`, `wails.tmpl.json`, `template.json` (metadata) and `frontend/` (default assets in `frontend/dist`). Follow `NEXTSTEPS.md` first.

## From an existing frontend project

Example (Vue 3): `npm install -g @vue/cli`, `vue create vue3-base` (choose Default Vue 3), then
```shell
wails generate template -name wails-vue3-template -frontend .\vue3-base\
```
This extracts the base files, moves the project into `frontend`, and renames `package.json` and `package-lock.json` to `.tmpl.json` variants. Customise per `NEXTSTEPS.md`, then test: `wails init -n my-vue3-project -t .\wails-vue3-template\`, `cd my-vue3-project`, `wails build`, run `.\build\bin\my-vue3-project.exe`.

## Publish

Push to GitHub after removing unwanted files (e.g. `.git` from the frontend dir) and completing `template.json`, especially `helpurl`. Then open a PR on the Community Templates page and announce it on the Template Announcement discussion (wailsapp/wails discussion 825).

## Use a community template

```bash
wails init -n "Your Project Name" -t https://github.com/misitebao/wails-template-vue
```
Append `@version` to use a tag; without a suffix the main branch is used. The community list is grouped by Vue, Angular, React, Svelte, Solid, Elm, HTMX, vanilla JS and Lit.

## Security

The Wails project does not maintain or vouch for third-party templates. A template is code: `wails build` and `wails dev` run the `frontend:install`, `frontend:build`, `frontend:dev`, `frontend:dev:install`, `frontend:dev:build` and `frontend:dev:watcher` commands from `wails.json` without asking, and package.json scripts also run, all with your user's permissions. Review `wails.json`, `package.json` and referenced scripts before the first build; `wails init` prints the commands found in `wails.json` for remote templates.

## Checked

2026-11-07. Read the whole Templates guide (website/docs/guides/templates.mdx: default generated files and overview table, the Vue 3 example including the renamed package.tmpl.json files and the test commands, the publishing checklist with helpurl and discussion 825), the whole Community Templates page (website/docs/community/templates.mdx: wails init -t usage, @version suffix and main-branch default, the not-maintained warning, the "templates are code" security box with the six frontend commands, the framework section headings) and the init / Remote Templates section of the CLI reference (website/docs/reference/cli.mdx), which repeats the same security box. Individual template repositories on the community list were not opened. No claims were trimmed.

Method: documentation only; no commands were run.
