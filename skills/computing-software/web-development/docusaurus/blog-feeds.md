---
id: computing-software.web-development.docusaurus.blog-feeds
name: blog-feeds
category: computing-software
field: web-development
product: docusaurus
tags: [rss, atom, json-feed, feedoptions, createfeeditems]
level: practitioner
status: docs-checked
description: "Generate RSS, Atom and JSON feeds for the Docusaurus blog with feedOptions: types, copyright, limit, XSLT, createFeedItems, and where the feeds are served."
sources:
  - https://raw.githubusercontent.com/facebook/docusaurus/main/website/docs/blog.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
By default RSS and Atom feeds are generated. Disable with `feedOptions.type: null`.

`feedOptions` fields: `type` (`'rss' | 'atom' | 'json' | 'all'` or an array, or `null`), `title`, `description`, `copyright` (required in the type), `language`, `limit` (number, `false` or `null`; defaults to 20), `xslt` (boolean or `{rss, atom}` so browsers can style the XML), and `createFeedItems`.

```js title="docusaurus.config.js"
blog: {
  feedOptions: {
    type: 'all',
    copyright: `Copyright © ${new Date().getFullYear()} Facebook, Inc.`,
    createFeedItems: async (params) => {
      const {blogPosts, defaultCreateFeedItems, ...rest} = params;
      return defaultCreateFeedItems({
        blogPosts: blogPosts.filter((item, index) => index < 10),
        ...rest,
      });
    },
  },
},
```

`createFeedItems` receives `blogPosts`, `siteConfig`, `outDir` and `defaultCreateFeedItems`, so you can wrap the default to filter or alter items.

Feed locations:

- `https://example.com/blog/rss.xml`
- `https://example.com/blog/atom.xml`
- `https://example.com/blog/feed.json`

RSS feeds need an author's email to be set for that author to appear in the feed.

## Checked

2026-11-04. Read in full against the Docusaurus Blog page, Feed section: default RSS and Atom, feedOptions.type null to disable, option list, limit default of 20, xslt, createFeedItems example and the three feed URLs match. Narrowed the author email note to RSS feeds, as the page states it.

Method: documentation only; no commands were run.
