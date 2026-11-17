---
id: computing-software.web-development.jekyll.directory-structure
name: directory-structure
category: computing-software
field: web-development
product: jekyll
tags: [directory-structure, underscore-folders, site-layout, include-exclude, gitignore]
level: intro
status: docs-checked
description: "Know what each Jekyll folder does (_posts, _drafts, _layouts, _includes, _data, _sass, _site) and which paths are skipped or copied verbatim into the output."
sources:
  - https://raw.githubusercontent.com/jekyll/jekyll/master/docs/_docs/structure.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
A basic site holds `_config.yml`, `_data`, `_drafts`, `_includes`, `_layouts`, `_posts`, `_sass`, `_site`, `.jekyll-cache`, `.jekyll-metadata` and an `index.html` (or `index.md` with front matter).

- `_config.yml`: configuration.
- `_drafts`: unpublished posts, named `title.MARKUP` (no date).
- `_includes`: partials pulled in with the include tag.
- `_layouts`: templates that wrap content; `{{ content }}` injects the page.
- `_posts`: named `YEAR-MONTH-DAY-title.MARKUP`; date and markup come from the file name.
- `_data`: `.yml`, `.yaml`, `.json`, `.csv`, `.tsv` files, exposed as `site.data.<name>`.
- `_sass`: partials imported into a `main.scss`.
- `_site`: generated output; add to `.gitignore`.
- `.jekyll-cache`: cache of generated pages; add to `.gitignore`.
- `.jekyll-metadata`: created only with incremental regeneration; add to `.gitignore`.

Sites from `jekyll new` use a gem-based theme (minima), so `_layouts`, `_includes` and `_sass` live in the theme gem; `bundle info minima` shows where.

Any `.html`, `.markdown`, `.md` or `.textile` file with front matter is transformed. Every other file or folder (css, images, favicon.ico) is copied verbatim.

Anything starting with `.`, `_`, `#` or `~` is not copied to the destination unless listed under `include`:

```yaml
include:
 - _pages
 - .htaccess
```

## Checked

2026-11-04. Confirmed against the Jekyll directory structure page: the example tree, the description of each folder and file, the gem-based theme note with minima and `bundle info minima`, transformed versus verbatim files, and the `.`, `_`, `#`, `~` rule with the `include` example. Nothing removed.

Method: documentation only; no commands were run.
