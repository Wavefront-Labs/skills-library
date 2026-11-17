---
id: computing-software.web-development.vitepress.algolia-docsearch-and-ask-ai
name: algolia-docsearch-and-ask-ai
category: computing-software
field: web-development
product: vitepress
tags: [vitepress, algolia, docsearch, ask-ai, search-provider-algolia, sidepanel, assistantid, crawler]
level: advanced
status: docs-checked
description: "Configure Algolia DocSearch with appId/apiKey/indexName, multilingual search, and Ask AI modes including side panel and hybrid."
sources:
  - https://raw.githubusercontent.com/vuejs/vitepress/main/docs/en/reference/default-theme-search.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
```ts
themeConfig: {
  search: {
    provider: 'algolia',
    options: { appId: '...', apiKey: '...', indexName: '...' }
  }
}
```

For multilingual search the docs give a full example and point to the official Algolia DocSearch translations reference. The page also shows an example crawler config based on the VitePress docs site.

**Ask AI.** Pass `askAi` as an assistant id string or an object (`assistantId` required; `appId`, `apiKey`, `indexName` default to the top-level values):

```ts
options: { appId, apiKey, indexName, askAi: { assistantId: 'XXXYYY' } }
```

Omit `askAi` to stay with keyword search only.

**Side panel** (DocSearch v4.5+). Opens with Ctrl/Cmd+I by default:

```ts
askAi: {
  assistantId: 'XXXYYY',
  sidePanel: { panel: { variant: 'floating', side: 'right', width: '360px', expandedWidth: '580px', suggestedQuestions: true } }
}
```

Use `askAi.sidePanel.panel.suggestedQuestions`; the top-level `askAi.suggestedQuestions` is not enough in side panel mode. Disable the shortcut with `sidePanel: { keyboardShortcuts: { 'Ctrl/Cmd+I': false } }`.

**Mode:** `auto` (default; hybrid if keyword search is configured, else sidePanel), `sidePanel` (hides keyword button), `hybrid` (keyword modal plus side panel), `modal` (Ask AI inside the DocSearch modal).

**Ask AI only:** `mode: 'sidePanel'` with credentials under `askAi` and `sidePanel: true`.

## Checked

2026-11-04. Confirmed against the VitePress default-theme search page (Algolia Search, Ask AI, Ask AI Side Panel, Mode, Ask AI only, Crawler Config sections): provider and options, askAi as string or object with assistantId, sidePanel.panel options, suggestedQuestions note, keyboardShortcuts, the four modes, Ask AI only config. Removed: the claim that apiKey is a public search-only key, the claim about themeConfig.algolia/carbonAds locale overrides and `search.options.locales` for Algolia (the page only gives a snippet for that), and the Verify step.

Method: documentation only; no commands were run.
