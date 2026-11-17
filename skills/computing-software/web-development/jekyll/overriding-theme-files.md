---
id: computing-software.web-development.jekyll.overriding-theme-files
name: overriding-theme-files
category: computing-software
field: web-development
product: jekyll
tags: [theme-override, bundle-info-path, override-layouts, override-sass, theme-updates]
level: practitioner
status: docs-checked
description: "Override Jekyll theme layouts, includes, data, assets and Sass by same-named files in your site; find the theme gem path and mind the stylesheet and update trade-offs."
sources:
  - https://raw.githubusercontent.com/jekyll/jekyll/master/docs/_docs/themes.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Jekyll looks in your site first, then the theme, for files in `/assets`, `/_data`, `/_layouts`, `/_includes` and `/_sass`. To override one, create a file of the same name in your site, either by copying the theme's file or writing it from scratch. For a theme `page` layout, create `_layouts/page.html`; to override Minima's footer, add `_includes/footer.html`.

Find the theme's files:

```sh
bundle info --path minima
open $(bundle info --path minima)      # macOS
xdg-open $(bundle info --path minima)  # Linux
```

On Windows run `bundle info --path minima`, then open the path in `explorer` with `\` separators.

Minima's gem holds `_includes` (disqus_comments, footer, google-analytics, head, header and icon files), `_layouts` (default, home, page, post), `_sass/minima/` partials plus `_sass/minima.scss`, and `assets/main.scss`.

To change any stylesheet you must also copy the theme's main Sass file (`_sass/minima.scss` for Minima) into your site's `_sass`.

Copying theme files means you stop receiving updates for those files. An alternative that keeps stylesheet updates is adding higher-specificity CSS selectors in your own, separately named CSS files.

Check the theme's own documentation for which files you can override.

## Checked

2026-11-04. Confirmed against the Jekyll Themes page, overriding section: lookup folders, bundle info --path, open commands, Minima file list, the Sass copy rule and update trade-off. Nothing removed.

Method: documentation only; no commands were run.
