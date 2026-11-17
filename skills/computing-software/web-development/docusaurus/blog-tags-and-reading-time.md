---
id: computing-software.web-development.docusaurus.blog-tags-and-reading-time
name: blog-tags-and-reading-time
category: computing-software
field: web-development
product: docusaurus
tags: [blog-tags, tags-yml, reading-time, showreadingtime, wordsperminute]
level: practitioner
status: docs-checked
description: "Tag blog posts inline or via blog/tags.yml, and show, tune or disable reading time with the readingTime callback and wordsPerMinute."
sources:
  - https://raw.githubusercontent.com/facebook/docusaurus/main/website/docs/blog.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Tags are declared in front matter. Define inline, or reference keys from an optional tags file (usually `blog/tags.yml`).

```md title="blog/my-post.md"
---
tags:
  - Releases
  - docusaurus
---
```

```yml title="blog/tags.yml"
docusaurus:
  label: 'Docusaurus'
  permalink: '/docusaurus'
  description: 'Blog posts related to the Docusaurus framework'
```

`docusaurus` is predefined; `Releases` is inline because it is not in the file.

Reading time is estimated from word count. Control it in the blog options:

```js
blog: {
  showReadingTime: true, // false hides "x min read"
  readingTime: ({content, locale, frontMatter, defaultReadingTime}) =>
    frontMatter.hide_reading_time
      ? undefined
      : defaultReadingTime({content, locale, options: {wordsPerMinute: 100}}),
},
```

The callback gets `content`, `frontMatter`, `locale` and `defaultReadingTime`. The default returns minutes as a number, or `undefined` to disable it for that page; its option `wordsPerMinute` defaults to 300. You can also call your own implementation, for example `myReadingTime(content, locale)`.

## Checked

2026-11-04. Read in full against the Docusaurus Blog page: tags front matter, optional blog/tags.yml, inline versus predefined tags, showReadingTime, the readingTime callback parameters, undefined to disable per page, and wordsPerMinute default of 300 match. Nothing removed.

Method: documentation only; no commands were run.
