---
id: computing-software.web-development.trpc.data-transformer-devalue-and-directions
name: data-transformer-devalue-and-directions
category: computing-software
field: web-development
product: trpc
tags: [trpc, transformer, devalue, serialize, deserialize]
level: advanced
status: docs-checked
description: "Use devalue as a compact transformer, and supply separate input and output transformers via the CombinedDataTransformer interface."
sources:
  - https://github.com/trpc/trpc/blob/main/www/v11/docs/server/data-transformers.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Devalue works like superjson but focuses on performance and compact payloads, at the cost of a less human-readable body. Define the transformer once and share it (for example in `utils/trpc.ts`):

```ts
import { parse, stringify } from 'devalue';

export const transformer = {
  deserialize: (object: any) => parse(object),
  serialize: (object: any) => stringify(object),
};
```

The docs use `parse` and `stringify` because they mitigate XSS. Pass `transformer` to `initTRPC.create({ transformer })` on the server and to each link on the client.

Different transformers for upload and download are possible. Provide a combined transformer: `input` (`InputDataTransformer`) where `serialize` runs on the client before sending and `deserialize` runs on the server before the resolver; and `output` (`OutputDataTransformer`) where `serialize` runs on the server before sending and `deserialize` runs only on the client. Use the same combined transformer everywhere.

The `DataTransformer` interface is just `serialize(object)` and `deserialize(object)`.

Common mistakes from the docs: transformer on only one side or some links (compile error, or at runtime data arrives encoded as `{ json, meta }` or calls fail with `Unable to transform response from server`); creating a link outside the `links` array so the check is skipped (pass the router type, `httpBatchLink<AppRouter>(...)`, to restore it); passing `transformer` to `createTRPCClient()` (rejected, it has moved to the links).

## Checked

2026-11-04: read in full against the tRPC docs repo (trpc/trpc, docs repo www/v11/docs/): server/data-transformers.md (devalue, upload/download transformers, DataTransformer interface, Common mistakes). Every parameter name, default, error string and code sample left in this skill appears on those pages. Removed: nothing; no Verify step was present.

Method: documentation only; no commands were run.
