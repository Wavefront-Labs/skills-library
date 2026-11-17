---
id: computing-software.web-development.nuxt.nuxt-prerendering-crawl-and-routes
name: nuxt-prerendering-crawl-and-routes
category: computing-software
field: web-development
product: nuxt
tags: [nuxt, prerender, nuxt-generate, crawl-links, static-site]
level: practitioner
status: docs-checked
description: "Pre-render Nuxt pages with nuxt generate, the Nitro crawler, selective routes, ignore lists, routeRules prerender and runtime prerenderRoutes."
sources:
  - https://github.com/nuxt/nuxt/blob/main/docs/1.getting-started/15.prerendering.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`nuxt generate` builds and prerenders your app with the Nitro crawler (similar to `nuxt build` with `nitro.static` set to `true`, or `nuxt build --prerender`). By default it prerenders `/` and the pages it links to, recursively. Deploy `.output/public` to static hosting or preview it with `npx serve .output/public`. The crawler: (1) loads the root route, non-dynamic pages in `~/pages` and routes in `prerender.routes`; (2) saves the HTML and `_payload.json` to `~/.output/public/`; (3) finds anchor tags to other routes; (4) repeats until none remain. Pages not linked from a discoverable page cannot be prerendered automatically.

Selective control:

```ts
export default defineNuxtConfig({
  prerender: {
    crawlLinks: true,
    routes: ['/sitemap.xml', '/robots.txt'], // routes the crawler cannot discover
    ignore: ['/dynamic'],
  },
})
```

The top-level `prerender` option applies whichever `server.builder` you use; builder-specific options, such as Nitro's `concurrency` or `failOnError`, go in `nitro.prerender`. Or use route rules: `'/rss.xml': { prerender: true }`, `'/this-DOES-NOT-get-prerendered': { prerender: false }`, `'/blog/**': { prerender: true }` (everything under `/blog` is prerendered as long as it is linked from another page). `defineRouteRules` in a page file is a shorthand but needs the experimental `experimental.inlineRouteRules` option.

Dynamic registration:
- Inside a Nuxt context call `prerenderRoutes(['/some/other/url'])` or `prerenderRoutes('/api/content/article/my-article')`.
- The `prerender:routes` Nuxt hook is called before prerendering and receives `ctx` so you can add routes, for example `ctx.routes.add(`/${page.name}`)` for CMS pages.
- The `prerender:generate` Nitro hook (under `nitro.hooks`) is called for each route; set `route.skip = true` to skip it, for example when `route.route?.includes('private')`.

Static and prerender builds also emit `200.html` and `404.html` SPA fallbacks.

## Checked

2026-11-04. Confirmed against the Nuxt prerendering page: nuxt generate behaviour and crawler steps, prerender.routes/ignore/crawlLinks, nitro.prerender note, routeRules examples, defineRouteRules experimental flag, prerenderRoutes, the prerender:routes and prerender:generate hooks, the 200.html/404.html note. Removed the claim that ctx.routes is a Set and the Verify step.

Method: documentation only; no commands were run.
