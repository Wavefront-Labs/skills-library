---
id: computing-software.web-development.docusaurus.tabs-component
name: tabs-component
category: computing-software
field: web-development
product: docusaurus
tags: [tabs, tabitem, default-tab, lazy-tabs, tabs-values]
level: intro
status: docs-checked
description: "Use the Tabs and TabItem components in Docusaurus Markdown: values and defaultValue props, default tab rules, precedence, and lazy rendering."
sources:
  - https://raw.githubusercontent.com/facebook/docusaurus/main/website/docs/guides/markdown-features/markdown-features-tabs.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
```jsx
import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

<Tabs>
  <TabItem value="apple" label="Apple" default>
    This is an apple
  </TabItem>
  <TabItem value="orange" label="Orange">
    This is an orange
  </TabItem>
</Tabs>
```

Alternatively give `values` and `defaultValue` to `Tabs`:

```jsx
<Tabs
  defaultValue="apple"
  values={[
    {label: 'Apple', value: 'apple'},
    {label: 'Orange', value: 'orange'},
  ]}>
  <TabItem value="apple">This is an apple</TabItem>
  <TabItem value="orange">This is an orange</TabItem>
</Tabs>
```

`Tabs` props take precedence over `TabItem` props.

Default tab: the first tab shows unless one `TabItem` has `default` or `Tabs` has `defaultValue`. A `defaultValue` that refers to a non-existing value throws an error. Use `defaultValue={null}` to show no tab initially.

All tabs render eagerly at build time, so search engines can index hidden tabs. Render only the default tab with `<Tabs lazy />`.

Tabs inside Markdown rely on MDX.

## Checked

2026-11-04. Read in full against the Docusaurus Tabs page (markdown-features-tabs.mdx): Tabs/TabItem usage, values and defaultValue, props precedence, default-tab rules, the defaultValue error and defaultValue={null}, eager rendering and lazy all match. Nothing removed.

Method: documentation only; no commands were run.
