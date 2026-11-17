---
id: computing-software.web-development.docusaurus.deploy-github-pages
name: deploy-github-pages
category: computing-software
field: web-development
product: docusaurus
tags: [github-pages, docusaurus-deploy, github-actions, gh-pages, nojekyll]
level: practitioner
status: docs-checked
description: "Deploy a Docusaurus site to GitHub Pages: config fields, docusaurus deploy environment variables, .nojekyll, custom domain CNAME, and a Pages Actions workflow."
sources:
  - https://raw.githubusercontent.com/facebook/docusaurus/main/website/docs/deployment/github-pages.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Config fields (env counterparts `ORGANIZATION_NAME`, `PROJECT_NAME`, `DEPLOYMENT_BRANCH` take priority):

```js title="docusaurus.config.js"
export default {
  url: 'https://my-org.github.io',
  baseUrl: '/',
  organizationName: 'my-org',
  projectName: 'my-org.github.io',
  trailingSlash: false,
};
```

`deploymentBranch` defaults to `gh-pages` unless `projectName` ends in `.github.io`, then set it explicitly. Set `trailingSlash` to true or false, not undefined, because GitHub Pages adds one. Project repos serve at `https://my-org.github.io/my-project/`, so set `baseUrl` to `/my-project/`.

Add an empty `.nojekyll` file to `static`, or Jekyll discards files starting with `_`. For a custom domain, put a `CNAME` file in `static` and move `baseUrl` back to `/`.

Run `docusaurus deploy` (clone, build, commit to the deployment branch):

```bash
GIT_USER=<GITHUB_USERNAME> yarn deploy
```

Environment: `USE_SSH=true` (inferred when the source repo URL is SSH), `GIT_USER` (needs push access), `GIT_PASS` (personal access token), `CURRENT_BRANCH`, `GIT_USER_NAME`, `GIT_USER_EMAIL`, and `GITHUB_HOST`/`GITHUB_PORT` for Enterprise. GitHub needs a personal access token, not a password.

Actions, same repo: set Pages publishing to a custom workflow. A `build` job runs `npm ci`, `npm run build`, then `actions/upload-pages-artifact` with `path: build`. A `deploy` job needing it has `permissions: pages: write` and `id-token: write`, environment `github-pages`, and runs `actions/deploy-pages`. Use a separate workflow for PRs that only builds.

## Checked

2026-11-04: read the Docusaurus GitHub Pages deployment page in full. Confirmed config fields and environment counterparts, deploymentBranch default, trailingSlash advice, .nojekyll, CNAME, the deploy environment variables, GIT_USER usage, token note, and the same-repo Actions workflow shape. Nothing removed.

Method: documentation only; no commands were run.
