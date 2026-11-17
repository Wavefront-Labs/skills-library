---
id: computing-software.web-development.docusaurus.blog-posts-and-truncation
name: blog-posts-and-truncation
category: computing-software
field: web-development
product: docusaurus
tags: [blog-setup, blog-post, truncate-marker, blog-list, blogsidebarcount]
level: intro
status: docs-checked
description: "Set up the Docusaurus blog, write posts with front matter, mark summaries with a truncate comment, and configure list pagination and the recent-posts sidebar."
sources:
  - https://raw.githubusercontent.com/facebook/docusaurus/main/website/docs/blog.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Create a `blog` directory and add a navbar link:

```js title="docusaurus.config.js"
navbar: {items: [{to: 'blog', label: 'Blog', position: 'left'}]},
```

A post is a Markdown file in `blog`, for example `website/blog/2019-09-05-hello-docusaurus.md`. Front matter is optional; useful keys include `title`, `description`, `slug`, `authors`, `tags`, `image`, `hide_table_of_contents`.

The list page (default `/blog`) shows the summary above the truncate marker, which must be standalone renderable Markdown:

```md
Summary text.

<!-- truncate -->

Rest of the post.
```

In `.mdx` files use the MDX comment `{/* truncate */}`.

Options (set in the `blog` key of the preset):

```js
blog: {
  blogTitle: 'Docusaurus blog!',
  blogDescription: 'A Docusaurus powered blog!',
  postsPerPage: 'ALL',     // default 10; 'ALL' disables pagination
  blogSidebarCount: 'ALL', // default 5; 0 removes the sidebar; 'ALL' lists every post
  blogSidebarTitle: 'All posts',
},
```

## Checked

2026-11-04: read the Docusaurus blog page in full. Confirmed the navbar item, post example, truncate markers for md and mdx, postsPerPage default 10 and ALL, blogSidebarCount default 5, 0 and ALL, blogSidebarTitle. Nothing removed.

Method: documentation only; no commands were run.
