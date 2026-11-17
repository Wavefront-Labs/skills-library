---
id: computing-software.web-development.nextjs.draft-mode-cms-previews
name: draft-mode-cms-previews
category: computing-software
field: web-development
product: nextjs
tags: [draft-mode, cms-preview, headless-cms, nextjs-preview, static-rendering, nextjs]
level: practitioner
status: verified
description: "Previewing unpublished CMS content in Next.js App Router with draftMode: secret-checked enable route, fetching drafts uncached, exiting preview, and security pitfalls."
sources:
  - https://nextjs.org/docs/app/guides/draft-mode
  - https://nextjs.org/docs/app/api-reference/functions/draft-mode
  - https://nextjs.org/docs/app/guides/caching
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Draft mode for CMS previews

Static pages are built from published content. Draft mode lets editors see unpublished changes on the real site: requests with the draft cookie render dynamically.

## 1. Enable route (called by the CMS "Preview" button)
```ts
// app/api/draft/route.ts
import { draftMode } from "next/headers";
import { redirect } from "next/navigation";
export async function GET(req: Request) {
  const { searchParams } = new URL(req.url);
  if (searchParams.get("secret") !== process.env.PREVIEW_SECRET) return new Response("Invalid token", { status: 401 });
  const slug = searchParams.get("slug") ?? "/";
  const page = await cms.getPage(slug, { preview: true });            // verify it exists
  if (!page) return new Response("Not found", { status: 404 });
  (await draftMode()).enable();                                          // sets the __prerender_bypass cookie
  redirect(page.path);                                                   // use the CMS path, not the raw param (open redirect)
}
```
CMS preview URL: `https://site.example.com/api/draft?secret=...&slug={entry.slug}`.

## 2. Read drafts in the page
```tsx
import { draftMode } from "next/headers";
export default async function Page({ params }: { params: Promise<{ slug: string }> }) {
  const { slug } = await params;
  const { isEnabled } = await draftMode();
  const page = await cms.getPage(slug, { preview: isEnabled, cache: isEnabled ? "no-store" : "force-cache" });
  return <Article page={page} preview={isEnabled} />;
}
```
Show a visible "Preview mode - exit" banner when enabled.

## 3. Exit route
```ts
// app/api/draft/disable/route.ts
export async function GET() { (await draftMode()).disable(); return new Response(null, { status: 307, headers: { Location: "/" } }); }
```

## 4. Pitfalls
- Keep `PREVIEW_SECRET` server-side; rotate if leaked. Do not expose draft API tokens with `NEXT_PUBLIC_`.
- CDNs must not cache draft responses: the bypass cookie makes Next send `no-store`, but custom CDN rules that ignore cookies can leak drafts.
- Live preview (instant updates while editing) needs the CMS SDK's client-side listener on top of draft mode.
- On-demand revalidation (`revalidateTag` via CMS webhook) is separate: it updates the published static pages after publish.

Checked on a Next 16.4.2 production build: a wrong secret returns 401; the enable route answers 307 with `Set-Cookie: __prerender_bypass=...; HttpOnly; Secure; SameSite=None`; a request carrying that cookie renders the draft branch with `Cache-Control: private, no-cache, no-store`, while a request without it still gets the cached static page (`x-nextjs-cache: HIT`). `draftMode()` is async since v15.0.0-RC and does not make the route dynamic by itself. Draft Mode is unsupported with `output: "export"` (static-exports guide).

## Verify
- [ ] Preview button shows unpublished edits; a normal browser session still sees published content; wrong secret returns 401.
