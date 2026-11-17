---
id: computing-software.web-development.docusaurus.code-title-theme-languages
name: code-title-theme-languages
category: computing-software
field: web-development
product: docusaurus
tags: [code-title, prism-theme, additionallanguages, syntax-highlighting, prism-include-languages]
level: practitioner
status: docs-checked
description: "Add code block titles, change the Prism highlighting theme, enable extra languages with additionalLanguages, and swizzle prism-include-languages for custom languages."
sources:
  - https://raw.githubusercontent.com/facebook/docusaurus/main/website/docs/guides/markdown-features/markdown-features-code-blocks.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Title: add `title="..."` after the language, separated by a space.

````md
```jsx title="/src/components/HelloCodeTitle.js"
````

Highlighting uses Prism React Renderer, chosen by the language meta string. Default theme is Palenight. Change it in theme config:

```js title="docusaurus.config.js"
import {themes as prismThemes} from 'prism-react-renderer';

export default {
  themeConfig: {prism: {theme: prismThemes.dracula}},
};
```

A Prism theme is a plain JS object, so you can write your own.

Only a subset of common languages is bundled; Java, C# and PHP are not enabled by default. Add others with `additionalLanguages`, using valid Prism component names (for example `csharp`, not `cs`; look in `node_modules/prismjs/components`). Restart Docusaurus afterwards.

```js
themeConfig: {prism: {additionalLanguages: ['powershell']}},
```

For languages Prism lacks, swizzle `prism-include-languages`:

```sh
npm run swizzle @docusaurus/theme-classic prism-include-languages
```

Then require your definition in `src/theme/prism-include-languages.js`: `require('/path/to/your/prism-language-definition');`. Custom definitions do not go in `additionalLanguages`.

## Checked

2026-11-04. Read in full against the Docusaurus Code blocks page: title key, Prism React Renderer, Palenight default, themeConfig.prism.theme with prismThemes.dracula, Java/C#/PHP not enabled by default, additionalLanguages with valid Prism component names (csharp not cs), restart, and swizzling prism-include-languages all match. Nothing removed.

Method: documentation only; no commands were run.
