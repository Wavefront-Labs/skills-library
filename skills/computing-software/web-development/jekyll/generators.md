---
id: computing-software.web-development.jekyll.generators
name: generators
category: computing-software
field: web-development
product: jekyll
tags: [generators, jekyll-generator, site-pages, generate-method, plugins-dir]
level: advanced
status: docs-checked
description: "Write a Jekyll generator: subclass Jekyll::Generator, implement generate(site), inject data into templates, and know when generators run."
sources:
  - https://raw.githubusercontent.com/jekyll/jekyll/master/docs/_docs/plugins/generators.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
A generator subclasses `Jekyll::Generator` and defines `generate`, which receives the `Jekyll::Site` instance. The return value is ignored; it works by side effect.

Generators run after Jekyll has inventoried existing content and before the site is generated. Pages with front matter are `Jekyll::Page` instances in `site.pages`; static files are `Jekyll::StaticFile` instances in `site.static_files`.

Example: inject build-time values into `reading.html`, which has undefined variables `ongoing` and `done`:

```ruby
module Reading
  class Generator < Jekyll::Generator
    def generate(site)
      book_data = site.data['books']
      ongoing = book_data.select { |book| book['status'] == 'ongoing' }
      done = book_data.select { |book| book['status'] == 'finished' }

      reading = site.pages.find { |page| page.name == 'reading.html'}

      reading.data['ongoing'] = ongoing
      reading.data['done'] = done
    end
  end
end
```

A generator in a single file can have any name with an `.rb` extension. If split across several files, package it as a Rubygem for rubygems.org, whose name must be unique.

By default Jekyll looks in `_plugins`; change it with the `plugins_dir` config key.

## Checked

2026-11-04. Confirmed against the Jekyll plugins Generators page: generate method, run order, site.pages and site.static_files, the Reading example, single-file versus gem packaging and plugins_dir. Nothing removed.

Method: documentation only; no commands were run.
