---
id: computing-software.web-development.jekyll.tags-and-categories
name: tags-and-categories
category: computing-software
field: web-development
product: jekyll
tags: [post-tags, post-categories, site-tags, site-categories, category-from-path]
level: practitioner
status: docs-checked
description: "Use Jekyll post tags and categories: front matter keys, whitespace splitting, site.tags iteration, categories from folders and their effect on URLs."
sources:
  - https://raw.githubusercontent.com/jekyll/jekyll/master/docs/_docs/posts.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Tags: set `tag` (single) or `tags` (multiple) in front matter. A string with whitespace under `tags` is split: `tags: classic hollywood` gives `["classic", "hollywood"]`, while `tag: classic hollywood` stays one entry `"classic hollywood"`. Jekyll stores the plural key for Liquid.

`site.tags` yields pairs: item 0 is the tag name, item 1 an array of posts.

```liquid
{% for tag in site.tags %}
  <h3>{{ tag[0] }}</h3>
  <ul>
    {% for post in tag[1] %}
      <li><a href="{{ post.url }}">{{ post.title }}</a></li>
    {% endfor %}
  </ul>
{% endfor %}
```

Categories: keys `category` or `categories` follow the same splitting logic, and `site.categories` is iterated the same way. Differences from tags:

- Any directory above `_posts` is also a category. A post at `movies/horror/_posts/2019-05-21-bride-of-chucky.markdown` gets `movies` and `horror`.
- Front matter categories are added to that list if not already present.
- Categories can appear in the generated URL; tags cannot.

For that post, `category: classic hollywood` gives `movies/horror/classic%20hollywood/2019/05/21/bride-of-chucky.html`, whereas `categories: classic hollywood` gives `movies/horror/classic/hollywood/2019/05/21/bride-of-chucky.html`.

## Checked

2026-11-04. Confirmed against the Jekyll posts doc (Tags and Categories): `tag` versus `tags` splitting, `site.tags` pairs, categories from folders above `_posts`, merging with front matter categories, URL effect, and both example URLs. Nothing removed.

Method: documentation only; no commands were run.
