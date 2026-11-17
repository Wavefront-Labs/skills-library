---
id: computing-software.web-development.docusaurus.config-file-syntax
name: config-file-syntax
category: computing-software
field: web-development
product: docusaurus
tags: [docusaurus-config, esm, commonjs, async-config, config-creator]
level: practitioner
status: docs-checked
description: "Declare docusaurus.config.js as an object, function or async function; ESM, CommonJS and TypeScript forms; dynamic imports for ESM-only packages."
sources:
  - https://raw.githubusercontent.com/facebook/docusaurus/main/website/docs/configuration.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`docusaurus.config.js` runs in Node.js and must export either a config object or a function that creates one. It supports ES Modules, CommonJS and TypeScript.

Required: export with `export default` (or `module.exports`). Optional: `import` (or `require`) Node.js packages.

```js title="docusaurus.config.js"
export default {
  title: 'Docusaurus',
  url: 'https://docusaurus.io',
};
```

TypeScript:

```ts title="docusaurus.config.ts"
import type {Config} from '@docusaurus/types';

export default {
  title: 'Docusaurus',
  url: 'https://docusaurus.io',
} satisfies Config;
```

A function (sync or `async`) works the same:

```js title="docusaurus.config.js"
export default async function createConfigAsync() {
  return {title: 'Docusaurus', url: 'https://docusaurus.io'};
}
```

An async creator lets you import ESM-only modules, notably most Remark plugins, with a dynamic import instead of `require`:

```js
const lib = await import('lib');
```

Templates already ship a config with defaults, so you rarely write one from scratch.

## Checked

2026-11-04: read the Docusaurus configuration page in full. Confirmed object or function export, ESM, CommonJS and TypeScript support, the async creator with dynamic import. Nothing removed.

Method: documentation only; no commands were run.
