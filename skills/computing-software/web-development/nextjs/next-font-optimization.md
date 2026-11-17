---
id: computing-software.web-development.nextjs.next-font-optimization
name: next-font-optimization
category: computing-software
field: web-development
product: nextjs
tags: [nextjs-optimization, nextjs-metadata, next-font, google-fonts-self-hosting, font-display, size-adjust, css-variable-fonts, local-fonts]
level: practitioner
status: verified
description: "Loading fonts with next/font: self-hosted Google and local fonts, subsets, variable fonts as CSS variables, Tailwind wiring and zero-CLS fallbacks."
sources:
  - https://nextjs.org/docs/app/api-reference/components/font
  - https://nextjs.org/docs/app/getting-started/fonts
  - https://web.dev/articles/css-size-adjust
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# next/font

**Goal:** fonts load from your own domain, early, with fallback metrics adjusted so swapping causes no layout shift.

## 1. Google fonts (downloaded at build, self-hosted)
```tsx
// app/fonts.ts
import { Inter, Roboto_Mono } from 'next/font/google';
export const inter = Inter({ subsets: ['latin'], display: 'swap', variable: '--font-sans' });
export const mono = Roboto_Mono({ subsets: ['latin'], weight: ['400', '700'], variable: '--font-mono' });   // Roboto Mono is variable too: weight is optional
// app/layout.tsx
<html lang="en" className={`${inter.variable} ${mono.variable}`}><body className="font-sans">…</body></html>
```
- No request to Google at runtime (ran: the page HTML had no `googleapis` reference and the CSS pointed at `/_next/static/media/*.woff2`; the files are fetched from Google at build time, so the build needs network access).
- Variable fonts (Inter, Roboto Mono, and Roboto in the 16.4.2 build, which compiled without `weight`) need no `weight`; fonts that are not variable require listing weights (per the font docs: the weight is required for non-variable fonts).
- `subsets` limits glyphs and controls what is preloaded.

## 2. Local fonts
```ts
import localFont from 'next/font/local';
export const brand = localFont({ src: [{ path: './Brand-Regular.woff2', weight: '400' }, { path: './Brand-Bold.woff2', weight: '700' }], variable: '--font-brand', display: 'swap' });
```

## 3. CLS
next/font generates a fallback `@font-face` using `size-adjust`/`ascent-override` so the fallback (Arial/Times) occupies the same space as the web font (`adjustFontFallback`, on by default). Ran: `@font-face{font-family:Inter Fallback;src:local(Arial);ascent-override:90.44%;descent-override:22.52%;line-gap-override:0.0%;size-adjust:107.12%}`. Keep it on.

## 4. Tailwind
Use a different CSS variable name for next/font than for the Tailwind token. The font docs' v4 pattern: next/font `variable: '--font-inter'`, then in CSS `@import 'tailwindcss'; @theme inline { --font-sans: var(--font-inter); }` (a token that points at a variable of the same name would be circular). v3: `theme.extend.fontFamily.sans = ['var(--font-inter)']`. With the first snippet above, rename `variable: '--font-sans'` to `'--font-inter'` to follow this.

## 5. Gotchas
- Call font loaders at module top level with literal options (they're compiled at build); you can't compute options at runtime.
- Each `Inter({...})` call in a different file creates another instance - define once and import.
- Fonts are preloaded only on the routes where the file that calls the font function is used (a page: that route; a layout: all routes under it; root layout: all routes), per the font docs; a font used everywhere belongs in the root layout.

## Verify
- [ ] Network: font files served from `/_next/static/media/`, no fonts.googleapis.com requests.
- [ ] CLS from font swap ≈ 0 (Performance panel layout shifts).
- [ ] Only needed subsets/weights downloaded.
