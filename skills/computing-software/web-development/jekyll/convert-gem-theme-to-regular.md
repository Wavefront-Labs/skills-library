---
id: computing-software.web-development.jekyll.convert-gem-theme-to-regular
name: convert-gem-theme-to-regular
category: computing-software
field: web-development
product: jekyll
tags: [theme-eject, gem-theme-conversion, gemspec-dependencies, plugin-gems, github-pages-theme]
level: advanced
status: docs-checked
description: "Eject a gem-based Jekyll theme into your site: copy its files, carry over its runtime plugin dependencies, then remove the theme gem and config entry."
sources:
  - https://raw.githubusercontent.com/jekyll/jekyll/master/docs/_docs/themes.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
To get rid of the gem and keep all theme files in your site:

1. Copy the files from the theme gem directory (found via `bundle info --path <theme>`) into your site directory.
2. Find the plugins the theme used: its gemspec lists them as runtime dependencies, e.g. for Minima:

   ```ruby
   spec.add_runtime_dependency "jekyll-feed", "~> 0.12"
   spec.add_runtime_dependency "jekyll-seo-tag", "~> 2.6"
   ```

3. Tell Jekyll about them, either in both `Gemfile` and `_config.yml`:

   ```ruby
   gem "jekyll-feed", "~> 0.12"
   gem "jekyll-seo-tag", "~> 2.6"
   ```

   ```yaml
   plugins:
     - jekyll-feed
     - jekyll-seo-tag
   ```

   or in the Gemfile only, in the plugins group:

   ```ruby
   group :jekyll_plugins do
     gem "jekyll-feed", "~> 0.12"
     gem "jekyll-seo-tag", "~> 2.6"
   end
   ```

4. Run `bundle update`.
5. Remove the theme: delete its `gem` line from `Gemfile` (e.g. `gem "minima", "~> 2.5"`) and `theme: minima` from `_config.yml`.

On GitHub Pages update only `_config.yml`, because it does not load plugins via Bundler.

## Checked

2026-11-04. Confirmed against the Jekyll Themes page, section on converting gem-based themes: copying files, gemspec runtime dependencies, the two ways to list plugins, bundle update, removal and the GitHub Pages note. Nothing removed.

Method: documentation only; no commands were run.
