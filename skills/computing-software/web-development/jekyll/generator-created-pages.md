---
id: computing-software.web-development.jekyll.generator-created-pages
name: generator-created-pages
category: computing-software
field: web-development
product: jekyll
tags: [jekyll-page-subclass, category-pages, url-placeholders, frontmatter-defaults-type, generator-pages]
level: sme
status: docs-checked
description: "Generate pages at build time from a Jekyll generator by subclassing Jekyll::Page, with url_placeholders and a custom defaults type configurable from config."
sources:
  - https://raw.githubusercontent.com/jekyll/jekyll/master/docs/_docs/plugins/generators.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
To make a page per category, a generator appends `Jekyll::Page` subclass instances to `site.pages`. Since the pages exist only at runtime, the plugin defines their content, front matter and attributes.

```ruby
module SamplePlugin
  class CategoryPageGenerator < Jekyll::Generator
    safe true

    def generate(site)
      site.categories.each do |category, posts|
        site.pages << CategoryPage.new(site, category, posts)
      end
    end
  end

  class CategoryPage < Jekyll::Page
    def initialize(site, category, posts)
      @site = site
      @base = site.source
      @dir  = category
      @basename = 'index'
      @ext      = '.html'
      @name     = 'index.html'
      @data = { 'linked_docs' => posts }

      data.default_proc = proc do |_, key|
        site.frontmatter_defaults.find(relative_path, :categories, key)
      end
    end

    def url_placeholders
      { :path => @dir, :category => @dir,
        :basename => basename, :output_ext => output_ext }
    end
  end
end
```

Design choices: the basename is `index` so each page renders as a directory index; `linked_docs` exposes the category's posts as `page.linked_docs`; the `default_proc` looks up front matter defaults scoped to type `categories`.

Then configure layout and path through defaults:

```yaml
defaults:
  - scope:
      type: categories
    values:
      layout: category_page
      permalink: categories/:category/
```

## Checked

2026-11-04. Confirmed against the Jekyll plugins Generators page: the CategoryPage example, url_placeholders, default_proc lookup and the defaults scope. Nothing removed.

Method: documentation only; no commands were run.
