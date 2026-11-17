---
id: computing-software.web-development.astro.slot-fallback-and-transfer
name: slot-fallback-and-transfer
category: computing-software
field: web-development
product: astro
tags: [slot-fallback, slot-transfer, nested-layouts, empty-slot]
level: practitioner
status: docs-checked
description: "Render fallback content when a slot receives nothing, know the empty-slot caveat, and transfer slots to another component with name plus slot attributes."
sources:
  - https://raw.githubusercontent.com/withastro/docs/main/src/content/docs/en/basics/astro-components.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Fallback content: a `<slot />` renders its own children when nothing matching is passed.

```astro
<slot>
  <p>This is my fallback content, if there is no child passed into slot</p>
</slot>
```

Caveat: when a slot element exists but has no content, Astro passes an empty slot, and fallback content is not used. Fallback shows only when no slot element can be found. For a named slot it shows only when no element with the matching `slot="name"` is passed.

Transferring slots: use both `name` and `slot` on a `<slot />` tag to forward a named slot to another component.

```astro
---
// src/layouts/BaseLayout.astro
---
<html lang="en">
  <head>
    <slot name="head" />
  </head>
  <body>
    <slot />
  </body>
</html>
```

```astro
// src/layouts/HomeLayout.astro
---
import BaseLayout from './BaseLayout.astro';
---
<BaseLayout>
  <slot name="head" slot="head" />
  <slot />
</BaseLayout>
```

```astro
// src/pages/index.astro
---
import HomeLayout from '../layouts/HomeLayout.astro';
---
<HomeLayout>
	<title slot="head">Astro</title>
	<h1>Astro</h1>
</HomeLayout>
```

The default and `head` slots passed to `HomeLayout` reach `BaseLayout`.

## Checked

2026-11-04. Confirmed against the Astro components page: fallback content, the empty-slot caveat, transferring slots with name plus slot, nested layout example. Nothing removed.

Method: documentation only; no commands were run.
