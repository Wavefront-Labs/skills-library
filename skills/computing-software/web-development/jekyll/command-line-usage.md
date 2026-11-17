---
id: computing-software.web-development.jekyll.command-line-usage
name: command-line-usage
category: computing-software
field: web-development
product: jekyll
tags: [jekyll-cli, jekyll-new, jekyll-build, jekyll-serve, jekyll-clean, jekyll-doctor]
level: intro
status: docs-checked
description: "Use the jekyll executable: new, build, serve, clean, doctor, new-theme and help, with the command-argument-option structure."
sources:
  - https://raw.githubusercontent.com/jekyll/jekyll/master/docs/_docs/usage.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The gem installs a `jekyll` executable. Structure:

```
jekyll command [argument] [option] [argument_to_option]

jekyll new site/ --blank
jekyll serve --config _alternative_config.yml
```

Use `jekyll serve` while developing locally and `jekyll build` to generate the site for production.

Common commands:

- `jekyll new PATH`: new site with the default gem-based theme; directories are created as needed.
- `jekyll new PATH --blank`: blank site scaffold.
- `jekyll build` or `jekyll b`: one-off build to `./_site` by default.
- `jekyll serve` or `jekyll s`: rebuild on every source change and serve locally.
- `jekyll clean`: remove the destination folder, metadata file, Sass cache and Jekyll cache.
- `jekyll help [command]`: show help, e.g. `jekyll help build`.
- `jekyll new-theme`: scaffold a theme.
- `jekyll doctor`: print deprecation or configuration issues.

Full flag lists are under "Build Command Options" in the configuration options page. To change default build behaviour, use `_config.yml`.

## Checked

2026-11-04. Confirmed against the Jekyll command line usage doc: command structure, both examples, the serve-versus-build advice, and each listed command with its description (including the `b` and `s` shortcuts). Nothing removed.

Method: documentation only; no commands were run.
