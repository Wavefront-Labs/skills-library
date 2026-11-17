---
id: computing-software.web-development.trpc.formdata-and-binary-inputs
name: formdata-and-binary-inputs
category: computing-software
field: web-development
product: trpc
tags: [trpc, formdata, file-upload, octetinputparser, non-json]
level: advanced
status: docs-checked
description: "Accept FormData, File, Blob and Uint8Array inputs in mutations with z.instanceof(FormData) and octetInputParser, routed through httpLink via splitLink."
sources:
  - https://github.com/trpc/trpc/blob/main/www/v11/docs/server/non-json-content-types.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Besides JSON, tRPC can take FormData, File, Blob and other binary types as procedure inputs.

FormData:

```ts
hello: publicProcedure.input(z.instanceof(FormData)).mutation((opts) => {
  return { greeting: `Hello ${opts.input.get('name')}` };
}),
// client
const form = new FormData();
form.append('name', 'Bilbo');
await client.hello.mutate(form);
```

Binary: `tRPC` converts octet content types (`Blob`, `Uint8Array`, `File`) to a `ReadableStream`:

```ts
upload: publicProcedure.input(octetInputParser).mutation(async (opts) => {
  const reader = opts.input.getReader();
  let bytes = 0;
  while (true) {
    const { done, value } = await reader.read();
    if (done) break;
    bytes += value.byteLength;
  }
  return { bytes };
}),
```

`octetInputParser` comes from `@trpc/server/http`. On the client pass a `File`, `Blob` or `Uint8Array` to `.mutate()`.

Constraints: only `httpLink` sends non-JSON inputs, and only for mutations (a POST body); `httpBatchLink`, `httpBatchStreamLink` and the default `wsLink` serialize JSON and turn a `FormData` into `{}`. Use a `splitLink` with `condition: (op) => isNonJsonSerializable(op.input)` sending true to `httpLink` and false to `httpBatchLink`. Queries throw `FormData is only supported for mutations` unless `methodOverride: 'POST'` is set.

With a server transformer, give the non-JSON `httpLink` a transformer whose `serialize` is the identity and whose `deserialize` decodes responses, because tRPC passes these inputs untouched. Also stop the server framework parsing the body first (Express body parsers; Next pages `bodyParser: false`).

## Checked

2026-11-04: read in full against the tRPC docs repo (trpc/trpc, docs repo www/v11/docs/): server/non-json-content-types.md. Every parameter name, default, error string and code sample left in this skill appears on those pages. Removed: the invented Verify step.

Method: documentation only; no commands were run.
