---
id: computing-software.web-development.docusaurus.project-structure
name: project-structure
category: computing-software
field: web-development
product: docusaurus
tags: [project-structure, docs-folder, static-folder, src-pages, sidebars-js]
level: intro
status: docs-checked
description: "What each file and folder in a scaffolded Docusaurus classic site is for: blog, docs, src, static, docusaurus.config.js, sidebars.js and the build output."
sources:
  - https://raw.githubusercontent.com/facebook/docusaurus/main/website/docs/installation.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
A classic-template site `my-website` contains:

- `/blog/` holds blog Markdown files. Delete it if the blog plugin is disabled, or rename it after setting the plugin `path` option.
- `/docs/` holds the docs Markdown files. Same rule: delete if the docs plugin is disabled, or rename via `path`.
- `/src/` holds non-documentation files such as pages and React components. Keeping them under one directory makes linting and processing easier to target.
  - `/src/pages` turns any JSX/TSX/MDX file into a website page.
- `/static/` is copied into the root of the final `build` directory.
- `/docusaurus.config.js` is the site configuration (the equivalent of `siteConfig.js` in Docusaurus v1).
- `/sidebars.js` specifies the order of documents in the docs sidebar.
- `/package.json`: a Docusaurus site is a React app, so install any npm packages you like.

Monorepo: run `npx create-docusaurus` in the monorepo root; the Docusaurus root is a subfolder such as `website`. On hosts like Netlify or Vercel, set the `Base directory` to that folder.

Output of `npm run build` goes to `/build`, deployable to any static host.

## Checked

2026-11-04: read the Docusaurus installation page in full. Confirmed the folder rundown, monorepo advice and build output. Removed the claim that custom.css is the site CSS, which the page does not state (it only lists the file in the tree).

Method: documentation only; no commands were run.
