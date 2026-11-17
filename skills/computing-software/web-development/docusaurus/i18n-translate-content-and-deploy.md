---
id: computing-software.web-development.docusaurus.i18n-translate-content-and-deploy
name: i18n-translate-content-and-deploy
category: computing-software
field: web-development
product: docusaurus
tags: [i18n-content, translated-docs, multi-domain, single-domain, hreflang]
level: practitioner
status: docs-checked
description: "Translate Docusaurus docs, blog and pages by copying Markdown into i18n folders, then deploy locales under one domain or per-locale domains with localeConfigs urls."
sources:
  - https://raw.githubusercontent.com/facebook/docusaurus/main/website/docs/i18n/i18n-tutorial.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Copy Markdown into the locale folder and translate it:

```bash
mkdir -p i18n/fr/docusaurus-plugin-content-docs/current
cp -r docs/. i18n/fr/docusaurus-plugin-content-docs/current
mkdir -p i18n/fr/docusaurus-plugin-content-blog
cp -r blog/. i18n/fr/docusaurus-plugin-content-blog
mkdir -p i18n/fr/docusaurus-plugin-content-pages
cp -r src/pages/. i18n/fr/docusaurus-plugin-content-pages
```

Docs always divide by version: `./docs` maps to the `current` subfolder and `current.json`. Copy only `.md` and `.mdx` for pages; React pages use the JSON translation files.

Use explicit heading IDs in localized sites. A translated heading changes its generated ID (`hello-world` becomes `bonjour-le-monde`) and breaks anchor links.

Single-domain deploy: `npm run build` produces one single-page application per locale (`build` for the default, `build/fr` for French). Localize 404 pages by redirecting `/fr/*` to `/fr/404.html` where the host allows it (Netlify can, GitHub Pages cannot).

Multi-domain deploy: build one locale at a time without the `/fr/` prefix, with one deployment per locale:

```bash
npm run build -- --locale fr
```

Give each locale its own URL, which also emits `hreflang` alternate links and lets the locale dropdown redirect:

```js
i18n: {
  localeConfigs: {
    en: {url: 'https://en.example.com', baseUrl: '/'},
    fr: {url: 'https://fr.example.com', baseUrl: '/'},
  },
},
```

Not possible on GitHub Pages (a single deployment). Hybrid setups (some sub-paths, some subdomains, or subdomains assembled at the CDN) are allowed.

Docusaurus does not mandate how translations are managed; it only needs the files on disk at build time (git or Crowdin are common).

## Checked

2026-11-04: read the Docusaurus i18n tutorial in full. Confirmed the copy commands, current folder rule, md and mdx only for pages, explicit heading ID advice, single-domain and multi-domain builds, localeConfigs url example with hreflang, the 404 redirect note, GitHub Pages limits, hybrid setups and translation management. Nothing removed.

Method: documentation only; no commands were run.
