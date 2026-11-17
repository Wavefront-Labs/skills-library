---
id: computing-software.web-development.docusaurus.search-algolia-docsearch
name: search-algolia-docsearch
category: computing-software
field: web-development
product: docusaurus
tags: [search, algolia, docsearch, contextual-search, searchbar]
level: practitioner
status: docs-checked
description: "Add search to Docusaurus with Algolia DocSearch: themeConfig.algolia fields, contextual search, Ask AI, crawler config, troubleshooting, and other search options."
sources:
  - https://raw.githubusercontent.com/facebook/docusaurus/main/website/docs/search.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Options: Algolia DocSearch (official, free for eligible developer docs and technical blogs; apply to the program), Typesense DocSearch, local search plugins, or your own swizzled `SearchBar` (community options are maintained elsewhere).

`@docusaurus/preset-classic` already includes Algolia. Otherwise install `@docusaurus/theme-search-algolia` and add it to `themes`. Then:

```js title="docusaurus.config.js"
themeConfig: {
  algolia: {
    appId: 'YOUR_APP_ID',
    apiKey: 'YOUR_SEARCH_API_KEY', // public, safe to commit
    indexName: 'YOUR_INDEX_NAME',
    contextualSearch: true,
    searchParameters: {},
    searchPagePath: 'search', // false disables
  },
},
```

Other optional fields: `externalUrlRegex`, `replaceSearchResultPathname` (`from`/`to`), `insights`, and `askAi` (an assistant ID string, or an object with `assistantId`, `indexName`, `apiKey`, `appId`, `suggestedQuestions`).

Crawler: use the official Docusaurus v3 crawler configuration; other configurations are unsupported. `initialIndexSettings` only applies when the index is first created; to change it, delete the index and recrawl. The preset's `sitemap.xml` is usable by the crawler. Search is unreliable until a crawl completes; trigger one after big changes.

Contextual search (default on) filters by current language and docs version through facets. With it off, set your own `searchParameters.facetFilters`.

No results with contextual search on usually means the index lacks facet fields: `docusaurus_tag`, `language`, `lang`, `version`, `type`. Fix: use the recommended config, delete the index, recrawl.

Style via `.DocSearch` CSS variables under `[data-theme]` in `src/css/custom.css`. Edit the component with `npm run swizzle @docusaurus/theme-search-algolia SearchBar`.

## Checked

2026-11-04: read the Docusaurus Search page in full. Confirmed the search options, free DocSearch eligibility, the algolia theme config fields, askAi forms, crawler recommendation and initialIndexSettings rule, sitemap note, contextual search and facetFilters, the facet fields for troubleshooting, styling and swizzle command. Nothing removed.

Method: documentation only; no commands were run.
