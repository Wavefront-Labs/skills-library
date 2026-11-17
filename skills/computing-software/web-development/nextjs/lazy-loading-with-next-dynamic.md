---
id: computing-software.web-development.nextjs.lazy-loading-with-next-dynamic
name: lazy-loading-with-next-dynamic
category: computing-software
field: web-development
product: nextjs
tags: [next-dynamic, lazy-loading, code-splitting, ssr-false, nextjs]
level: practitioner
status: verified
description: "Lazy loading in Next.js with next/dynamic: client-only components with ssr false, loading fallbacks, named exports, loading on interaction, and RSC rules."
sources:
  - https://nextjs.org/docs/app/guides/lazy-loading
  - https://react.dev/reference/react/lazy
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Lazy loading with next/dynamic

## 1. Basic use (Client Components)
```tsx
"use client";
import dynamic from "next/dynamic";
const Chart = dynamic(() => import("@/components/chart"), { loading: () => <ChartSkeleton /> });
const Map = dynamic(() => import("@/components/map"), { ssr: false });            // browser-only lib (leaflet, window)
const Editor = dynamic(() => import("@/components/editor").then(m => m.Editor));  // named export
```
- Creates a separate chunk loaded when the component first renders.
- `ssr: false` skips server rendering entirely - only allowed inside Client Components in the App Router. Use it for libraries that touch `window`/`document` at import time.
- Give the skeleton the same dimensions as the final component to avoid CLS.

## 2. Load on interaction
```tsx
const [show, setShow] = useState(false);
const Comments = dynamic(() => import("./comments"));
<button onClick={() => setShow(true)} onMouseEnter={() => import("./comments")}>Show comments</button>
{show && <Comments />}
```
Preloading the import on hover/focus hides the latency. For non-components, `const { parse } = await import("heavy-lib")` inside the handler.

## 3. Server Components
- Server Components are already code-split and don't ship JS; `dynamic()` of a Server Component only splits its Client Component children.
- `ssr: false` cannot be used in a Server Component - ran on 16.4.2: the build fails with ``ssr: false` is not allowed with `next/dynamic` in Server Components. Please move it into a Client Component.` Wrap it in a small client component that does the dynamic import.

## 4. What to lazy load
Charts, maps, rich text editors, video players, date pickers, modals' content, admin-only tools, anything below the fold or behind interaction. Not the LCP element or above-the-fold content (adds a round trip).

## 5. Verify the split
`npx next analyze` (Turbopack, Next 16.1+) or `ANALYZE=true next build --webpack` with `@next/bundle-analyzer` should show the heavy library in its own chunk, not in the page's First Load JS. The old `--experimental-analyze` flag is not in `next build --help` on 16.4.2, and `@next/bundle-analyzer` produces no report under the default Turbopack build.

## Verify
- [ ] First Load JS for the route drops by the size of the lazy component; skeleton matches layout (no CLS); browser-only libs don't break the server render.
