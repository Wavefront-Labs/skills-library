---
id: computing-software.web-development.jekyll.converters
name: converters
category: computing-software
field: web-development
product: jekyll
tags: [converter-plugin, matches-method, output-ext, convert-method, custom-markup]
level: advanced
status: docs-checked
description: "Add a markup language to Jekyll with a converter plugin implementing matches, output_ext and convert, and remember files still need front matter."
sources:
  - https://raw.githubusercontent.com/jekyll/jekyll/master/docs/_docs/plugins/converters.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Converters add support for a new markup language; Markdown and Textile are implemented this way. Jekyll converts only files with a YAML header at the top, even for plugin converters.

Example: convert files ending in `.upcase`:

```ruby
module Jekyll
  class UpcaseConverter < Converter
    safe true
    priority :low

    def matches(ext)
      ext =~ /^\.upcase$/i
    end

    def output_ext(ext)
      ".html"
    end

    def convert(content)
      content.upcase
    end
  end
end
```

Three methods are the minimum:

- `matches(ext)`: takes the file extension including the dot; returns true or false.
- `output_ext(ext)`: the extension of the output file, including the dot, usually `".html"`.
- `convert(content)`: takes the raw file content without front matter and returns a String.

Here `matches` checks for `.upcase`, `convert` upcases the content, and the page is saved with an `.html` extension.

## Checked

2026-11-04. Confirmed against the Jekyll plugins Converters page: front matter requirement, the UpcaseConverter example and the three minimum methods. Nothing removed.

Method: documentation only; no commands were run.
