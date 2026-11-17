---
id: computing-software.web-development.jekyll.exclude-include-keep-files
name: exclude-include-keep-files
category: computing-software
field: web-development
product: jekyll
tags: [exclude, include, keep-files, fnmatch-globs, destination-cleaning]
level: practitioner
status: docs-checked
description: "Control which files Jekyll reads and keeps: exclude and include globs, Jekyll 3 vs 4 behaviour, default exclusions, keep_files and destination cleaning."
sources:
  - https://raw.githubusercontent.com/jekyll/jekyll/master/docs/_data/config_options/global.yml
  - https://raw.githubusercontent.com/jekyll/jekyll/master/docs/_docs/configuration/options.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`exclude` removes directories or files from conversion. Paths are relative to the site source and cannot be outside it. It supports Ruby `File.fnmatch` globs:

```yaml
exclude: ["README.md", "**/README.md"]
```

- Jekyll 3: `exclude` replaces the default exclusion list.
- Jekyll 4: your entries are added to the defaults, and `include` can override default exclusions.

Defaults in a `jekyll new` config: `.sass-cache/`, `.jekyll-cache/`, `gemfiles/`, `Gemfile`, `Gemfile.lock`, `node_modules/`, `vendor/bundle/`, `vendor/cache/`, `vendor/gems/`, `vendor/ruby/`.

`include` forces inclusion, e.g. `.htaccess`, since dotfiles are excluded by default. It also takes fnmatch globs; in Jekyll 4 include entries beat exclude entries.

`keep_files` preserves selected files when the destination is cleaned; paths are relative to `destination`. Use it for files made by another build tool.

The destination is cleaned by default when the site is built, and anything not created by the site is removed. Never point `destination` at an important location; use it as a staging area and copy from there.

```yaml
keep_files: [DIR, FILE]
```

## Checked

2026-11-04. Confirmed against the Jekyll global configuration data and Configuration Options page: exclude and include globs, Jekyll 3 versus 4 behaviour, default exclusions, keep_files and the destination-cleaning warning. Changed 'cleaned on every build' to 'cleaned by default', as the page says.

Method: documentation only; no commands were run.
