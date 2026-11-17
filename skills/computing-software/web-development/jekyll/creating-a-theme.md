---
id: computing-software.web-development.jekyll.creating-a-theme
name: creating-a-theme
category: computing-software
field: web-development
product: jekyll
tags: [new-theme, theme-authoring, theme-assets, theme-sass, theme-readme, theme-screenshot]
level: advanced
status: docs-checked
description: "Build a Jekyll gem theme: jekyll new-theme scaffold, layouts and includes precedence, assets with front matter, Sass import, README, screenshot and preview."
sources:
  - https://raw.githubusercontent.com/jekyll/jekyll/master/docs/_docs/themes.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Scaffold with `jekyll new-theme jekyll-theme-awesome`. It creates `_layouts` (page, post, default), `_includes`, `_sass`, `Gemfile`, a gemspec, `README.md`, `LICENSE.txt` and a git repo with `.gitignore`. Add templates, then complete the gemspec and README.

- Layouts and includes work as in any site. For `layout: page`, Jekyll first checks the site's `_layouts`, then the theme's.
- Assets: files in `/assets` are copied to the user's site unless it has the same relative path. With front matter they are rendered, without it just copied. Ship a default `/assets/styles.scss` that layouts reference as `/assets/styles.css`.
- Stylesheets go in the theme's `_sass`, e.g. `_sass/jekyll-theme-awesome.scss`, and users pull them in:

  ```css
  @import "{{ site.theme }}";
  ```

- Document it in `/README.md`: layouts, includes, any config additions.
- Add a screenshot at `/screenshot.png` in the repository.
- Preview by adding dummy content such as `/index.html` and `/page.html`, then run `jekyll build` or `jekyll serve`. Add `/_site` to the theme's `.gitignore`.

## Checked

2026-11-04. Confirmed against the Jekyll Themes page, section on creating a gem-based theme: new-theme scaffold, layouts precedence, assets, Sass import, README, screenshot and preview. Nothing removed.

Method: documentation only; no commands were run.
