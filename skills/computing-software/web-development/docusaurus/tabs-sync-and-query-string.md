---
id: computing-software.web-development.docusaurus.tabs-sync-and-query-string
name: tabs-sync-and-query-string
category: computing-software
field: web-development
product: docusaurus
tags: [tabs-groupid, querystring, synced-tabs, tab-attributes, localstorage]
level: practitioner
status: docs-checked
description: "Sync Docusaurus tab choices with groupId, persist the selection in the URL with queryString, and style tab headings with className and attributes."
sources:
  - https://raw.githubusercontent.com/facebook/docusaurus/main/website/docs/guides/markdown-features/markdown-features-tabs.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Sync: give related `Tabs` the same `groupId`. The choice persists in `localStorage` and all tab groups with that ID update together. Group IDs are globally namespaced.

```jsx
<Tabs groupId="operating-systems">
  <TabItem value="win" label="Windows">Use Ctrl + C to copy.</TabItem>
  <TabItem value="mac" label="macOS">Use Command + C to copy.</TabItem>
</Tabs>
```

Groups with the same ID need not share values; if a chosen value is missing in a group, that group does not change. Different group IDs do not interfere.

Query string: `queryString="current-os"` writes the choice into the URL (`?current-os=android`) so you can link to a pre-selected tab. It does not scroll to the tab.

```jsx
<Tabs groupId="current-os" queryString>
```

With `queryString` set to `true`, the `groupId` is the parameter name. On load, the query string choice wins over the `groupId` choice from `localStorage`.

Styling: `className` on `Tabs` is added to the tab list (`<ul role="tablist">`). Per heading, pass `attributes` on `TabItem` or in the `values` prop:

```jsx
<TabItem value="apple" label="Apple" attributes={{className: styles.red}}>
```

`className` merges with defaults. A custom `data-value` attribute pairs with CSS selectors like `li[role='tab'][data-value='apple']`. Selected headings have `aria-selected='true'`.

## Checked

2026-11-04. Read in full against the Docusaurus Tabs page: groupId sync and localStorage, global namespacing, differing values, queryString (including queryString true falling back to groupId and query string taking priority on load), className on the tab list, attributes and data-value all match. Nothing removed.

Method: documentation only; no commands were run.
