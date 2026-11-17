---
id: computing-software.web-development.jekyll.plugin-installation
name: plugin-installation
category: computing-software
field: web-development
product: jekyll
tags: [plugins, plugins-dir, plugins-key, safe-mode-whitelist, gemfile-plugins, jekyll-plugins-group]
level: practitioner
status: docs-checked
description: "Load Jekyll plugins three ways: .rb files in _plugins, gems listed under plugins (and whitelist in safe mode), and Gemfile entries including the :jekyll_plugins group."
sources:
  - https://raw.githubusercontent.com/jekyll/jekyll/master/docs/_docs/plugins/installation.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Route 1: any `.rb` file in `_plugins` at the source root loads automatically. The directory can change via CLI or config. It is skipped in `safe` mode and cannot extend the CLI.

Route 2: list plugin gems under top-level `plugins`; in `safe` mode they must also be under `whitelist`:

```yaml
plugins:
  - jekyll-gist
  - jekyll-seo-tag
  - some-other-jekyll-plugin
safe: true
whitelist:
  - jekyll-gist
  - jekyll-seo-tag
```

Here `some-other-jekyll-plugin` is not loaded in safe mode. Without a Gemfile, install the gems yourself with `gem install`.

Route 3: Gemfile with Bundler. List all primary dependencies, including Jekyll itself, because Bundler limits gems to the Gemfile's runtime dependencies. Include gems that custom `_plugins` code needs. Install with `bundle install`.

```ruby
source "https://rubygems.org"
gem "jekyll"
gem "jekyll-gist"
gem "jekyll-seo-tag", "~> 1.5"
```

Gems in the `:jekyll_plugins` group load at the very start of any Jekyll process, regardless of `--safe` or config. That allows CLI subcommands and avoids listing them in config, but you must be careful what you put there:

```ruby
group :jekyll_plugins do
  gem "jekyll-cli-plus"
end
```

All three routes can be used together.

## Checked

2026-11-04. Confirmed against the Jekyll Plugins installation page: _plugins directory, plugins and whitelist keys, Gemfile guidance and the :jekyll_plugins group. Nothing removed.

Method: documentation only; no commands were run.
