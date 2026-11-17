---
id: computing-software.web-development.jekyll.hooks
name: hooks
category: computing-software
field: web-development
product: jekyll
tags: [hooks, jekyll-hooks-register, post-render, pre-render, post-convert, hook-payload]
level: sme
status: docs-checked
description: "Use Jekyll hooks: register with Jekyll::Hooks.register, owners (site, pages, documents, posts, clean), events and the payload given to pre_render and site post_render."
sources:
  - https://raw.githubusercontent.com/jekyll/jekyll/master/docs/_docs/plugins/hooks.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Register a hook with an owner, an event name and a block:

```ruby
Jekyll::Hooks.register :pages, :post_render do |page|
  # code to call after Jekyll renders a page
end
```

Owners: `:site`, `:pages`, `:documents`, `:clean`. Document hooks can target one collection by its name, e.g. `:posts` or `:movies`. The owner object is the first callback parameter.

Events for `:pages`, `:documents`, `:posts`: `:post_init`, `:pre_render`, `:post_convert` (4.2.0+), `:post_render`, `:post_write`.

`:site` events:

- `:after_init`: after site initialises; good for changing configuration; once per build/serve session.
- `:after_reset`: after the site resets during regeneration.
- `:post_read`: after source files are read.
- `:pre_render`: before rendering the whole site.
- `:post_render`: after rendering the whole site, before writing.
- `:post_write`: after all files are written.

`:clean` has `:on_obsolete`, during destination cleanup before the build.

Payload: all `:pre_render` hooks and `:site, :post_render` receive a `payload` hash as the second parameter. In `:pre_render` it controls variables available during rendering; in `:site, :post_render` it holds the final values after rendering, useful for sitemaps and feeds.

Page, document and post `:post_convert` runs after conversion but before the layout is rendered.

## Checked

2026-11-04. Confirmed against the Jekyll plugins Hooks page: register syntax, owners, events, 4.2.0 post_convert, :site and :clean events and payload rules. Nothing removed.

Method: documentation only; no commands were run.
