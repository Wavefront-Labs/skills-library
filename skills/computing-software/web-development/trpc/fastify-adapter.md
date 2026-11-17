---
id: computing-software.web-development.trpc.fastify-adapter
name: fastify-adapter
category: computing-software
field: web-development
product: trpc
tags: [trpc, fastify, fastifytrpcplugin, maxparamlength, adapter]
level: practitioner
status: docs-checked
description: "Register fastifyTRPCPlugin on Fastify 5 with prefix and maxParamLength set high enough for batch URLs, with typed onError via satisfies."
sources:
  - https://github.com/trpc/trpc/blob/main/www/v11/docs/server/adapters/fastify.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The Fastify adapter converts a router into a Fastify plugin. The v11 adapter requires Fastify v5 or later; with Fastify v4 requests may return empty responses without errors.

```ts
import { fastifyTRPCPlugin, FastifyTRPCPluginOptions } from '@trpc/server/adapters/fastify';
import fastify from 'fastify';

const server = fastify({ routerOptions: { maxParamLength: 5000 } });

server.register(fastifyTRPCPlugin, {
  prefix: '/trpc',
  trpcOptions: {
    router: appRouter,
    createContext,
    onError({ path, error }) {
      console.error(`Error in tRPC handler on path '${path}':`, error);
    },
  } satisfies FastifyTRPCPluginOptions<AppRouter>['trpcOptions'],
});
await server.listen({ port: 3000 });
```

Why `maxParamLength`: a batch request puts every procedure in one path parameter (`/trpc/getUserById,createUser`), and Fastify's default of 100 makes it answer `414 URI Too Long` for longer ones. The `satisfies` clause helps TypeScript type `onError` correctly, since plugin typing is limited.

Plugin options: `prefix` (default `/trpc`), `useWSS` (default false, enable WebSockets through `@fastify/websocket`), and `trpcOptions` (router, createContext and the common adapter options; with `useWSS` also `keepAlive`, `dangerouslyDisablePong`, `experimental_encoder`).

Context: `createContext({ req, res }: CreateFastifyContextOptions)`.

## Checked

2026-11-04: read in full against the tRPC docs repo (trpc/trpc, docs repo www/v11/docs/): server/adapters/fastify.md. Every parameter name, default, error string and code sample left in this skill appears on those pages. Removed: the invented Verify step.

Method: documentation only; no commands were run.
