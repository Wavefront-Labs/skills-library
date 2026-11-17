---
id: computing-software.web-development.astro.server-endpoints-api-routes
name: server-endpoints-api-routes
category: computing-software
field: web-development
product: astro
tags: [api-routes, http-methods, server-endpoints, endpoint-redirect]
level: practitioner
status: docs-checked
description: "Build on-demand API routes in Astro: opt out of prerender, return status and headers, export per-method handlers and ALL, read the request body, and redirect."
sources:
  - https://raw.githubusercontent.com/withastro/docs/main/src/content/docs/en/guides/endpoints.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
With on-demand rendering the endpoint runs per request. Routes render on demand by default in `server` mode; in `static` mode add `export const prerender = false` per endpoint. Server endpoints read `params` without `getStaticPaths` and control status and headers:

```ts
export const GET = (async ({ params }) => {
  const id = params.id;
  const product = await getProduct(id);

  if (!product) {
    return new Response(null, {
      status: 404,
      statusText: "Not found",
    });
  }

  return new Response(JSON.stringify(product), {
    status: 200,
    headers: {
      "Content-Type": "application/json",
    },
  });
}) satisfies APIRoute;
```

Export a function per HTTP method (`GET`, `POST`, `DELETE`...). `ALL` matches any method without its own export; with no match the request redirects to your 404 page. Defining `GET` without `HEAD` makes Astro answer `HEAD` by calling `GET` and stripping the body.

```ts
export const ALL = (({ request }) => {
  return new Response(
    JSON.stringify({
      message: `This was a ${request.method}!`,
    }),
  );
}) satisfies APIRoute;
```

`request` is a full `Request`:

```ts
export const POST = (async ({ request }) => {
  if (request.headers.get("Content-Type") === "application/json") {
    const body = await request.json();
    return new Response(JSON.stringify({ message: "Your name was: " + body.name }), { status: 200 });
  }
  return new Response(null, { status: 400 });
}) satisfies APIRoute;
```

The context has `redirect()`: `return redirect(link, 307);`. Some providers require a `Content-Type` header for images.

## Checked

2026-11-04. Confirmed against the Astro endpoints guide: on-demand behaviour and prerender opt-out, params without getStaticPaths, status and headers, per-method exports, ALL, 404 redirect for unmatched methods, automatic HEAD handling, request body, redirect() with 307, Content-Type for images. Nothing removed.

Method: documentation only; no commands were run.
