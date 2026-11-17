---
id: computing-software.web-development.nextjs.metadata-sitemap-robots-og-images
name: metadata-sitemap-robots-og-images
category: computing-software
field: web-development
product: nextjs
tags: [nextjs-optimization, nextjs-metadata, generatemetadata, og-images, sitemap-xml, robots-txt, metadata-api, seo, imageresponse]
level: practitioner
status: verified
description: "Next.js Metadata API: static and generateMetadata, title templates, canonical/alternates, sitemap.ts and robots.ts, and dynamic OG images with ImageResponse."
sources:
  - https://nextjs.org/docs/app/getting-started/metadata-and-og-images
  - https://nextjs.org/docs/app/api-reference/functions/generate-metadata
  - https://nextjs.org/docs/app/api-reference/file-conventions/metadata/sitemap
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Metadata, sitemap, robots and OG images

**Goal:** every route has correct title, description, canonical and social cards, and crawlers get a sitemap and robots rules - generated from data, not hand-maintained.

## 1. Static and dynamic metadata
```tsx
// app/layout.tsx
export const metadata = {
  metadataBase: new URL('https://www.example.com'),
  title: { template: '%s | Example', default: 'Example' },
  description: 'Project tracking for small teams',
  openGraph: { siteName: 'Example', type: 'website' },
};
// app/blog/[slug]/page.tsx
export async function generateMetadata({ params }) {
  const { slug } = await params;                  // params is a Promise in Next 15+
  const post = await getPost(slug);                // fetch is deduped with the page's own call (or use React cache())
  if (!post) return {};
  return { title: post.title, description: post.excerpt, alternates: { canonical: `/blog/${slug}` },
           openGraph: { type: 'article', publishedTime: post.date } };
}
```
- `metadataBase` makes relative OG/canonical URLs absolute - without it you get build warnings and broken social cards.
- Metadata is merged from layouts to pages (shallow per key: a page `openGraph` replaces the layout's whole `openGraph` object; ran: with layout `siteName` and a page `openGraph: { type: 'article' }` the output had `og:type=article` and no `og:site_name`). `og:title` and `twitter:*` tags are derived from `title`/`description` automatically (ran), and a page `title` goes through the layout's `title.template`.

## 2. Sitemap and robots
```ts
// app/sitemap.ts
export default async function sitemap() {
  const posts = await getAllPosts();
  return [{ url: 'https://www.example.com', lastModified: new Date() },
          ...posts.map(p => ({ url: `https://www.example.com/blog/${p.slug}`, lastModified: p.updatedAt }))];
}
// app/robots.ts
export default function robots() {
  return { rules: [{ userAgent: '*', allow: '/', disallow: ['/admin', '/api'] }], sitemap: 'https://www.example.com/sitemap.xml' };
}
```
Large sites: `generateSitemaps()` to split (the docs example uses Google's limit of 50,000 URLs per sitemap). Ran: `sitemap.ts` produced `/sitemap.xml` with `<lastmod>` as ISO strings for `Date` values and the raw string otherwise, and `robots.ts` produced `User-Agent: *`, `Allow: /`, `Disallow: /admin`, `Disallow: /api` and the `Sitemap:` line.

## 3. OG images
`app/blog/[slug]/opengraph-image.tsx` exporting a default function that returns `new ImageResponse(<div style={{…}}>{post.title}</div>, { width: 1200, height: 630 })` (from `next/og`). Uses Satori: flexbox subset of CSS, custom fonts loaded as ArrayBuffer, no CSS grid. The docs say generated images are statically optimised (built at build time and cached) unless they use request-time APIs or dynamic config. Ran on 16.4.2: `app/og/[slug]/opengraph-image.tsx` (reads `params`, no `generateStaticParams` of its own) showed as a dynamic route (`ƒ`) in the build table and answered `cache-control: public, max-age=0, must-revalidate` with `image/png`; the page's meta tags pointed at it with absolute URLs via `metadataBase`, `og:image:width` 1200 and `og:image:height` 630. `ImageResponse` limits per the docs: flexbox and a subset of CSS (no `display: grid`), 500KB bundle, `ttf`/`otf`/`woff` fonts only.

## 4. Pitfalls
- Non-production deploys should send `noindex` (`robots: { index: false }` based on env) so previews don't get indexed.
- Streaming metadata: Next may stream `generateMetadata` results for human visitors but blocks for bots - slow metadata fetches still delay crawlers.

## Verify
- [ ] View source: one `<title>`, description, canonical, og:* and twitter:* per route.
- [ ] `/sitemap.xml` and `/robots.txt` valid; preview deployments are noindex.
- [ ] Social card validators (opengraph.xyz, LinkedIn Post Inspector) render the image.
