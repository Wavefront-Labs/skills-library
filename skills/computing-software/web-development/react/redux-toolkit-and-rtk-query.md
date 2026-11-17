---
id: computing-software.web-development.react.redux-toolkit-and-rtk-query
name: redux-toolkit-and-rtk-query
category: computing-software
field: web-development
product: react
tags: [redux-toolkit, rtk-query, createslice, configurestore, cache-tags, react]
level: practitioner
status: docs-checked
description: "Modern Redux with Redux Toolkit: configureStore, createSlice with Immer, typed hooks, memoised selectors, and RTK Query endpoints with cache tags and invalidation."
sources:
  - https://redux-toolkit.js.org/introduction/getting-started
  - https://redux-toolkit.js.org/rtk-query/overview
  - https://redux-toolkit.js.org/api/getDefaultMiddleware
  - https://redux-toolkit.js.org/rtk-query/api/setupListeners
  - https://redux-toolkit.js.org/rtk-query/usage/manual-cache-updates
  - https://redux.js.org/usage/usage-with-typescript
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Redux Toolkit and RTK Query

Use Redux when many distant components share complex client state with traceable updates (editors, dashboards, offline queues). For server data alone, RTK Query or TanStack Query; for small global state, Zustand or context.

## 1. Store and slice
```ts
import { configureStore, createSlice, type PayloadAction } from "@reduxjs/toolkit";
const cart = createSlice({
  name: "cart",
  initialState: { items: [] as { id: string; qty: number }[] },
  reducers: {
    added(state, a: PayloadAction<string>) {             // Immer: "mutating" code is safe here
      const it = state.items.find(i => i.id === a.payload);
      it ? it.qty++ : state.items.push({ id: a.payload, qty: 1 });
    },
    removed(state, a: PayloadAction<string>) { state.items = state.items.filter(i => i.id !== a.payload); },
  },
});
export const { added, removed } = cart.actions;
export const store = configureStore({ reducer: { cart: cart.reducer, [api.reducerPath]: api.reducer },
  middleware: gDM => gDM().concat(api.middleware) });
export type RootState = ReturnType<typeof store.getState>;
export const useAppSelector = useSelector.withTypes<RootState>();
export const useAppDispatch = useDispatch.withTypes<typeof store.dispatch>();
```
`configureStore` adds DevTools, thunk, and development-only checks for mutations and non-serialisable values. `api` is the RTK Query service from section 3; define it first or import it into the store file.

## 2. Selectors
Select the smallest slice; derive with `createSelector` so components re-render only when inputs change:
```ts
const selectTotal = createSelector([(s: RootState) => s.cart.items], items => items.reduce((n, i) => n + i.qty, 0));
```
Returning new objects/arrays from `useSelector` without memoisation re-renders on every store update.

## 3. RTK Query
```ts
export const api = createApi({
  baseQuery: fetchBaseQuery({ baseUrl: "/api" }),
  tagTypes: ["Post"],
  endpoints: b => ({
    getPosts: b.query<Post[], void>({ query: () => "posts",
      providesTags: r => [...(r ?? []).map(p => ({ type: "Post" as const, id: p.id })), { type: "Post", id: "LIST" }] }),
    addPost: b.mutation<Post, Partial<Post>>({ query: body => ({ url: "posts", method: "POST", body }),
      invalidatesTags: [{ type: "Post", id: "LIST" }] }),
  }),
});
export const { useGetPostsQuery, useAddPostMutation } = api;
```
Handles caching, dedupe, refetch on focus/reconnect (`setupListeners`), polling, optimistic updates (`onQueryStarted` + `updateQueryData`).

## Gotchas
- Do not put server data in slices and also in RTK Query: one source of truth.
- Keep state serialisable (no class instances, Dates as ISO strings).

## Verify
- [ ] Redux DevTools shows readable actions; adding a post refetches the list via tag invalidation.

## Checked

Checked 2026-10-25 against the Redux Toolkit docs (RTK 2.13.0, 2026-09-29) and the Redux and React Redux docs. Confirmed: `configureStore` with a middleware callback and `.concat(api.middleware)`; thunk plus development-only immutability and serializability middleware, DevTools on by default; Immer "mutating" reducers in `createSlice`; `createSelector` is exported by RTK; React Redux 9.1+ `useSelector.withTypes` and `useDispatch.withTypes`; `createApi` with `tagTypes`, `providesTags` and `invalidatesTags`; `setupListeners` enables `refetchOnFocus` and `refetchOnReconnect`; `pollingInterval`; `updateQueryData` for manual cache updates. No claims removed.

Method: documentation only; no commands were run.
