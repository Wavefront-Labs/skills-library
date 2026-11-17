---
id: computing-software.web-development.jekyll.creating-posts
name: creating-posts
category: computing-software
field: web-development
product: jekyll
tags: [posts, post-filename, post-url-tag, post-index, post-assets, charset]
level: intro
status: docs-checked
description: "Create Jekyll blog posts in _posts: the YEAR-MONTH-DAY-title.MARKUP filename, required front matter, listing posts with site.posts and linking images and files."
sources:
  - https://raw.githubusercontent.com/jekyll/jekyll/master/docs/_docs/posts.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Posts live in `_posts` (Markdown typically, HTML also works). The filename must be:

```
YEAR-MONTH-DAY-title.MARKUP
```

`YEAR` is four digits, `MONTH` and `DAY` two digits, `MARKUP` the format extension, e.g. `2011-12-31-new-years-eve-is-awesome.md`. Every post must begin with front matter (it may be empty), usually setting a layout:

```markdown
---
layout: post
title:  "Welcome to Jekyll!"
---

# Welcome
```

Link to other posts with the `post_url` tag so URLs do not break when the permalink style changes.

If a processor converts quotes to curly Unicode ones, declare the charset in the layout head: `<meta charset="utf-8">`.

Assets: put images and downloads in a folder such as `assets` and link from the site root:

```markdown
![My helpful screenshot](/assets/screenshot.jpg)
[get the PDF](/assets/mydoc.pdf)
```

Index of posts:

```liquid
<ul>
  {% for post in site.posts %}
    <li><a href="{{ post.url }}">{{ post.title }}</a></li>
  {% endfor %}
</ul>
```

`post` exists only inside the loop; use `page` for the variables of the page being rendered.

## Checked

2026-11-04. Confirmed against the Jekyll posts doc: `_posts` folder, the filename format and valid examples, required front matter, `post_url` advice, charset meta note, `assets` linking examples, the `site.posts` index and the `post` versus `page` note. Nothing removed.

Method: documentation only; no commands were run.
