---
id: computing-software.web-development.vitepress.home-page-hero-and-features
name: home-page-hero-and-features
category: computing-software
field: web-development
product: vitepress
tags: [vitepress, home-page, hero, features, landing-page, hero-actions, home-hero-name-color, themeable-image]
level: practitioner
status: docs-checked
description: "Configure layout: home with hero (name, text, tagline, image, actions), features list, gradient name colour and extra Markdown."
sources:
  - https://raw.githubusercontent.com/vuejs/vitepress/main/docs/en/reference/default-theme-home-page.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
```yaml
---
layout: home
hero:
  name: VitePress
  text: Vite & Vue powered static site generator.
  tagline: Lorem ipsum...
  image:
    src: /logo.png
    alt: VitePress
  actions:
    - theme: brand
      text: Get Started
      link: /guide/what-is-vitepress
    - theme: alt
      text: View on GitHub
      link: https://github.com/vuejs/vitepress
features:
  - icon: 🛠️
    title: Simple and minimal, always
    details: Lorem ipsum...
  - icon: { src: /cool-feature-icon.svg }
    title: Another cool feature
    details: Lorem ipsum...
---
```

**Hero fields:** `name` (short, brand coloured), `text` (the `h1`), `tagline`, `image` (a path, `{ src, alt }` or `{ light, dark, alt }`), `actions` (`theme: brand | alt`, `text`, `link`, optional `target` and `rel`).

**Features:** each has `icon` (emoji, or an image given as `{ src, alt?, width?, height }` or a `{ light, dark, ... }` pair; for image icons give width and height; the type marks `height` required), `title`, `details`, and optional `link`, `linkText`, `rel`, `target`.

**Name colour.** The `name` uses `--vp-c-brand-1`. Override with `--vp-home-hero-name-color`, and make a gradient by combining `--vp-home-hero-name-color: transparent` with `--vp-home-hero-name-background: -webkit-linear-gradient(120deg, #bd34fe, #41d1ff)`.

**Extra content.** Any Markdown after the closing `---` is rendered on the home page. Older VitePress did not auto-style it; add `markdownStyles: false` to the frontmatter to revert to that behaviour.

Slots for injecting hero content are in the layout-slots skill.

Verify: the home page shows the hero, feature cards and trailing Markdown.

## Checked

2026-11-08. Read the VitePress docs source page default-theme-home-page. Confirmed the Hero and Feature interfaces, ThemeableImage forms, action theme default brand, the name colour variables, and the markdownStyles note. Reworded the image-icon size rule to match the prose and type.

Method: docs-only read of cited pages, 2026-11-08
