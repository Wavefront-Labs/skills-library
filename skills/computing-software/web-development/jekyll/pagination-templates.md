---
id: computing-software.web-development.jekyll.pagination-templates
name: pagination-templates
category: computing-software
field: web-development
product: jekyll
tags: [paginator-posts, pagination-links, page-one-edge-case, numbered-pagination]
level: practitioner
status: docs-checked
description: "Render paginated Jekyll posts with paginator.posts, prev/next links, and the page-one edge case where no page1 folder exists, using a numbered pager."
sources:
  - https://raw.githubusercontent.com/jekyll/jekyll/master/docs/_docs/pagination.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Loop over `paginator.posts` in the index HTML page, and link with `previous_page_path` / `next_page_path`:

```liquid
---
layout: default
title: My Blog
---
{% for post in paginator.posts %}
  <h1><a href="{{ post.url }}">{{ post.title }}</a></h1>
  {{ post.content }}
{% endfor %}

<div class="pagination">
  {% if paginator.previous_page %}
    <a href="{{ paginator.previous_page_path }}">Previous</a>
  {% else %}
    <span>Previous</span>
  {% endif %}
  Page: {{ paginator.page }} of {{ paginator.total_pages }}
  {% if paginator.next_page %}
    <a href="{{ paginator.next_page_path }}">Next</a>
  {% else %}
    <span>Next</span>
  {% endif %}
</div>
```

Edge case: Jekyll does not generate a `page1` folder, so a `/page1` link breaks. For a numbered pager, special-case page 1 by stripping `page:num/` from `paginate_path`:

```liquid
{% for page in (1..paginator.total_pages) %}
  {% if page == paginator.page %}
    <em>{{ page }}</em>
  {% elsif page == 1 %}
    <a href="{{ site.paginate_path | relative_url | replace: 'page:num/', '' }}">{{ page }}</a>
  {% else %}
    <a href="{{ site.paginate_path | relative_url | replace: ':num', page }}">{{ page }}</a>
  {% endif %}
{% endfor %}
```

Wrap it in `{% if paginator.total_pages > 1 %}` to hide the pager when there is one page.

## Checked

2026-11-04. Confirmed against the Jekyll pagination doc: the `paginator.posts` loop, previous/next link template, the page-one edge case (no `page1` folder), the numbered-pager snippet with its `replace` filters, and the `total_pages > 1` wrapper. Dropped the author/date markup from the example, which is not needed.

Method: documentation only; no commands were run.
