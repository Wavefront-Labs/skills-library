---
id: computing-software.web-development.docusaurus.blog-authors
name: blog-authors
category: computing-software
field: web-development
product: docusaurus
tags: [blog-authors, authors-yml, inline-authors, global-authors, authors-pages]
level: practitioner
status: docs-checked
description: "Declare blog authors inline or globally in authors.yml, mix and override them per post, localize the file, and enable author pages."
sources:
  - https://raw.githubusercontent.com/facebook/docusaurus/main/website/docs/blog.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Use the `authors` front matter. An author needs at least a `name` or an `image_url`; `url`, `email`, `title` and `socials` are used, and other fields are allowed.

Inline, in the post:

```md
---
authors:
  name: Joel Marcey
  title: Co-creator of Docusaurus 1
  url: https://github.com/JoelMarcey
  image_url: https://github.com/JoelMarcey.png
  socials:
    x: joelmarcey
---
```

Global, in `website/blog/authors.yml` (path set by `authorsMapPath`; JSON works too):

```yml
jmarcey:
  name: Joel Marcey
  page: true # author page at /authors/jmarcey
```

Reference with `authors: jmarcey` or `authors: [jmarcey, slorber]`.

- Mix keys and inline objects in one list.
- Override global data per post: `- key: jmarcey` then `title: New title`.
- Localize at `website/i18n/[locale]/docusaurus-plugin-content-blog/authors.yml`.

Author pages: `page: true`, or `page: {permalink: '/custom-author-url'}`. This generates a page per author plus an authors index in `authors.yml` order. Only global authors can enable it.

RSS feeds only list an author whose email is set.

## Checked

2026-11-04. Read in full against the Docusaurus Blog page (blog.mdx): authors front matter requirements, inline and global authors, authorsMapPath and JSON, mixing keys with inline authors, per-post override with key, localized authors.yml path, authors pages (page: true or permalink, global authors only) and the RSS email warning match. Nothing removed.

Method: documentation only; no commands were run.
