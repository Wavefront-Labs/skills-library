---
id: computing-software.web-development.jekyll.plugin-types-and-flags
name: plugin-types-and-flags
category: computing-software
field: web-development
product: jekyll
tags: [plugin-types, safe-flag, priority-flag, plugin-gem, plugin-best-practices]
level: advanced
status: docs-checked
description: "Choose among Jekyll's six plugin types (generators, converters, commands, tags, filters, hooks) and set the safe and priority flags; package plugins as gems."
sources:
  - https://raw.githubusercontent.com/jekyll/jekyll/master/docs/_docs/plugins/your-first-plugin.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Six plugin types:

- Generators create content (jekyll-feed makes an Atom feed, jekyll-archives makes category and tag archives, jekyll-sitemap a sitemap).
- Converters change one markup into another (jekyll-textile-converter, jekyll-coffeescript, jekyll-opal).
- Commands add subcommands to the `jekyll` executable (jekyll-compose).
- Tags create custom Liquid tags.
- Filters create custom Liquid filters.
- Hooks give fine-grained control of the build process (jemoji, jekyll-mentions).

Two flags:

- `safe`: tells Jekyll whether the plugin may run where arbitrary code execution is not allowed. GitHub Pages uses it to decide which core plugins are usable. Set `true` if your plugin does not allow arbitrary code execution. GitHub Pages still will not load your plugin, but it should be correct if submitted to core.
- `priority`: load order. Values `:lowest`, `:low`, `:normal`, `:high`, `:highest`. Highest-priority matches apply first, lowest last.

```ruby
module Jekyll
  class UpcaseConverter < Converter
    safe true
    priority :low
  end
end
```

Best practice: write the plugin as a gem. That manages dependencies, separates it from site source and lets you reuse it across projects. The jekyll-feed source is a good reference.

## Checked

2026-11-04. Confirmed against the Jekyll Your first plugin page: six plugin types, safe and priority flags and the gem recommendation. Nothing removed.

Method: documentation only; no commands were run.
