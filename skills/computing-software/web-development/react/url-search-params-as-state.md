---
id: computing-software.web-development.react.url-search-params-as-state
name: url-search-params-as-state
category: computing-software
field: web-development
product: react
tags: [react, url-search-params-state, usesearchparams, nuqs, deep-linking, filters, react-router, nextjs, web-development]
level: practitioner
status: docs-checked
description: "Keeping shareable UI state (filters, sort, page, tabs) in the URL with useSearchParams, history replace vs push, parsing defaults and debounced inputs."
sources:
  - https://developer.mozilla.org/en-US/docs/Web/API/URLSearchParams
  - https://reactrouter.com/api/hooks/useSearchParams
  - https://nextjs.org/docs/app/api-reference/functions/use-search-params
  - https://nextjs.org/docs/app/api-reference/file-conventions/page
  - https://nextjs.org/docs/app/api-reference/functions/use-router
  - https://github.com/47ng/nuqs
  - https://zod.dev/api
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# URL search params as state

**Goal:** filters, sorting, pagination and selected tabs survive reloads, back/forward and sharing.

## 1. What belongs in the URL
Put it there if a user would expect a copied link to reproduce the view: search query, filters, sort, page, active tab, selected item id. Keep transient UI (hover, open dropdown, unsaved form text) in component state.

## 2. React Router
```jsx
const [params, setParams] = useSearchParams();
const page = Number(params.get("page") ?? 1);
const sort = params.get("sort") ?? "newest";

function setSort(next) {
  setParams(p => { p.set("sort", next); p.delete("page"); return p; }, { replace: true });
}
```
The function form does not queue like React's `setState`: several calls in the same tick do not build on each other, so make one combined update.

## 3. Next.js App Router
```tsx
"use client";
const params = useSearchParams(); const router = useRouter(); const pathname = usePathname();
function update(key: string, value: string) {
  const next = new URLSearchParams(params);
  value ? next.set(key, value) : next.delete(key);
  router.replace(`${pathname}?${next}`, { scroll: false });
}
```
Server components read the page `searchParams` prop, a Promise in current Next.js (`const { q } = await searchParams`). Next.js recommends wrapping a client component that uses `useSearchParams` in `<Suspense>`: in a prerendered route the tree up to the nearest Suspense boundary renders on the client.

## 4. Parse at the boundary
URL values are untrusted strings. Validate and default:
```ts
const Sort = z.enum(["newest", "price"]).catch("newest");
const sort = Sort.parse(params.get("sort"));
```
Libraries like `nuqs` give built-in typed parsers and have adapters for Next.js, React Router and other routers.

## 5. push vs replace
- `replace` for typing in a search box and tweaking filters (don't flood history).
- `push` for deliberate navigation-like changes (page 2, opening an item) so Back works.
Debounce text inputs before writing to the URL; keep the input itself controlled by local state so typing stays smooth.

## 6. Keep the URL canonical
Delete params equal to their default, keep a stable key order if the URL is a cache key, and reset `page` when filters change.

## Verify
- [ ] Reload and copy-paste the URL reproduce the exact view.
- [ ] Back button steps through meaningful states, not every keystroke.
- [ ] Garbage params (`?page=abc&sort=x`) fall back to defaults without crashing.

## Checked

Checked 2026-10-25 against the React Router docs and source (react-router 8.5.0), the Next.js docs (16.4.3) and the nuqs README. Confirmed: `useSearchParams` returns `[searchParams, setSearchParams]`, accepts a function updater and a second `NavigateOptions` argument with `replace`; the function form does not queue; Next.js `searchParams` page prop is a Promise; `useSearchParams` Suspense behaviour in prerendered routes; `router.replace(href, { scroll })`; `new URLSearchParams(searchParams)` pattern; nuqs supports Next.js, React Router, Remix and TanStack Router with built-in parsers; zod `.catch()` fallbacks. Removed the "Next 15+" version claim, the 300 ms figure and the nuqs batching claim.

Method: documentation only; no commands were run.
