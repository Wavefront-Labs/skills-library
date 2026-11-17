---
id: computing-software.web-development.jekyll.upgrading-3-to-4
name: upgrading-3-to-4
category: computing-software
field: web-development
product: jekyll
tags: [upgrade, jekyll-4, post-url-baseurl, exclude-defaults, kramdown-v2, template-caching]
level: advanced
status: docs-checked
description: "Upgrade a site from Jekyll 3.x to 4.x: post_url now adds baseurl, templates are parsed once, exclude entries add to defaults, and kramdown 2 needs extension gems."
sources:
  - https://raw.githubusercontent.com/jekyll/jekyll/master/docs/_docs/upgrading/3-to-4.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Update with `gem update jekyll` (check `ruby -v` first).

- `post_url` now applies `relative_url`, so drop manual baseurl prefixes: change `{{ site.baseurl }}/{% post_url 2018-03-20-hello-world.markdown %}` to `{% post_url 2018-03-20-hello-world.markdown %}`.
- Templates are parsed once, cached and rendered many times; some community plugins may break. Plugin authors: `site.liquid_renderer.file(path).parse(content)` returns the same object per path, so do not memoize the payload. For a fresh template use `Liquid::Template.parse(content)`.
- Static files in a collection with no `output: true` are not written, nor are its documents.
- Default `exclude` is now `.sass-cache/`, `.jekyll-cache/`, `gemfiles/`, `Gemfile`, `Gemfile.lock`, `node_modules/`, `vendor/bundle/`, `vendor/cache/`, `vendor/gems/`, `vendor/ruby/`. Your `exclude` entries are added to it, not replacing it. To process an excluded path, list it under `include`; a user `include` still replaces the default (`[".htaccess"]`), so re-add `.htaccess` if needed.
- kramdown 1.x is dropped. `kramdown-parser-gfm` installs with Jekyll 4; other kramdown 2 extensions go in your `Gemfile`. `kramdown-converter-pdf` is ignored; use a custom `Jekyll::Converter` plugin.
- Legacy deprecated config keys are no longer honored: ignored, or `InvalidConfigurationError` if the value type is wrong.

## Checked

2026-11-04. Confirmed against the Jekyll 3.x to 4.x upgrade page: post_url and baseurl, template caching, unrendered collection statics, default exclude and include behaviour, kramdown 2 and removed legacy config keys. Nothing removed.

Method: documentation only; no commands were run.
