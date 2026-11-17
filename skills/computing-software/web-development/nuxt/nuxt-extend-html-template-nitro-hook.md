---
id: computing-software.web-development.nuxt.nuxt-extend-html-template-nitro-hook
name: nuxt-extend-html-template-nitro-hook
category: computing-software
field: web-development
product: nuxt
tags: [nuxt, nitro, render-html, html-template, nitro-plugin]
level: advanced
status: docs-checked
description: "Mutate the rendered HTML or response by registering render:html and render:response hooks in a Nitro plugin under server/plugins."
sources:
  - https://github.com/nuxt/nuxt/blob/main/docs/1.getting-started/04.views.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
You can have full control over the HTML template by adding a Nitro plugin that registers a hook. The callback of the `render:html` hook lets you mutate the HTML before it is sent to the client; the `html` argument is an object representation of the HTML template. If you only need to modify the `<head>`, the docs point to the SEO and meta section instead.

```ts
// server/plugins/extend-html.ts
import { definePlugin } from 'nitro'

export default definePlugin((nitroApp) => {
  nitroApp.hooks.hook('render:html', (html, { event }) => {
    html.head.push(`<meta name="description" content="My custom description" />`)
  })

  // you can also intercept the response
  nitroApp.hooks.hook('render:response', (response, { event }) => {
    console.log(response)
  })
})
```

For the list of hooks see the hooks guide in the Nuxt docs.

## Checked

2026-11-04. Confirmed against the Nuxt views page, section "Advanced: Extending the HTML Template": Nitro plugin location in server/plugins, render:html and render:response hooks, the head.push example, the SEO and meta pointer. Removed (not in the page): the claims about client navigation, branching on the event, body-level edits, and the Verify step.

Method: documentation only; no commands were run.
