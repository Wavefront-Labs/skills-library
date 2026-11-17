---
id: computing-software.web-development.react.data-grids-with-tanstack-table
name: data-grids-with-tanstack-table
category: computing-software
field: web-development
product: react
tags: [tanstack-table, data-grids, headless-table, sorting-filtering, react]
level: practitioner
status: docs-checked
description: "Data grids with TanStack Table: column definitions, sorting, filtering and pagination client or server side, selection, virtualisation and accessible markup."
sources:
  - https://tanstack.com/table/latest/docs/framework/react/quick-start
  - https://tanstack.com/table/latest/docs/framework/react/guide/pagination
  - https://tanstack.com/table/latest/docs/framework/react/guide/sorting
  - https://tanstack.com/table/latest/docs/framework/react/guide/row-selection
  - https://tanstack.com/table/latest/docs/framework/react/guide/migrating
  - https://tanstack.com/table/latest/docs/framework/react/guide/virtualization
  - https://www.w3.org/WAI/ARIA/apg/patterns/table/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Data grids with TanStack Table

TanStack Table is headless: it computes rows, sorting, filtering, grouping and pagination; you render the `<table>`. This skill uses the v9 API (`@tanstack/react-table` 9.x, current in October 2026). v8 code uses `useReactTable` and `getCoreRowModel()`; the migration guide covers the move and a deprecated `useLegacyTable` shim exists for incremental upgrades.

## 1. Setup
```tsx
import { createSortedRowModel, rowSortingFeature, sortFns, tableFeatures, useTable } from "@tanstack/react-table";
import type { ColumnDef } from "@tanstack/react-table";

const features = tableFeatures({
  rowSortingFeature,                       // enables sorting state and APIs
  sortedRowModel: createSortedRowModel(),  // client-side sorting
  sortFns,
});
const columns: Array<ColumnDef<typeof features, Order>> = [
  { accessorKey: "id", header: "Order" },
  { accessorKey: "customer", header: "Customer" },
  { accessorKey: "total", header: "Total", cell: i => fmt.format(i.getValue<number>()), sortFn: "basic" },
];
const table = useTable({ key: "orders", features, columns, data });
```
Features are opt-in: register only the ones you use (`rowPaginationFeature`, `rowSelectionFeature` and so on) on `tableFeatures`. `data` and `columns` must be **stable references** (module scope, `useState`, a query result); new arrays each render cause repeated recalculation.

## 2. Render with accessible sorting
```tsx
<table>
  <caption>Recent orders</caption>
  <thead>{table.getHeaderGroups().map(hg => <tr key={hg.id}>{hg.headers.map(h => (
    <th key={h.id} scope="col" aria-sort={({ asc: "ascending", desc: "descending" } as const)[h.column.getIsSorted() as string] ?? "none"}>
      <button onClick={h.column.getToggleSortingHandler()}><table.FlexRender header={h} /></button>
    </th>))}</tr>)}</thead>
  <tbody>{table.getRowModel().rows.map(r => <tr key={r.id}>{r.getAllCells().map(c =>
    <td key={c.id}><table.FlexRender cell={c} /></td>)}</tr>)}</tbody>
</table>
```
Use a real `<table>`; `role="grid"` with arrow-key cell navigation only for spreadsheet-like editing.

## 3. Server-side data
```ts
useTable({ key: "orders", features, columns, data: page.rows, rowCount: page.total,
  manualPagination: true, manualSorting: true, manualFiltering: true,
  state: { pagination, sorting, columnFilters },
  onPaginationChange: setPagination, onSortingChange: setSorting, onColumnFiltersChange: setColumnFilters });
```
`features` here also registers `rowPaginationFeature` (and the filtering feature if used). With `manual*` options the table assumes `data` is already paginated, sorted and filtered; give it `rowCount` (or `pageCount`) so it knows the total. Fetch with TanStack Query keyed on `[pagination, sorting, columnFilters]` and `placeholderData: keepPreviousData` to avoid flashing. v9 also supports owning a state slice through an external atom (`atoms` option); the v8-style `state` plus `onXChange` pattern remains supported. Keep table state in the URL for shareable views.

## 4. Large data
Client-side row models still render every row you show, so DOM size is the cost. Virtualise rows with `useVirtualizer` from `@tanstack/react-virtual` (the table owns rows and columns, the virtualizer owns scroll indexes and measurement), or paginate.

## 5. Features
Row selection (`rowSelectionFeature`, `enableRowSelection`, `getRowId` for stable ids, `row.getToggleSelectedHandler()` and `row.getIsSelected()` for checkboxes labelled like "Select order 1042"), column visibility, resizing, pinning, grouping and faceting are each their own opt-in feature with a guide in the docs.

## Verify
- [ ] Sorting announced via aria-sort; data/columns memoised (no runaway renders in Profiler); server mode requests one page at a time; 10k-row view scrolls smoothly with virtualisation.

## Checked

Checked 2026-10-25 against the TanStack Table repository docs (main branch, @tanstack/react-table 9.3.1 released 2026-10-12). The skill previously showed the v8 API (`useReactTable`, `getCoreRowModel`, `createColumnHelper`); the setup, rendering, server-side and selection sections are rewritten to the documented v9 API. Confirmed: `useTable`, `tableFeatures`, `rowSortingFeature`, `createSortedRowModel`, `sortFns`, `table.FlexRender`, `getToggleSortingHandler`, `getIsSorted`; `rowPaginationFeature`, `manualPagination`, `manualSorting`, `manualFiltering`, `rowCount` and `pageCount`; the `basic` built-in sort function; `rowSelectionFeature`, `enableRowSelection`, `getRowId`, `getToggleSelectedHandler`; stable data references; `useVirtualizer` from `@tanstack/react-virtual`; `placeholderData: keepPreviousData`; v8-style `state` plus `onXChange` still supported. Removed the unconfirmed "10k-50k rows" figure, the sticky-header advice and the `aria-sort` rationale beyond the APG table pattern link.

Method: documentation only; no commands were run.
