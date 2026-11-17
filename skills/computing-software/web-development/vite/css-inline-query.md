---
id: computing-software.web-development.vite.css-inline-query
name: css-inline-query
category: computing-software
field: web-development
product: vite
tags: [css-inline-query, disable-css-injection, css-default-import-removed]
level: practitioner
status: docs-checked
description: "Stop Vite injecting CSS into the page with the ?inline query and get the processed CSS string as the default export; plain default CSS imports were removed in Vite 5."
sources:
  - https://raw.githubusercontent.com/vitejs/vite/main/docs/guide/features.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Automatic injection of CSS can be turned off with the `?inline` query. The processed CSS string is the module's default export, but the styles are not added to the page.

```js
import './foo.css' // will be injected into the page
import otherStyles from './bar.css?inline' // will not be injected
```

Default and named imports from CSS files (such as `import style from './foo.css'`) were removed in Vite 5. Use `?inline` instead.

## Checked

Date: 2026-11-07. Read the Disabling CSS injection section of features.md (features.md read in full). Removed the closing 'Typical use ... shadow root' sentence, which the page does not state. The `?inline` behaviour, the example and the Vite 5 removal of default/named CSS imports matched.

Method: documentation only; no commands were run.
