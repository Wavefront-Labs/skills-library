---
id: computing-software.web-development.vitepress.ignore-dead-links
name: ignore-dead-links
category: computing-software
field: web-development
product: vitepress
tags: [vitepress, ignoredead-links, ignoredeadlinks, dead-links, link-checking, localhost-links, build-failure]
level: practitioner
status: docs-checked
description: "Control dead-link failures with ignoreDeadLinks: true, localhostLinks, or an array of strings, regexes and filter functions."
sources:
  - https://raw.githubusercontent.com/vuejs/vitepress/main/docs/en/reference/site-config.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`ignoreDeadLinks` (default `false`) controls whether dead links fail the build:

- `true`: never fail on dead links (use sparingly, it hides real errors).
- `'localhostLinks'`: still fail on dead links, but skip `localhost` ones (handy for docs that mention `http://localhost:5173`).
- an array of exact strings, regular expressions or functions `(link, source) => boolean`:

```ts
export default {
  ignoreDeadLinks: [
    '/playground',                    // exact url
    /^https?:\/\/localhost/,          // all localhost links
    /\/repl\//,                       // anything containing /repl/
    (url) => url.toLowerCase().includes('ignore')
  ]
}
```

Advice:

- Prefer the narrowest rule: whitelist the single link instead of turning checking off.
- The function form receives the source page as its second argument, so you can scope the exception to one document.

Verify: temporarily add a bad link and confirm the build fails.

## Checked

Read the `ignoreDeadLinks` entry in the site-config reference. Confirmed the type, default `false`, `true`, `'localhostLinks'`, and the array of strings, regexes and functions with its example. Removed unsourced advice about `public/` false positives, CI and `rewrites`, and the claim that the error lists the source page.

Method: docs-only read of cited pages, 2026-11-08
