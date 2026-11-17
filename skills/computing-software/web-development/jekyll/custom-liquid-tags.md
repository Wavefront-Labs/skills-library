---
id: computing-software.web-development.jekyll.custom-liquid-tags
name: custom-liquid-tags
category: computing-software
field: web-development
product: jekyll
tags: [custom-tags, liquid-tag, liquid-block, register-tag, render-method]
level: advanced
status: docs-checked
description: "Create custom Liquid tags and tag blocks for Jekyll by subclassing Liquid::Tag or Liquid::Block, implementing render and registering the tag name."
sources:
  - https://raw.githubusercontent.com/jekyll/jekyll/master/docs/_docs/plugins/tags.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
A tag subclasses `Liquid::Tag` and must at least implement `render`, which outputs the tag's content. Register it with Liquid.

```ruby
module Jekyll
  class RenderTimeTag < Liquid::Tag
    def initialize(tag_name, text, tokens)
      super
      @text = text
    end

    def render(context)
      "#{@text} #{Time.now}"
    end
  end
end

Liquid::Template.register_tag('render_time', Jekyll::RenderTimeTag)
```

Use it in a page: `<p>{% render_time page rendered at: %}</p>`.

A tag block inherits `Liquid::Block`; calling `super` in `render` returns the block body:

```ruby
module Jekyll
  class RenderTimeTagBlock < Liquid::Block
    def render(context)
      text = super
      "<p>#{text} #{Time.now}</p>"
    end
  end
end

Liquid::Template.register_tag('render_time', Jekyll::RenderTimeTagBlock)
```

Used as `{% render_time %}page rendered at:{% endrender_time %}`.

Registering a tag and a tag block with the same name in one project is not recommended because it may cause conflicts.

## Checked

2026-11-04. Confirmed against the Jekyll plugins Tags page: Liquid::Tag render, register_tag, tag blocks with Liquid::Block and the same-name conflict note. Nothing removed.

Method: documentation only; no commands were run.
