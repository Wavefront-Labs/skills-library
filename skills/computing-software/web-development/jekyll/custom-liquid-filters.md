---
id: computing-software.web-development.jekyll.custom-liquid-filters
name: custom-liquid-filters
category: computing-software
field: web-development
product: jekyll
tags: [custom-filters, register-filter, liquid-context-registers, filter-module]
level: advanced
status: docs-checked
description: "Write a custom Liquid filter for Jekyll as a module registered with Liquid::Template.register_filter, and reach the site object through context registers."
sources:
  - https://raw.githubusercontent.com/jekyll/jekyll/master/docs/_docs/plugins/filters.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
A filter is a module whose methods are exported to Liquid. Every method must take at least one parameter, the filter input, and its return value is the output.

```ruby
module Jekyll
  module AssetFilter
    def asset_url(input)
      "http://www.example.com/#{input}?#{Time.now.to_i}"
    end
  end
end

Liquid::Template.register_filter(Jekyll::AssetFilter)
```

More details are in the Liquid docs on creating your own filters.

Access the site object from inside a filter through Liquid's context registers: `@context.registers[:site]`. For example, the global configuration is `@context.registers[:site].config`.

## Checked

2026-11-04. Confirmed against the Jekyll plugins Filters page: module shape, register_filter and @context.registers[:site]. Removed the sentence calling the registration line required, which the page does not state.

Method: documentation only; no commands were run.
