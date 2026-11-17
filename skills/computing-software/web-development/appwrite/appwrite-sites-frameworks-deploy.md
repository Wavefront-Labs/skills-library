---
id: computing-software.web-development.appwrite.appwrite-sites-frameworks-deploy
name: appwrite-sites-frameworks-deploy
category: computing-software
field: web-development
product: appwrite
tags: [appwrite, sites, frameworks, ssr, static, deployment]
level: practitioner
status: docs-checked
description: "Choose a supported framework for Appwrite Sites, know which render SSR or static, and set manual build settings for others."
sources:
  - https://github.com/appwrite/website/blob/main/src/routes/docs/products/sites/frameworks/+page.markdoc
  - https://github.com/appwrite/website/blob/main/src/routes/docs/products/sites/quick-start/+page.markdoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: host a web app on Appwrite Sites.

Supported with SSR or static: Next.js, Nuxt, SvelteKit, Angular, Astro, Remix and TanStack Start. Static only: Flutter Web, React Native and Other JavaScript. The quick start has a page per framework.

Appwrite detects the framework from your package dependencies and config files, picks SSR or static, and sets the install command, build command and output directory. For an unsupported framework choose the "Other" option and set those three yourself; most JavaScript frameworks can produce a static build.

Create the site (quick start): Console > Sites > Create site > Connect Git repository, select the repository, optionally set a name and site ID, verify the framework, confirm the install command, build command and output directory, and add any environment variables. The site is created and a build starts; use the site domain to open the deployment.

## Checked

Date: 2026-11-07. Read in full on the appwrite/website docs source (Markdoc): products/sites/frameworks, products/sites/quick-start. Code tabs for non-JavaScript SDKs were collapsed when read and Markdoc partials (shared include files) were not opened; all prose and the JavaScript examples were read. Corrections: Static list corrected to React Native (not "React Native web"); removed "upload manually", the CLI appwrite init/push sites line, the deployment status list, the output-directory gotcha and the invented Verify; create steps now follow the quick start.

Method: documentation only; no commands were run.
