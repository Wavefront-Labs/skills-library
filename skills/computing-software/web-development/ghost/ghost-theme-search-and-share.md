---
id: computing-software.web-development.ghost.ghost-theme-search-and-share
name: ghost-theme-search-and-share
category: computing-software
field: web-development
product: ghost
tags: [ghost, theme, search, native-share, data-ghost-search, algolia]
level: practitioner
status: docs-checked
description: "Add Ghost's built-in search and native share modal to a theme with helpers, data attributes and the hash links."
sources:
  - https://github.com/TryGhost/docs/blob/main/themes/search.mdx
  - https://github.com/TryGhost/docs/blob/main/themes/share.mdx
  - https://github.com/TryGhost/docs/blob/main/themes/helpers/utility/search.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: ship search and sharing without custom JavaScript.

Search: add a link to `#/search` in the navigation, use the `{{search}}` helper (renders an icon button using currentColor; override styling with `.gh-search-icon` and `!important`), or add the `data-ghost-search` attribute to any element. Clicking opens the search modal; `Cmd/Ctrl + K` also opens it.

Technical limits: tag and author results need the tag and author taxonomies defined in routes.yaml; search covers titles and excerpts of the most recent 10,000 posts, and excerpts are excluded for member-only posts. For larger or more complex sites, the docs recommend an Algolia index kept updated via webhooks and Netlify Functions.

Share: link to `#/share` anywhere in the theme (post footer, floating bar, menu). Ghost opens a native modal with share options; picking a platform opens it with the post title and link prefilled. Themes without the link still work, and official Ghost themes already include one.

The `{{search}}` helper outputs `<button class="gh-search-icon" aria-label="search" data-ghost-search ...>` with an inline SVG icon. The page's Casper example for the attribute is `<button class="gh-search" data-ghost-search>{{> "icons/search"}}</button>`. The share link is plain `<a href="#/share">Share</a>`; a link ending in `#/share` opens the modal. For Algolia, the page names Algolia Ghost CLI to pre-populate the index and the Algolia Netlify package, whose Netlify Functions process webhook events to index, reindex or unindex a URL.

## Checked

Date: 2026-11-07. Read in full (GitHub blob text, 47, 29 and 26 lines, code samples inline, no imported snippets): themes/search.mdx, themes/share.mdx and themes/helpers/utility/search.mdx. Search entry points, shortcut, technical limits, Algolia recommendation and share behaviour match. The Algolia CLI and Netlify package documentation linked from the search page were not opened. Removed the Verify step.
Method: documentation only; no commands were run.
