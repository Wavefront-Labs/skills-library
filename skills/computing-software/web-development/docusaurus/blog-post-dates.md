---
id: computing-software.web-development.docusaurus.blog-post-dates
name: blog-post-dates
category: computing-software
field: web-development
product: docusaurus
tags: [blog-date, file-naming, date-front-matter, post-folders, publish-time]
level: practitioner
status: docs-checked
description: "How Docusaurus extracts blog post dates from file and folder names, the supported patterns, and using date front matter to order same-day posts."
sources:
  - https://raw.githubusercontent.com/facebook/docusaurus/main/website/docs/blog.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Docusaurus extracts a `YYYY-MM-DD` date from the path of a blog file. Supported patterns:

| Pattern | Example |
| --- | --- |
| Single file | `2021-05-28-my-blog-post-title.md` |
| MDX file | `2021-05-28-my-blog-post-title.mdx` |
| Single folder + `index.md` | `2021-05-28-my-blog-post-title/index.md` |
| Folder named by date | `2021-05-28/my-blog-post-title.md` |
| Nested folders by date | `2021/05/28/my-blog-post-title.md` |
| Partially nested folders | `2021/05-28-my-blog-post-title.md` |
| Nested folders + `index.md` | `2021/05/28/my-blog-post-title/index.md` |
| Date in the middle of path | `category/2021/05-28-my-blog-post-title.md` |

Choose one pattern and use it for all posts to avoid confusion. A folder per post is convenient for co-locating images.

The naming convention is optional. Provide the date in front matter instead (YAML datetime notation works), which allows finer ordering of several posts on one day:

```md
---
date: 2021-09-13T10:00
---
```

A later post would use `date: 2021-09-13T18:00`.

## Checked

2026-11-04: read the Docusaurus blog page in full. Confirmed the date pattern table, the advice to pick one pattern, folder co-location and the date front matter example. Nothing removed.

Method: documentation only; no commands were run.
