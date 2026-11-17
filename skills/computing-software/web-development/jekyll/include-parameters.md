---
id: computing-software.web-development.jekyll.include-parameters
name: include-parameters
category: computing-software
field: web-development
product: jekyll
tags: [include-parameters, include-content, capture-tag, default-filter, templated-includes]
level: advanced
status: docs-checked
description: "Pass parameters to Jekyll includes and read them as include.name, default missing values, and pass strings containing variables by capturing them first."
sources:
  - https://raw.githubusercontent.com/jekyll/jekyll/master/docs/_docs/includes.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Parameters are given in the include call and read as `include.<name>`. `_includes/note.html`:

```liquid
<div markdown="span" class="alert alert-info" role="alert">
<b>Note:</b> {{ include.content }}
</div>
```

Call it:

```liquid
{% include note.html content="This is my sample note." %}
```

Several parameters work the same way. `image.html` could use `include.url`, `include.file`, `include.max-width`, `include.alt` and `include.caption`:

```liquid
{% include image.html url="http://jekyllrb.com"
max-width="200px" file="logo.png" alt="Jekyll logo"
caption="This is the Jekyll logo." %}
```

Guard against a missing value with Liquid's `default` filter.

A parameter string cannot contain curly braces, so `"The latest version of {{ site.product_name }} is now available."` fails. Store it with `capture`, then pass the variable without quotation marks:

```liquid
{% capture download_note %}
The latest version of {{ site.product_name }} is now available.
{% endcapture %}

{% include note.html content=download_note %}
```

Parameterised includes are useful for hiding complex markup from Markdown authors.

## Checked

2026-11-04. Confirmed against the Jekyll includes doc: `include.<name>` parameters, the `note.html` and `image.html` examples and their five parameters, the `default` filter advice, the no-curly-braces limit, and the `capture` workaround with unquoted variable. Nothing removed.

Method: documentation only; no commands were run.
