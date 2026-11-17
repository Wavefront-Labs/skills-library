---
id: computing-software.web-development.storybook.publish-storybook
name: publish-storybook
category: computing-software
field: web-development
product: storybook
tags: [publish, static-build, storybook-static, chromatic-publish, deploy]
level: practitioner
status: docs-checked
description: "Build a static Storybook, preview it locally and publish it to Chromatic or any static host."
sources:
  - https://storybook.js.org/docs/sharing/publish-storybook
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Publish Storybook

Goal: share a deployable Storybook.

Build:

```shell
storybook build
# Angular projects often use the Angular builder instead
```
This produces a static web application that any web server can serve; the page also gives a command to preview it locally and links the CLI options for extra flags.

Notes:
- Large projects can slim the production bundle with the `test` option in main config's `build` and the `--test` flag.
- Older browsers: `--preview-only` skips building the manager and builds only the preview iframe. `/index.html` then returns 404; start from `/iframe.html?navigator=true`, which renders a basic HTML-only sidebar. It applies to `dev` and `build`.
- Stencil with lazy-loaded components (web-components renderer): enable import injection (`extras.enableImportInjection: true` in Stencil 4.26+, otherwise `experimentalImportInjection: true`).

Chromatic hosting:

```shell
npm install --save-dev chromatic
npx chromatic --project-token=<your-project-token>
```
The token comes from signing up to Chromatic. The page also shows a GitHub Actions workflow that publishes on push (the project token is kept as a secret) so PRs get a link in their checks, and Chromatic gives component history and versioning down to the commit.

Other hosts (GitHub Pages, Netlify, S3) work for the static build, but Composition, embedding, history, versioning and assets may need tighter integration; the page describes Component Publishing Protocol levels 0 and 1, with Chromatic at level 1. For public Storybooks, add a description or a noindex meta tag in `manager-head.html`.

## Checked

Method: 2026-11-08 read docs/sharing/publish-storybook.mdx from the Storybook repo. Removed unsupported claims (`storybook-static`/`-o`/http-server details, subpath relative-asset rule, "Storybook per branch"), corrected the preview-only URL to `/iframe.html?navigator=true`, and removed a Verify step. Shell snippets for build and preview were not read.
