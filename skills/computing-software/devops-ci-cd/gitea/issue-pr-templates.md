---
id: computing-software.devops-ci-cd.gitea.issue-pr-templates
name: issue-pr-templates
category: computing-software
field: devops-ci-cd
product: gitea
tags: [gitea-issue-template, gitea, issue-forms-yaml, issue-config-yaml, pull-request-template, blank-issues-enabled, contact-links, form-field-visible]
level: advanced
status: docs-checked
description: "Add Gitea issue and pull request templates as markdown or YAML forms, with file locations, front matter, field types and validations, and config.yaml contact links."
sources: ["https://gitea.com/gitea/docs/src/branch/main/docs/usage/issues-prs/issue-pull-request-templates.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Gitea issue and PR templates

Templates must be on the repository's **default branch**. Global templates are not possible. `?title=...&body=...` on the New Issue URL overrides the template.

## Locations
- Single issue template: `ISSUE_TEMPLATE.md|.yaml|.yml` (upper or lower case) in the root, `.gitea/` or `.github/`.
- Multiple issue templates: files inside a directory named `ISSUE_TEMPLATE` or `issue_template` in the root, `.gitea/`, `.github/` or `.gitlab/`.
- Issue config: `.gitea/ISSUE_TEMPLATE/config.yaml|yml` (also lower case dir, and `.github/`).
- PR template: `PULL_REQUEST_TEMPLATE.md|.yaml|.yml` (either case) in the root, `.gitea/` or `.github/`.

## Markdown template
Front matter keys: `name`, `about`, `title` (prefix), `ref` (e.g. `main`), `assignees`, `projects`, `labels`; the body below becomes the issue body.

## YAML form
Top-level `name`, `about`, `title`, then `body:` a list of elements with `type`, optional `id`, `attributes`, `validations`, `visible`.
- `markdown` (`value`): extra context, not submitted; `visible` default `[form]`.
- `textarea`: `label` (required), `hide_label`, `description`, `placeholder`, `value`, `render` (formats the text as a code block in a known language; the area then will not expand for attachments). Allows file attachments.
- `input`: same plus validations `required`, `is_number`, `regex`.
- `dropdown`: `label`, `multiple`, `list`, `options` (required, non-empty, distinct).
- `checkboxes`: `options` with `label`, `required`, `visible` per item.
`visible` accepts `form` and `content` (shown in the form, in the created issue, or both); default `[form, content]` except for `markdown`. `validations.required: true` blocks submission until filled.

## config.yaml
```yaml
blank_issues_enabled: true
contact_links:
  - name: Gitea
    url: https://gitea.com
    about: Visit the Gitea Website
```
`blank_issues_enabled: false` forces users to pick a template (default `true`). Each contact link needs `name`, `url` and `about`.

## Checked
2026-11-03. Commands, flags, settings, numbers and behaviour were compared line by line with the Gitea docs source page named in `sources` (read in full from the docs repository raw file). Nothing else removed; no unconfirmed claim remained.
Method: documentation only; no commands were run.
