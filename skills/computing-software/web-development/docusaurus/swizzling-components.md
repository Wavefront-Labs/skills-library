---
id: computing-software.web-development.docusaurus.swizzling-components
name: swizzling-components
category: computing-software
field: web-development
product: docusaurus
tags: [swizzle, eject, wrap, theme-components, theme-original]
level: advanced
status: docs-checked
description: "Customize Docusaurus theme components by swizzling: eject versus wrap, the swizzle CLI, safe versus unsafe components, and the Root wrapper."
sources:
  - https://raw.githubusercontent.com/facebook/docusaurus/main/website/docs/swizzling.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Swizzling swaps a theme component for your own in `src/theme`. Two patterns:

- Eject: copy the original and fully customize it.
- Wrap: create a wrapper that enhances the original. Prefer this; there is less code to maintain.

```bash
npm run swizzle                                   # interactive
npm run swizzle -- --list                         # list swizzlable components
npm run swizzle @docusaurus/theme-classic Footer -- --wrap
npm run swizzle @docusaurus/theme-classic Footer -- --eject
```

Wrapper shape (`@theme-original/X` imports the shadowed original, avoiding a self-import loop):

```jsx title="src/theme/Footer/index.js"
import React from 'react';
import Footer from '@theme-original/Footer';

export default function FooterWrapper(props) {
  return (<><Footer {...props} /></>);
}
```

Restart the dev server after swizzling. To undo, delete the files from `src/theme`. The CLI is only a helper: creating `src/theme/Component.js` by hand works.

Safety levels (declared by theme authors): Safe (stable within a major version), Unsafe (may break in minor versions), Forbidden (CLI refuses). Some components are safe to wrap but not to eject. After upgrades, re-eject and compare with `git diff`.

Before swizzling, try CSS or translations (`write-translations` then edit `code.json`).

`src/theme/Root.js` is created manually. It renders above `Layout` and never unmounts, so it suits Context providers and persistent state:

```js
export default function Root({children}) {
  return <>{children}</>;
}
```

## Checked

2026-11-04: read the Docusaurus Swizzling page in full. Confirmed eject and wrap, the swizzle commands and options, @theme-original, restart and removal notes, the three safety levels, the CSS and translation alternatives and the Root component. Nothing removed.

Method: documentation only; no commands were run.
