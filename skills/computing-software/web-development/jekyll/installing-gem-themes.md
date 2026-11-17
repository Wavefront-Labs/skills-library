---
id: computing-software.web-development.jekyll.installing-gem-themes
name: installing-gem-themes
category: computing-software
field: web-development
product: jekyll
tags: [gem-based-themes, minima, theme-install, bundle-update, remote-theme]
level: intro
status: docs-checked
description: "Install and update a gem-based Jekyll theme: Gemfile entry, bundle install, theme key in config, and how minima's files stay hidden in the gem."
sources:
  - https://raw.githubusercontent.com/jekyll/jekyll/master/docs/_docs/themes.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`jekyll new <PATH>` installs a site using the gem-based theme Minima. With gem-based themes, `assets`, `_data`, `_layouts`, `_includes` and `_sass` are stored in the gem but still read during the build. A Minima site shows only `Gemfile`, `Gemfile.lock`, `_config.yml`, `_posts`, `about.markdown` and `index.markdown`.

Update with `bundle update` (all gems) or `bundle update <THEME>` (e.g. `minima`) to pull new theme files automatically.

Install another gem theme:

1. Add it to `Gemfile` (replace the `minima` line if you started with `jekyll new`):

   ```ruby
   gem "jekyll-theme-minimal"
   ```

2. `bundle install`
3. Activate it in `_config.yml`:

   ```yaml
   theme: jekyll-theme-minimal
   ```

4. Build with `bundle exec jekyll serve`.

You can list several themes in the Gemfile, but only one can be selected in `_config.yml`. Not all themes use `jekyll-theme` in their name when searching RubyGems.

GitHub Pages supports only some gem-based themes, plus any theme hosted on GitHub through the `remote_theme` configuration, used as if it were a gem theme.

## Checked

2026-11-04. Confirmed against the Jekyll Themes page: Minima file list, bundle update, install steps, one theme in config and the GitHub Pages remote_theme note. Nothing removed.

Method: documentation only; no commands were run.
