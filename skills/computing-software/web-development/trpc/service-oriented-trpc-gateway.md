---
id: computing-software.web-development.trpc.service-oriented-trpc-gateway
name: service-oriented-trpc-gateway
category: computing-software
field: web-development
product: trpc
tags: [trpc, microservices, custom-link, faux-gateway, soa]
level: sme
status: docs-checked
description: "Split routers across services with a shared initTRPC, a type-only faux gateway and a custom client link that routes by the first path segment."
sources:
  - https://github.com/trpc/trpc/blob/main/www/v11/docs/server/service-oriented-architecture.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The docs say you probably do not need this: splitting adds moving parts and every service must share the same context type, error formatter and transformer. If unsure, merge routers in one server.

Four parts:

1. A shared library that creates the single tRPC instance (`initTRPC.context<Context>().create()`) and exports `router` and `publicProcedure`; every service imports it.
2. Services, each with its own router and server (any adapter, for example standalone on ports 2021 and 2022).
3. A faux gateway that merges the service routers (`router({ serverA: serverARouter, serverB: serverBRouter })`) and exports `type AppRouter`. It never runs; the client only imports its type.
4. A client with a custom terminating link:

```ts
const serviceLink: TRPCLink<AppRouter> = (runtime) => {
  // created once so calls to one service are batched together
  const services = {
    serverA: httpBatchLink<AppRouter>({ url: 'http://localhost:2021' })(runtime),
    serverB: httpBatchLink<AppRouter>({ url: 'http://localhost:2022' })(runtime),
  };
  return (ctx) => {
    const [name, ...rest] = ctx.op.path.split('.');
    const link = services[name as keyof typeof services];
    if (!link) throw new Error(`No service for procedure "${ctx.op.path}"`);
    return link({ ...ctx, op: { ...ctx.op, path: rest.join('.') } });
  };
};
```

Mistakes: forwarding the full path (service answers `No procedure found on path "serverA.greet"`), creating service links per call (no batching), separate `initTRPC` per service, omitting `<AppRouter>` on inner links (transformer check lost), and running the gateway.

## Checked

2026-11-07. Read in full from a clone of github.com/trpc/trpc (main, commit fe64009), www/v11/docs/server/service-oriented-architecture.md (read in full, including all twoslash blocks): the caution, the four parts, the shared instance, the standalone services on ports 2021 and 2022, the faux gateway, the custom link, and all five common mistakes including the `No procedure found on path "serverA.greet"` message. Every claim matched the page text.

Removed or corrected: nothing; the skill matched the page and only gained the Checked section.

Method: documentation only; no commands were run.
