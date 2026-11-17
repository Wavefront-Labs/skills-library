---
id: computing-software.web-development.eleventy.collections-api
name: collections-api
category: computing-software
field: web-development
product: eleventy
tags: [addcollection, collections-api, getfilteredbytag, getfilteredbyglob, getallsorted]
level: practitioner
status: docs-checked
description: "Build custom Eleventy collections in the config with addCollection and the getAll, getAllSorted and getFilteredBy tag or glob methods."
sources:
  - https://www.11ty.dev/docs/collections-api/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
```js
export default function (eleventyConfig) {
  eleventyConfig.addCollection("myCollectionName", async (collectionsApi) => {
    return collectionsApi.getAllSorted();
  });
};
```

The callback may return any object type: arrays, strings, objects. It is available as `collections.myCollectionName`.

Methods on `collectionsApi`:

- `getAllSorted()`: default sort (ascending by date, filename tiebreaker).
- `getAll()`: arbitrary order, marginally faster.
- `getFilteredByTag("post")`: sorted array.
- `getFilteredByTags("post", "travel", "photo")`: items having all the tags.
- `getFilteredByGlob("_posts/*.md")`: one glob or an array; matched against the full `inputPath` including the input directory.

`getFilteredByGlob` filters what `getAllSorted` returns. It does not scan the file system, does not match the includes directory, anything with `eleventyExcludeFromCollections`, or file types Eleventy does not support.

All API methods return new array copies, so `.reverse()` here has no side effect on other collections (`.toReversed()` also works, Node 20+).

```js
eleventyConfig.addCollection("onlyMarkdown", (api) =>
  api.getAllSorted().filter((item) => item.inputPath.endsWith(".md")));
eleventyConfig.addCollection("byDateDesc", (api) =>
  api.getAll().sort((a, b) => b.date - a.date));
```

## Checked

2026-11-04. Confirmed against the Eleventy Collections API page: addCollection (async-friendly), arbitrary return types, getAllSorted, getAll (arbitrary order, marginally faster), getFilteredByTag, getFilteredByTags (all tags), getFilteredByGlob (glob or array, matched against the full inputPath, filters getAllSorted, ignores includes, eleventyExcludeFromCollections and unsupported file types), copies returned so reverse() is safe, toReversed on Node 20+. Removed the unconfirmed 0.5.3+ version gate.

Method: documentation only; no commands were run.
