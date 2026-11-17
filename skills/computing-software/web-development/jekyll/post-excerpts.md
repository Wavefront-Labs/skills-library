---
id: computing-software.web-development.jekyll.post-excerpts
name: post-excerpts
category: computing-software
field: web-development
product: jekyll
tags: [excerpt, excerpt-separator, page-excerpts, post-listing]
level: practitioner
status: docs-checked
description: "Show post excerpts in Jekyll: the default first-paragraph excerpt, custom excerpt_separator in front matter or config, and optional page excerpts."
sources:
  - https://raw.githubusercontent.com/jekyll/jekyll/master/docs/_docs/posts.md
  - https://raw.githubusercontent.com/jekyll/jekyll/master/docs/_docs/pages.md
  - https://raw.githubusercontent.com/jekyll/jekyll/master/docs/_docs/configuration/default.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Every post has an `excerpt` variable. By default it is the first paragraph (the default `excerpt_separator` is `"\n\n"`). Customise it by setting `excerpt_separator` in front matter or `_config.yml`:

```markdown
---
excerpt_separator: <!--more-->
---

Excerpt with multiple paragraphs

Here's another paragraph in the excerpt.
<!--more-->
Out-of-excerpt
```

List posts with excerpts:

```liquid
<ul>
  {% for post in site.posts %}
    <li>
      <a href="{{ post.url }}">{{ post.title }}</a>
      {{ post.excerpt }}
    </li>
  {% endfor %}
</ul>
```

Pages (4.1.1+): excerpts are only generated for pages when you opt in with `page_excerpts` in the config file.

```yaml
page_excerpts: true
```

## Checked

2026-11-04. Confirmed against the Jekyll posts doc and pages doc, with the default `excerpt_separator` value from the default configuration page: first-paragraph default, `excerpt_separator` in front matter or config, the `<!--more-->` example, the listing loop, and `page_excerpts` from 4.1.1. Nothing removed.

Method: documentation only; no commands were run.
