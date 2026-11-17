---
id: computing-software.web-development.jekyll.link-and-post-url-tags
name: link-and-post-url-tags
category: computing-software
field: web-development
product: jekyll
tags: [link-tag, post-url-tag, internal-links, link-validation, root-relative-paths]
level: practitioner
status: docs-checked
description: "Link to pages, posts, collection items and files with the link and post_url tags: root-relative paths, subdirectories, variables, build-time validation and limits."
sources:
  - https://raw.githubusercontent.com/jekyll/jekyll/master/docs/_docs/liquid/tags.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Since 4.0 you do not need to prepend `site.baseurl` to either tag.

`link` generates the correct permalink for a post, page, collection item or file. Include the original file extension, and give the path from the site root, not from the current page:

```liquid
{% link _collection/name-of-document.md %}
{% link _posts/2016-07-26-name-of-post.md %}
{% link news/index.html %}
[Link to a file]({% link /assets/files/doc.pdf %})
```

A link from `pages/folder1/folder2/page_a.md` to `pages/folder1/page_b.md` uses `/pages/folder1/page_b.md`, not `../page_b.html`. Print `page.path` if unsure.

Missing targets fail the build, which catches broken links. Filters cannot be applied (no `| append: "#section1"`); use plain HTML or Markdown for section anchors. The filename may be a variable: `{% link {{ page.my_variable }} %}`.

`post_url` links to a post with no extension; include the subdirectory if posts are nested:

```liquid
{% post_url 2010-07-21-name-of-post %}
{% post_url /subdir/2010-07-21-name-of-post %}
[Name of Link]({% post_url 2010-07-21-name-of-post %})
```

From 4.5.0 the argument can be a variable, e.g. looping over data and using `{% post_url {{ cool_post.slug }} %}`.

## Checked

2026-11-04. Confirmed against the Jekyll Liquid tags doc (Links): the 4.0 baseurl note, `link` examples and extension requirement, root-relative path example, validation, no filters, variable file name, `post_url` forms and subdirectories, and the 4.5.0 variable form. Nothing removed.

Method: documentation only; no commands were run.
