---
id: computing-software.web-development.jekyll.github-pages-deployment
name: github-pages-deployment
category: computing-software
field: web-development
product: jekyll
tags: [github-pages, user-pages, project-pages, gh-pages-branch, relative-url, baseurl-local]
level: practitioner
status: docs-checked
description: "Host Jekyll on GitHub Pages: user/org vs project page repos and branches, source must be at the root, URL filters for subpaths, and local testing with an empty baseurl."
sources:
  - https://raw.githubusercontent.com/jekyll/jekyll/master/docs/_docs/github-pages.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
GitHub Pages builds your site with Jekyll when you push source files. Files without front matter are treated as static assets, so plain HTML works with no further setup.

User and organisation pages live in a repository named after the account, e.g. `mojombo.github.io`, and are built from the `master` branch. That name is required even with a custom domain.

Project pages live in the project's own repository, with site content in a `gh-pages` branch or a `docs` folder on `master`, and are served under a subpath such as `username.github.io/project` (unless a custom domain is set).

GitHub Pages overrides the "Site Source" configuration, so keep source files in the root directory or the site may not build.

Subpath URLs complicate previews, so use the URL filters:

```liquid
<link href="{{ 'assets/css/style.css' | relative_url }}" rel="stylesheet">
[{{ page.title }}]("{{ page.url | relative_url }}")
```

To test locally in a github-pages environment from `http://localhost:4000`:

```sh
bundle exec jekyll serve --baseurl=""
```

Windows is not officially supported but the `github-pages` gem can be installed there; see the Windows docs. GitHub's own Pages docs cover troubleshooting.

## Checked

2026-11-04. Confirmed against the Jekyll GitHub Pages page: user and project page layout, root-directory warning, URL filters, local serve with empty baseurl and Windows note. Nothing removed.

Method: documentation only; no commands were run.
