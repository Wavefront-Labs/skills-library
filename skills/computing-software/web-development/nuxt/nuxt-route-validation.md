---
id: computing-software.web-development.nuxt.nuxt-route-validation
name: nuxt-route-validation
category: computing-software
field: web-development
product: nuxt
tags: [nuxt, route-validation, define-page-meta, not-found, dynamic-routes]
level: practitioner
status: docs-checked
description: "Validate route params per page with the validate property of definePageMeta so invalid ids produce a 404."
sources:
  - https://github.com/nuxt/nuxt/blob/main/docs/1.getting-started/07.routing.md
  - https://github.com/nuxt/nuxt/blob/main/docs/4.api/3.utils/define-page-meta.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Each page can validate its route through the `validate` property of `definePageMeta()`. It receives the `route` and returns a boolean: `true` means the route can validly be rendered with this page, `false` means it cannot, and if no other match is found that causes a 404. You can instead return an object with `status`/`statusText` to respond immediately with a customised error (other matches are then not checked).

```vue
<script setup lang="ts">
definePageMeta({
  validate (route) {
    // Check if the id is made up of digits
    return typeof route.params.id === 'string' && /^\d+$/.test(route.params.id)
  },
})
</script>
```

Details:
- The type is `(route: RouteLocationNormalized) => boolean | Promise<boolean> | Partial<NuxtError> | Promise<Partial<NuxtError>>`, so async validators are allowed.
- For more complex use cases, the routing page says to use anonymous route middleware instead.
- `definePageMeta` is a compiler macro for page components in `app/pages/` (unless configured otherwise).

## Checked

2026-11-08. Read in full from the nuxt/nuxt docs repository: docs/1.getting-started/07.routing.md (Route Validation) and docs/4.api/3.utils/define-page-meta.md (validate). Corrected: the error object uses `status`/`statusText`, not statusCode/statusMessage as the draft said. Removed: the unsupported claims about string-array params and about when the check runs, the "needing data, redirects" gloss on middleware, and the invented Verify step.

Method: documentation only; no commands were run.
