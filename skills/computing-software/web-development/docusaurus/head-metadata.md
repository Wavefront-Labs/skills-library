---
id: computing-software.web-development.docusaurus.head-metadata
name: head-metadata
category: computing-software
field: web-development
product: docusaurus
tags: [head-metadata, head-tag, react-helmet, page-description, seo-metadata]
level: practitioner
status: docs-checked
description: "Add or override page head metadata from a Docusaurus Markdown file with a head tag, and control the page description used for metadata and category cards."
sources:
  - https://raw.githubusercontent.com/facebook/docusaurus/main/website/docs/guides/markdown-features/markdown-features-head-metadata.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Docusaurus sets page metadata in `<html>`, `<head>` and `<body>`. Add or override with a `<head>` tag in Markdown:

```md
---
id: head-metadata
title: Head Metadata
---

<head>
  <html className="some-extra-html-class" />
  <body className="other-extra-body-class" />
  <title>Head Metadata customized title!</title>
  <meta charSet="utf-8" />
  <meta name="twitter:card" content="summary" />
  <link rel="canonical" href="https://example.com/docs/head-metadata" />
</head>

# Head Metadata
```

This is built on the `<Head>` component from `@docusaurus/Head`, itself based on react-helmet; see its docs for the full API.

For regular SEO you do not need it: content plugins accept front matter such as `description`, `keywords` and `image`, which set both `description` and `og:description` automatically. With a `<head>` tag you would declare both tags by hand.

Page description: the description metadata is also used elsewhere, for example by the docs plugin's generated category index cards. By default it is the first content-ful line, converted to plain text with best effort (links and emphasis stripped). Where that is poor, set it in front matter:

```md
---
description: This description will override the default.
---
```

## Checked

2026-11-04. Read in full against the Docusaurus Head metadata page (markdown-features-head-metadata.mdx, fetched as raw text because the stripped copy was empty): the head tag in Markdown, Head component and react-helmet note, front matter tip for description and og:description, and the default description rule with front matter override all match. Nothing removed.

Method: documentation only; no commands were run.
