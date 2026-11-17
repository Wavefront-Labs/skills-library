---
id: computing-software.web-development.trpc.custom-trpc-link
name: custom-trpc-link
category: computing-software
field: web-development
product: trpc
tags: [trpc, links, custom-link, observable, operation-context]
level: advanced
status: docs-checked
description: "Write your own TRPCLink with the three-layer function shape, observable passthrough and op.context for passing metadata between links."
sources:
  - https://github.com/trpc/trpc/blob/main/www/v11/docs/client/links.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
A link is a function following the `TRPCLink` type, built from three layers:

1. The outer function has no parameters. It is the setup phase and runs once per app, useful for caches or other state.
2. It returns a function receiving `{ op, next }`: `op` is the `Operation` being executed, `next` calls the next link down the chain.
3. That returns an `observable` (from `@trpc/server/observable`) whose callback receives an `observer` used to notify the link above of the result.

```ts
import { TRPCLink } from '@trpc/client';
import { observable } from '@trpc/server/observable';

export const customLink: TRPCLink<AppRouter> = () => {
  return ({ next, op }) => {
    return observable((observer) => {
      console.log('performing operation:', op);
      const unsubscribe = next(op).subscribe({
        next(value) { observer.next(value); },
        error(err) { observer.error(err); },
        complete() { observer.complete(); },
      });
      return unsubscribe;
    });
  };
};
```

You can return `next(op)` untouched, or subscribe to it to observe or alter the result. The docs example returns the `unsubscribe` function from the `observable` callback.

Context: each operation carries a context that every link can read and modify through `op.context`. Set its initial value per call by passing `context` to the call, for example `trpc.posts.query(undefined, { context: { skipBatch: true } })`, or `trpc: { context }` in React Query options. A `splitLink` condition can then branch on it.

The docs point to the built-in links in the tRPC repository under `packages/client/src/links` as a reference.

## Checked

2026-11-04: read in full against the tRPC docs repo (trpc/trpc, docs repo www/v11/docs/): client/links.md (Creating a custom link, Managing context), client/links/splitLink.md. Every parameter name, default, error string and code sample left in this skill appears on those pages. Removed: the invented Verify step and the unsupported 'so cancellation propagates' rationale.

Method: documentation only; no commands were run.
