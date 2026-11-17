---
id: computing-software.web-development.sveltekit.sveltekit-seo
name: sveltekit-seo
category: computing-software
field: web-development
product: sveltekit
tags: [sveltekit, seo, sitemap, meta, title, ssr, trailing-slash]
level: intro
status: docs-checked
description: "Apply SvelteKit SEO basics: keep SSR on, set unique title and meta description per page, and serve a dynamic sitemap.xml from a +server.js endpoint."
sources:
  - https://github.com/sveltejs/kit/blob/main/documentation/docs/40-best-practices/20-seo.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# SvelteKit SEO

Quality, widely-linked content matters most; the rest is technical.

## Defaults that help

- SSR: server-rendered content is indexed more frequently and reliably than client-rendered. It is on by default; you can disable it in `handle`, but should leave it on unless you have a good reason. Dynamic rendering is possible but not generally recommended.
- Performance: Core Web Vitals affect ranking. Use the default hybrid rendering, optimize images, and measure with PageSpeed Insights or Lighthouse.
- Normalized URLs: SvelteKit redirects pathnames with trailing slashes to ones without (or the reverse, per the `trailingSlash` page option), avoiding duplicate URLs.

## Per-page title and description

Every page needs a unique, well-written `<title>` and `<meta name="description">` inside `<svelte:head>`. A common pattern: return SEO data from page `load` functions and render it from `page.data` in a `<svelte:head>` in your root layout.

## Sitemap

Create it dynamically with an endpoint at `src/routes/sitemap.xml/+server.js`:

```js
export async function GET() {
	return new Response(
		`
		<?xml version="1.0" encoding="UTF-8" ?>
		<urlset
			xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"
			xmlns:xhtml="http://www.w3.org/1999/xhtml"
			xmlns:mobile="http://www.google.com/schemas/sitemap-mobile/1.0"
			xmlns:news="http://www.google.com/schemas/sitemap-news/0.9"
			xmlns:image="http://www.google.com/schemas/sitemap-image/1.1"
			xmlns:video="http://www.google.com/schemas/sitemap-video/1.1"
		>
			<!-- <url> elements go here -->
		</urlset>`.trim(),
		{
			headers: {
				'Content-Type': 'application/xml'
			}
		}
	);
}
```

Fill in the `<url>` elements for your pages. Sitemaps help search engines prioritize pages, especially on large sites.

## Checked

Checked 2026-11-07.

Method: documentation only; no commands were run.

Read 40-best-practices/20-seo.md in full: SSR, rendering, Core Web Vitals, URLs, title and meta, sitemap. No claims trimmed.
