---
id: computing-software.web-development.astro.dynamic-redirects-astro-redirect
name: dynamic-redirects-astro-redirect
category: computing-software
field: web-development
product: astro
tags: [astro-redirect, login-redirect, html-streaming, page-level]
level: practitioner
status: docs-checked
description: "Redirect users at request time with Astro.redirect, such as sending logged-out visitors to a login page, and why it must run at page level."
sources:
  - https://raw.githubusercontent.com/withastro/docs/main/src/content/docs/en/guides/routing.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`Astro.redirect()` redirects to another page dynamically, for example after checking a session in a cookie:

```astro title="src/pages/account.astro"
---
import { isLoggedIn } from "../utils";

const cookie = Astro.request.headers.get("cookie");

// If the user is not logged in, redirect them to the login page
if (!isLoggedIn(cookie)) {
  return Astro.redirect("/login");
}
---
```

Because Astro uses HTML streaming in on-demand rendering, redirects must be done at the page level, not inside child components.

Use a redirect (rather than a rewrite) for content that has permanently moved, or to direct a user to a page with a new URL such as a dashboard after login. Permanent moves can instead be declared in the `redirects` config.

## Checked

2026-11-04. Confirmed against the Astro routing guide: Astro.redirect example and the page-level restriction caused by HTML streaming. Softened an unsupported 'prefer' statement about the redirects config.

Method: documentation only; no commands were run.
