---
id: computing-software.web-development.nextjs.internationalised-routing-with-locale-segment
name: internationalised-routing-with-locale-segment
category: computing-software
field: web-development
product: nextjs
tags: [nextjs-i18n, i18n-routing, locale-segment, next-intl, localisation]
level: practitioner
status: docs-checked
description: "Internationalised routing in the Next.js App Router: a [lang] segment, locale detection in middleware, static params per locale, dictionaries or next-intl, hreflang and SEO."
sources:
  - https://nextjs.org/docs/app/guides/internationalization
  - https://next-intl.dev/docs/getting-started/app-router
  - https://developers.google.com/search/docs/specialty/international/localized-versions
  - https://nextjs.org/docs/app/api-reference/file-conventions/proxy
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Internationalised routing with a locale segment

The App Router has no built-in i18n config (that was Pages Router `i18n` in next.config). You build it with a dynamic segment and a proxy (called middleware before Next 16).

## 1. Structure
```
app/[lang]/layout.tsx
app/[lang]/page.tsx
app/[lang]/products/[slug]/page.tsx
proxy.ts                  (middleware.ts before Next 16)
```
```tsx
// app/[lang]/layout.tsx
export const locales = ["en", "de", "fr"] as const;
export async function generateStaticParams() { return locales.map(lang => ({ lang })); }
export const dynamicParams = false;                 // unknown locales -> 404
export default async function Layout({ children, params }: { children: React.ReactNode; params: Promise<{ lang: string }> }) {
  const { lang } = await params;
  return <html lang={lang} dir={lang === "ar" ? "rtl" : "ltr"}><body>{children}</body></html>;
}
```

## 2. Locale detection
```ts
// proxy.ts (middleware.ts before Next 16)
import { NextResponse, type NextRequest } from "next/server";
import Negotiator from "negotiator"; import { match } from "@formatjs/intl-localematcher";
const locales = ["en", "de", "fr"], defaultLocale = "en";
export function proxy(req: NextRequest) {   // named `middleware` before Next 16
  const { pathname } = req.nextUrl;
  if (locales.some(l => pathname === `/${l}` || pathname.startsWith(`/${l}/`))) return;
  const cookie = req.cookies.get("NEXT_LOCALE")?.value;
  const langs = new Negotiator({ headers: { "accept-language": req.headers.get("accept-language") ?? "" } }).languages();
  const locale = cookie && locales.includes(cookie) ? cookie : match(langs, locales, defaultLocale);
  req.nextUrl.pathname = `/${locale}${pathname}`;
  return NextResponse.redirect(req.nextUrl);
}
export const config = { matcher: ["/((?!api|_next|.*\\..*).*)"] };
```
Honour an explicit user choice (a cookie of your own naming) over `Accept-Language`.

## 3. Translations
- Simple: per-locale JSON dictionaries loaded in Server Components with `import(`./dictionaries/${lang}.json`)` - zero client JS.
- Full-featured: a library such as **next-intl** (one of several i18n libraries listed in the Next.js docs).
- Format dates/numbers with `Intl` using the route locale, not the server's.

## 4. SEO
```tsx
export async function generateMetadata({ params }) {
  const { lang } = await params;
  return { alternates: { canonical: `/${lang}`, languages: { en: "/en", de: "/de", fr: "/fr", "x-default": "/en" } } };
}
```
Per Google's localized-versions guide, each language version must list itself and all other versions, the annotations must be reciprocal or they are ignored, and `x-default` is the fallback for users who match no version. Map translated slugs in a table if you localise URLs.

## Verify
- [ ] `/` redirects to the preferred locale; switching language persists via cookie; each locale page statically generated; hreflang tags present and reciprocal.

## Checked
Date: 2026-10-25. Documentation: Next.js documentation source (vercel/next.js canary, commit of 2026-10-24; latest release v16.4.3) (guides/internationalization, file-conventions/proxy, generate-static-params, generate-metadata) and Google Search Central localized-versions guide (fetched 2026-10-25).
Confirmed: `[lang]` segment with `generateStaticParams`, `dynamicParams = false` returns 404 for ungenerated params, Negotiator plus `@formatjs/intl-localematcher` locale matching, `alternates.languages` metadata output, middleware renamed to proxy in Next 16, hreflang reciprocity, self-listing and `x-default`.
Corrected or removed: the middleware file name for Next 16, the `NEXT_LOCALE` cookie name implication, the unsupported IP-geolocation redirect advice, the unconfirmed next-intl feature list and the "self-referencing canonical" advice.
Method: documentation only; no commands were run.
