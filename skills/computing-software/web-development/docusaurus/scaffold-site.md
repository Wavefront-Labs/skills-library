---
id: computing-software.web-development.docusaurus.scaffold-site
name: scaffold-site
category: computing-software
field: web-development
product: docusaurus
tags: [create-docusaurus, scaffold, classic-template, typescript-template, installation]
level: intro
status: docs-checked
description: "Create a new Docusaurus site with create-docusaurus: the classic template, the TypeScript variant, alternative init commands, and checking the installed version."
sources:
  - https://raw.githubusercontent.com/facebook/docusaurus/main/website/docs/installation.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Docusaurus is a set of npm packages. Scaffold a site with the `create-docusaurus` CLI, anywhere in an empty or existing repository; it creates a new directory.

```sh
npx create-docusaurus@latest my-website classic
```

The `classic` template is recommended. It contains `@docusaurus/preset-classic`, which includes docs, a blog, custom pages and a CSS framework with dark mode.

TypeScript variant:

```sh
npx create-docusaurus@latest my-website classic --typescript
```

Alternative: `npm init docusaurus`. Run `npx create-docusaurus@latest --help` for all flags.

Requirement: a minimum Node.js version (see the installation page; check yours with `node -v`).

Start the dev server with `npm run start` (opens `http://localhost:3000`) and build with `npm run build` into `/build`.

Updating: change the version in `package.json` (all `@docusaurus/`-namespaced packages must use the same version), run your package manager's install, then check with:

```sh
npx docusaurus --version
```

Unreleased features are available through the `@canary` npm dist tag.

## Checked

2026-11-04: read the Docusaurus installation page in full. Confirmed the create-docusaurus commands, classic template contents, the TypeScript variant, npm init docusaurus, the version update steps and the canary tag. Nothing removed.

Method: documentation only; no commands were run.
