---
id: computing-software.web-development.nextjs.after-for-post-response-work
name: after-for-post-response-work
category: computing-software
field: web-development
product: nextjs
tags: [nextjs-after, background-work, post-response, logging, serverless]
level: practitioner
status: verified
description: "Using after() in Next.js to run logging, analytics and cache warming after the response is sent: where it works, reading request data, platform waitUntil support and limits."
sources:
  - https://nextjs.org/docs/app/api-reference/functions/after
  - https://vercel.com/docs/functions/functions-api-reference/vercel-functions-package#waituntil
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# after() for post-response work

`after()` (stable since Next.js 15.1) schedules work to run after the response finishes streaming, so it doesn't add latency for the user.

## 1. Usage
```ts
import { after } from "next/server";
import { cookies, headers } from "next/headers";

export default async function Page({ params }) {
  const { slug } = await params;
  const post = await getPost(slug);
  after(async () => {
    const ua = (await headers()).get("user-agent");
    await analytics.track("post_view", { slug, ua });     // runs after the page is sent
  });
  return <Article post={post} />;
}
```
Works in Server Components (including `generateMetadata`), Server Functions, Route Handlers and Proxy (the Next 16 name for middleware). Checked against the 16.4.2 docs shipped in the `next` package and by running a production build.

## 2. Rules
- In **Server Actions and Route Handlers** you can call `cookies()`/`headers()` inside the `after` callback. In **Server Components**, read request APIs *before* `after()` and close over the values. Calling them inside the callback throws (ran on 16.4.2: `Route /x used headers() inside after() while rendering. This is not supported`), because Next must know which part of the tree reads request data.
- `after()` is not a dynamic API: using it doesn't make a page dynamic. In static pages it runs at build/revalidation time.
- Runs even if the response errors or `notFound()`/`redirect()` is called (ran: a page that called `notFound()` still logged its `after` callback).
- Can be nested inside other `after` calls. In Server Components, React `cache()` dedupes work done inside the callback.

## 3. Platform support
Execution continues past the response only where the runtime allows it:
- Vercel: uses `waitUntil` under the hood; `after` runs for the platform's default or configured max duration (`maxDuration` segment config).
- Self-hosted `next start`: supported (process keeps running).
- Docker container and Node server: supported. Static export (`output: "export"`): not supported.
- Other serverless hosts: provide a `waitUntil` on `globalThis[Symbol.for('@next/request-context')]` (the docs show the exact object shape); otherwise work may be cut off when the function freezes.

## 4. What to use it for
Good: logging, analytics, audit trails, cache warming, sending non-critical webhooks, revalidating related paths.
Not for: work the user must know succeeded (payments, emails that must send) - use a durable queue (Inngest, QStash, SQS, a job table) so failures are retried.

## Verify
- [ ] TTFB unchanged by the work moved into after(); logs show callbacks executing in production; critical tasks go through a queue, not after().
