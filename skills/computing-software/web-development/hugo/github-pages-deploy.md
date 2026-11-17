---
id: computing-software.web-development.hugo.github-pages-deploy
name: github-pages-deploy
category: computing-software
field: web-development
product: hugo
tags: [github-pages, github-actions, hugo-yaml-workflow, ci-deploy]
level: practitioner
status: docs-checked
description: "Deploy a Hugo site to GitHub Pages with a GitHub Actions workflow: Pages source setting, workflow jobs, build command and image cache dir."
sources:
  - https://raw.githubusercontent.com/gohugoio/hugoDocs/master/content/en/host-and-deploy/deploy-to-github-pages/index.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Prerequisites: a GitHub account, a repository, a local Git repository with a remote, and a site tested with `hugo server`.

1. In the repository, open Settings, then Pages, and set the Source to GitHub Actions. The change applies immediately; there is no Save button.
2. Create `.github/workflows/hugo.yaml`. Adjust tool versions and `TZ`.
3. Set the image cache location in the Hugo config:

```toml
[caches.images]
dir = ':cacheDir/images'
```

4. Commit and push, watch the run under Actions, and when it turns green follow the link under the deploy step.

The documented workflow, named `Build and deploy`:

- Triggers: pushes to `main` and manual `workflow_dispatch`.
- Env vars: `DART_SASS_VERSION`, `GO_VERSION`, `HUGO_VERSION`, `NODE_VERSION`, `TZ`.
- `build` job: checkout, Setup Pages, conditional Go and Node installs, install Dart Sass and Hugo, configure Git, fetch full history, init submodules, install Node dependencies, restore cache, build, save cache, upload `./public` as the artifact.
- `deploy` job: runs after `build` with `actions/deploy-pages@v5`.

Build command: `hugo build --gc --minify`, with `--baseURL` and `--cacheDir` supplied by the workflow. Later pushes rebuild and redeploy automatically. GitHub Pages has three site types: project, user and organization.

## Checked

2026-11-04. Confirmed against the Hugo docs page Deploy to GitHub Pages: the Settings > Pages Source step (no Save button), the `.github/workflows/hugo.yaml` workflow name, triggers, env vars, job steps, `actions/deploy-pages@v5`, the `:cacheDir/images` setting and the `hugo build --gc --minify` command with `--baseURL` and `--cacheDir`. Removed the claim that site types have different naming rules, which the page does not state.

Method: documentation only; no commands were run.
