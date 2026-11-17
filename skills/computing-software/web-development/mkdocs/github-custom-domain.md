---
id: computing-software.web-development.mkdocs.github-custom-domain
name: github-custom-domain
category: computing-software
field: web-development
product: mkdocs
tags: [custom-domain, cname, github-pages, gh-deploy]
level: practitioner
status: docs-checked
description: "Keep a GitHub Pages custom domain through MkDocs gh-deploy by storing a CNAME file in docs_dir so it is not wiped on deploy."
sources:
  - https://raw.githubusercontent.com/mkdocs/mkdocs/master/docs/user-guide/deploying-your-docs.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Besides GitHub's own custom-domain steps, MkDocs needs a `CNAME` file at the root of your `docs_dir`. It contains a single bare domain or subdomain on one line.

```text
docs/
    CNAME
    index.md
```

Why: `gh-deploy` rebuilds the pages branch every time. If you set the domain in GitHub's web interface (Settings / Custom Domain), GitHub creates `CNAME` on the pages branch, and the next deploy removes it. Copy that file into `docs_dir`; MkDocs then copies it into the built site and pushes it each run.

Related: the `404.html` is used on GitHub only with a custom domain (see `404-page`).

If the domain still fails, see GitHub's troubleshooting guide for custom domains.

## Checked

2026-11-04. Confirmed against Deploying your docs (Custom Domains, 404 Pages): `CNAME` at the root of `docs_dir`, one bare domain on one line, GitHub web interface behaviour, copy into `docs_dir`, troubleshooting link, and the 404 note. Removed: a generic verify line.

Method: documentation only; no commands were run.
