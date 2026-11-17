---
id: computing-software.web-development.react.list-virtualization
name: list-virtualization
category: computing-software
field: web-development
product: react
tags: [list-virtualization, tanstack-virtual, react-window, windowing, large-lists, react]
level: practitioner
status: docs-checked
description: "Rendering huge lists with virtualisation: TanStack Virtual setup, dynamic row measurement, window scrolling, accessibility and find-in-page trade-offs, and alternatives."
sources:
  - https://tanstack.com/virtual/latest/docs/introduction
  - https://tanstack.com/virtual/latest/docs/api/virtualizer
  - https://tanstack.com/virtual/latest/docs/framework/react/react-virtual
  - https://react-window.vercel.app/
  - https://github.com/bvaughn/react-window
  - https://developer.mozilla.org/en-US/docs/Web/CSS/content-visibility
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# List virtualization

Render only rows in (and near) the viewport; thousands of rows stay cheap to render and update.

## 1. TanStack Virtual
```tsx
import { useVirtualizer } from "@tanstack/react-virtual";
function Rows({ rows }: { rows: Row[] }) {
  const parentRef = useRef<HTMLDivElement>(null);
  const v = useVirtualizer({ count: rows.length, getScrollElement: () => parentRef.current, estimateSize: () => 48, overscan: 8 });
  return (
    <div ref={parentRef} style={{ height: 600, overflow: "auto" }}>
      <div style={{ height: v.getTotalSize(), position: "relative" }}>
        {v.getVirtualItems().map(item => (
          <div key={rows[item.index].id} data-index={item.index} ref={v.measureElement}
               style={{ position: "absolute", top: 0, left: 0, width: "100%", transform: `translateY(${item.start}px)` }}>
            <RowView row={rows[item.index]} />
          </div>
        ))}
      </div>
    </div>
  );
}
```
- `measureElement` + `data-index` handles variable row heights; a good `estimateSize` reduces scroll jumps.
- `useWindowVirtualizer` when the page itself scrolls.
- Horizontal lists use the `horizontal` option; grids use one virtualizer per axis.
- react-window (2.x) is an alternative with a different API (`List` and `Grid` components); see its documentation site.

## 2. Trade-offs
- Ctrl+F only finds rendered rows; offer in-app search.
- Screen readers see a partial list: set `role="list"`/`grid` with `aria-setsize` and `aria-posinset` (or `aria-rowcount`/`aria-rowindex`) so position is announced.
- Keyboard focus on a row that scrolls out gets unmounted; keep focus management in state and scroll the focused index into view (`v.scrollToIndex`).
- Print and anchor links do not see unrendered content.

## 3. Alternatives first
Pagination or "load more"; `content-visibility: auto` keeps all DOM but skips the contents of elements that are not relevant to the user; server-side filtering.

## Verify
- [ ] Scrolling 10k rows stays at 60 fps on a mid-range phone; DOM contains only ~visible + overscan rows; screen reader announces "row 532 of 10000".

## Checked

Checked 2026-10-25 against the TanStack Virtual docs (virtualizer API, React adapter), the react-window repository (2.5.0, released 2026-10-22) and MDN content-visibility. Confirmed: `useVirtualizer` and `useWindowVirtualizer`; options `count`, `getScrollElement`, `estimateSize`, `overscan`, `horizontal`, `measureElement`; methods `getVirtualItems`, `getTotalSize`, `scrollToIndex`; the React example uses `data-index` with `measureElement`; react-window 2.x exposes List and Grid; `content-visibility: auto` skips contents when the element is not relevant to the user. Replaced the web.dev source (a react-window 1.x article) with the react-window docs site. Removed the SEO claim and the "few hundred items" threshold.

Method: documentation only; no commands were run.
