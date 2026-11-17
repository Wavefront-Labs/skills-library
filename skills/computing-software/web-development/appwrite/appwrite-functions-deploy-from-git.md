---
id: computing-software.web-development.appwrite.appwrite-functions-deploy-from-git
name: appwrite-functions-deploy-from-git
category: computing-software
field: web-development
product: appwrite
tags: [appwrite, functions, git, deployments, ci]
level: practitioner
status: docs-checked
description: "Connect a Git repository so pushes build and activate function deployments, with branch, path and entrypoint filters."
sources:
  - https://github.com/appwrite/website/blob/main/src/routes/docs/products/functions/deploy-from-git/+page.markdoc
  - https://github.com/appwrite/website/blob/main/src/routes/docs/products/functions/deployments/+page.markdoc
  - https://github.com/appwrite/website/blob/main/src/routes/docs/products/functions/functions/+page.markdoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: continuous deployment for a function.

Setup: Git deployment works only for functions connected to Git: create the function with Git, or open Functions > your function > Settings > Configuration > Git settings > Connect Git. Pick the production branch (usually `main`), the root directory and the entry point.

Behaviour from the docs:
- A push to the production branch creates, builds and activates a deployment, which immediately replaces the current active deployment.
- A push to any other branch creates a deployment but does not activate it, so it handles no requests until activated.
- Build triggers: branch filters match branch names and path filters match files changed in a commit or pull request, both using glob patterns. An empty path filter deploys on all file changes; a `!` pattern excludes paths (the page's example is `!docs/**`).
- Silent mode suppresses the comments Appwrite creates on pull requests to your connected branch.

Root directory: the root of the code copied to the executor; in a monorepo set it to the function's subdirectory. To share code between functions, set the root directory to the common monorepo root and use `cd <working directory>` in Build settings before building, or use Git submodules.

Statuses: `waiting`, `processing`, `building`, `ready`, `active`, `failed`. `ready` is built but not activated; `active` serves executions.

Gotchas: changes to Git settings, Build settings and environment variables require a redeploy to take effect. On Appwrite Cloud the build must finish within the plan's maximum build duration (15 minutes on Free, 45 on Pro and Scale). Self-hosting needs extra environment variables to enable Git deployments.

## Checked

2026-11-04. Confirmed against the Appwrite docs pages Deploy from Git, Deployments and Functions: Connect Git path, production-branch and other-branch behaviour, build triggers and glob filters, root directory and shared-code advice, silent mode on pull request comments, statuses, redeploy rule, build duration and self-hosting note. Removed: the claim that Silent mode also disables checks, the "common cause of failed builds in monorepos" gotcha, and the Verify step. Added the deployments and functions pages as sources.
Method: documentation only; no commands were run.
