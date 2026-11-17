---
id: computing-software.web-development.vite.html-options
name: html-options
category: computing-software
field: web-development
product: vite
tags: [html-csp-nonce-option, additional-asset-sources, custom-element-assets]
level: advanced
status: docs-checked
description: "Use html.cspNonce and html.additionalAssetSources to treat custom web components or data-* attributes as asset sources, with srcAttributes, srcsetAttributes and filter."
sources:
  - https://raw.githubusercontent.com/vitejs/vite/main/docs/config/shared-options.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`html.cspNonce` (string): nonce placeholder for generated script and style tags; it also generates a meta tag with the nonce.

`html.additionalAssetSources` (`Record<string, HtmlAssetSource>`) extends the built-in element list (`<img src>`, `<video src>`, `<link href>` ...) for custom web components or non-standard attributes:

```ts
interface HtmlAssetSource {
  srcAttributes?: string[]
  srcsetAttributes?: string[]
  filter?: (data: {
    key: string
    value: string
    attributes: Record<string, string>
  }) => boolean
}
```

```js
html: {
  additionalAssetSources: {
    'html-import': { srcAttributes: ['src'] },
    img: { srcAttributes: ['data-src-dark', 'data-src-light'] },
    'my-picture': { srcsetAttributes: ['data-srcset'] },
    'my-component': {
      srcAttributes: ['asset'],
      filter: ({ attributes }) => attributes.type === 'image',
    },
  },
}
```

## Checked

2026-11-07. Confirmed against the `html.cspNonce` and `html.additionalAssetSources` sections of config/shared-options.md (read line by line; the rest of the long page was not read for this skill): the types, the `HtmlAssetSource` interface, the purpose text and the four-case example. Nothing removed.

Method: documentation only; no commands were run.
