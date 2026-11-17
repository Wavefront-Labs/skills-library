---
id: computing-software.web-development.jekyll.custom-hook-owners
name: custom-hook-owners
category: computing-software
field: web-development
product: jekyll
tags: [custom-hooks, hook-owner, trigger-hooks, excerpt-hooks]
level: sme
status: docs-checked
description: "Add hooks to your own Jekyll objects by calling Jekyll::Hooks.trigger under a custom owner name and registering handlers, shown with a hooked Excerpt class."
sources:
  - https://raw.githubusercontent.com/jekyll/jekyll/master/docs/_docs/plugins/hooks.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Plugins can register and trigger hooks for Jekyll objects they introduce. Place `trigger` calls under an owner name at the positions you want inside your class, then register handlers for that owner.

Example: custom behaviour for every initialised `Excerpt` object, owner `:excerpts`.

```ruby
module Foobar
  class HookedExcerpt < Jekyll::Excerpt
    def initialize(doc)
      super
      trigger_hooks(:post_init)
    end

    def output
      @output ||= trigger_hooks(:post_render, renderer.run)
    end

    def renderer
      @renderer ||= Jekyll::Renderer.new(
        doc.site, self, site.site_payload
      )
    end

    def trigger_hooks(hook_name, *args)
      Jekyll::Hooks.trigger :excerpts, hook_name, self, *args
    end
  end
end

Jekyll::Hooks.register :excerpts, :post_init do |excerpt|
  Jekyll.logger.debug "Initialized:",
                      "Hooked Excerpt for #{excerpt.doc.inspect}"
end

Jekyll::Hooks.register :excerpts, :post_render do |excerpt, output|
  return output unless excerpt.doc.type == :posts
  Foobar.transform(output)
end
```

The trigger passes the object first (`self`), then extra arguments such as the rendered output.

## Checked

2026-11-04. Confirmed against the Jekyll plugins Hooks page, custom objects section: the HookedExcerpt example and trigger argument order. Nothing removed.

Method: documentation only; no commands were run.
