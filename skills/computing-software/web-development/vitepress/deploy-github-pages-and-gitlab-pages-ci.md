---
id: computing-software.web-development.vitepress.deploy-github-pages-and-gitlab-pages-ci
name: deploy-github-pages-and-gitlab-pages-ci
category: computing-software
field: web-development
product: vitepress
tags: [vitepress, deploy, github-pages, gitlab-pages, github-actions, deploy-yml, upload-pages-artifact, gitlab-ci, outdir]
level: practitioner
status: docs-checked
description: "Deploy VitePress with a GitHub Actions Pages workflow or a .gitlab-ci.yml pages job, including base, cache, and fetch-depth settings."
sources:
  - https://raw.githubusercontent.com/vuejs/vitepress/main/docs/en/guide/deploy.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Assumptions used by the official guides: site in `docs`, default output `.vitepress/dist`, scripts `docs:build` = `vitepress build docs` and `docs:preview` = `vitepress preview docs`.

**GitHub Pages.** Create `.github/workflows/deploy.yml`. Key elements of the documented workflow:

- Triggers: `push` to `main` (change to `master` if needed) and `workflow_dispatch`.
- `permissions`: `contents: read`, `pages: write`, `id-token: write`.
- `concurrency` group `pages` with `cancel-in-progress: false`, so production deployments finish.
- Build job: `actions/checkout@v5` with `fetch-depth: 0` (only needed if `lastUpdated` is on), `actions/setup-node@v6` (Node 24, `cache: npm`), an `actions/cache@v4` step on `docs/.vitepress/cache` keyed on `hashFiles` of `docs/**` and the lockfiles, `actions/configure-pages@v4`, `npm ci`, `npm run docs:build`, then `actions/upload-pages-artifact@v3` with `path: docs/.vitepress/dist`.
- Deploy job: `needs: build`, environment `github-pages`, step `actions/deploy-pages@v4`.

Then in repository Settings > Pages choose "GitHub Actions" as the source. Site URL is `https://<username>.github.io/[repository]/` or your custom domain. Set `base` to `/repo/` when deploying to `user.github.io/repo/`.

**GitLab Pages.** Set `outDir: '../public'` in the config; set `base: '/<repository>/'` only for `https://<username>.gitlab.io/<repository>/` (not needed for custom domains, user/group pages, or "Use unique domain"). Then `.gitlab-ci.yml`:

```yaml
image: node:24
pages:
  cache:
    paths: [node_modules/]
  script:
    - npm install
    - npm run docs:build
  artifacts:
    paths: [public]
  only: [main]
```

On small images like alpine, install git first if `lastUpdated` is enabled.

## Checked

2026-11-04. Confirmed against the VitePress deploy guide (shared assumptions, GitHub Pages workflow and settings, GitLab Pages config and .gitlab-ci.yml, Setting a Public Base Path). Removed: the Verify step.

Method: documentation only; no commands were run.
