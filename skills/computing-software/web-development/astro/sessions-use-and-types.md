---
id: computing-software.web-development.astro.sessions-use-and-types
name: sessions-use-and-types
category: computing-software
field: web-development
product: astro
tags: [astro-session, session-get-set, sessiondata, devalue]
level: practitioner
status: docs-checked
description: "Read and write session data via Astro.session or context.session in pages, endpoints, actions and middleware, and type it with App.SessionData."
sources:
  - https://raw.githubusercontent.com/withastro/docs/main/src/content/docs/en/guides/sessions.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The session object is `Astro.session` in components and pages, and `context.session` in endpoints, middleware and actions. It is created on first use; `session.regenerate()` and `session.destroy()` replace or end it. Most uses need only `session.get()` and `session.set()`. Sessions are not supported in edge middleware.

```astro
---
export const prerender = false; // Not needed with 'server' output
const cart = await Astro.session?.get('cart');
---

<a href="/checkout">🛒 {cart?.length ?? 0} items</a>
```

Endpoint:

```ts
import type { APIContext } from "astro";

export async function POST(context: APIContext) {
  const cart = await context.session?.get('cart') || [];
  const data = await context.request.json();
  if(!data?.item) {
    return new Response('Item is required', { status: 400 });
  }
  cart.push(data.item);
  await context.session?.set('cart', cart);
  return Response.json(cart);
}
```

Middleware:

```ts
export const onRequest = defineMiddleware(async (context, next) => {
  context.session?.set('lastVisit', new Date());
  return next();
});
```

Values are serialized with devalue (strings, numbers, `Date`, `Map`, `Set`, `URL`, arrays, plain objects). Optionally type the keys:

```ts title="src/env.d.ts"
declare namespace App {
  interface SessionData {
    user: {
      id: string;
      name: string;
    };
    cart: string[];
  }
}
```

This is type-checking only. Take care changing a type while users hold stored data, which could cause runtime errors.

## Checked

2026-11-04. Confirmed against the Astro sessions guide: Astro.session and context.session locations, regenerate and destroy, get and set, edge middleware note, devalue types, App.SessionData typing and runtime caution. Nothing removed.

Method: documentation only; no commands were run.
