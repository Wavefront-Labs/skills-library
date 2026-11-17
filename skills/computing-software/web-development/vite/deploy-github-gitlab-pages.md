---
id: computing-software.web-development.vite.deploy-github-gitlab-pages
name: deploy-github-gitlab-pages
category: computing-software
field: web-development
product: vite
tags: [github-pages, gitlab-pages, base-repo-path, pages-workflow]
level: practitioner
status: docs-checked
description: "Deploy a Vite build to GitHub Pages and GitLab Pages: set base to the repo path, enable the Actions source, and copy dist into public for GitLab CI."
sources:
  - https://raw.githubusercontent.com/vitejs/vite/main/docs/guide/static-deploy.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Base rule for both hosts:
- Site at the user/group root (`https://<USERNAME>.github.io/`, a custom domain, or `https://<USERNAME or GROUP>.gitlab.io/`): `base` is `'/'` (the default; may be omitted).
- Site under a repo path (`.../<REPO>/`): set `base` to `'/<REPO>/'`.

GitHub Pages:
1. Set `base` in `vite.config.js`.
2. In Settings, Pages, Build and deployment, choose Source: GitHub Actions (Vite needs a build step).
3. Add `.github/workflows/deploy.yml` that installs, builds and deploys on pushes to `main`. The docs include a sample workflow file.

GitLab Pages: add `.gitlab-ci.yml` with a `pages` job (image `node:lts`) whose script runs:

```yaml
script:
  - npm install
  - npm run build
  - cp -a dist/. public/
artifacts:
  paths:
    - public
rules:
  - if: $CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH
```

## Checked

Date: 2026-11-07. Read static-deploy.md in full (GitHub Pages and GitLab Pages sections). The sample workflow is pulled in by an include (`static-deploy-github-pages.yaml`) that was NOT opened; the skill only repeats the page's prose about it (installs, builds, deploys on pushes to `main`). The `base` rules, Settings, Pages, Build and deployment, Source: GitHub Actions path and the `.gitlab-ci.yml` fragment (the skill's script/artifacts/rules lines are a subset of the page's) matched.

Method: documentation only; no commands were run.
