---
id: computing-software.web-development.mkdocs.repo-link-edit-uri
name: repo-link-edit-uri
category: computing-software
field: web-development
product: mkdocs
tags: [repo-url, edit-uri, repo-name, edit-links]
level: practitioner
status: docs-checked
description: "Add repository and edit-this-page links in MkDocs with repo_url, repo_name and edit_uri, including the edit versus blob default for GitHub and GitLab."
sources:
  - https://raw.githubusercontent.com/mkdocs/mkdocs/master/docs/user-guide/configuration.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
```yaml
repo_url: https://example.com/project/repo
edit_uri: blob/main/docs/
```

MkDocs joins `repo_url`, `edit_uri` and the page path: `foo/bar.md` links to `https://example.com/project/repo/blob/main/docs/foo/bar.md`. `edit_uri` may also be an absolute URL, or use `?query` / `#fragment` forms.

Defaults:
- `repo_name`: GitHub, Bitbucket or GitLab if the URL matches; else the hostname.
- `edit_uri` on GitHub/GitLab: `edit/master/docs/`; Bitbucket: `src/default/docs/`.
- If `repo_url` is unset, `edit_uri` is ignored.
- Empty string `edit_uri: ''` removes the edit link.

Gotcha: the default `edit/...` path opens the online editor and sends anonymous users to a login page. Use the `blob/master/docs/` path for a read-only anonymous view.

Whether links display depends on the theme.

## Checked

2026-11-04. Confirmed against the MkDocs configuration guide (repo_url, repo_name, edit_uri): concatenation, absolute URL form, query and fragment forms, the GitHub, GitLab and Bitbucket defaults, ignored without `repo_url`, empty string disables, the edit versus blob warning, and theme dependence. Removed: a generic verify line.

Method: documentation only; no commands were run.
