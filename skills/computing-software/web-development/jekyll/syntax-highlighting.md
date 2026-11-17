---
id: computing-software.web-development.jekyll.syntax-highlighting
name: syntax-highlighting
category: computing-software
field: web-development
product: jekyll
tags: [highlight-tag, rouge, linenos, mark-lines, highlight-stylesheet, raw-endraw]
level: practitioner
status: docs-checked
description: "Highlight code in Jekyll with Rouge: the highlight tag, linenos, mark_lines, the needed stylesheet, and escaping Liquid with raw or render_with_liquid false."
sources:
  - https://raw.githubusercontent.com/jekyll/jekyll/master/docs/_docs/liquid/tags.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Jekyll highlights over 100 languages through Rouge, the default since Jekyll 3. Pygments is deprecated and unsupported in Jekyll 4: `highlighter: pygments` falls back to Rouge, which is 100% compatible with Pygments stylesheets.

```liquid
{% highlight ruby %}
def foo
  puts 'foo'
end
{% endhighlight %}
```

The argument is the language identifier, the "short name" from the Rouge list of supported languages.

- `linenos` adds line numbers: `{% highlight ruby linenos %}`.
- `mark_lines` (4.4.0+) takes a space-separated, double-quoted list of line numbers: `{% highlight ruby mark_lines="1 2" %}`. Marked lines get the class `hll`.

A highlighting stylesheet is required. Any Pygments theme CSS works, for example one copied from the jekyll-pygments-themes repository; copy it into your css directory and import it:

```css
@import "native.css";
```

Liquid is processed inside code blocks. For languages with curly braces wrap code in raw and endraw tags. Since 4.0, `render_with_liquid: false` in front matter disables Liquid for that whole document.

## Checked

2026-11-04. Confirmed against the Jekyll Liquid tags doc (Code snippet highlighting): Rouge default and over 100 languages, Pygments fallback, `highlight` tag and language short name, `linenos`, `mark_lines` (4.4.0, `hll` class), stylesheet requirement and the `native.css` import, raw/endraw, and `render_with_liquid: false` (4.0). Nothing removed.

Method: documentation only; no commands were run.
