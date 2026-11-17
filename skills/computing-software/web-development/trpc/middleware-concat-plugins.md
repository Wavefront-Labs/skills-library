---
id: computing-software.web-development.trpc.middleware-concat-plugins
name: middleware-concat-plugins
category: computing-software
field: web-development
product: trpc
tags: [trpc, middleware, concat, plugin, library]
level: sme
status: docs-checked
description: "Use procedure.concat() to attach a partial procedure from a separate tRPC instance, the supported way to ship reusable tRPC plugins and libraries."
sources:
  - https://github.com/trpc/trpc/blob/main/www/v11/docs/server/middlewares.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Creating middleware with `t.middleware` ties its `Context` type to your tRPC instance, and `experimental_standaloneMiddleware()` cannot carry input parsers. `.concat()` lets you define a partial procedure independently and attach it to any instance whose context and metadata match what the plugin needs. The docs say it primarily targets plugin and library authors.

```ts
export function createMyPlugin() {
  // a plugin uses the same API as any app: its own root t
  const t = initTRPC.context<{}>().meta<{}>().create();
  return {
    pluginProc: t.procedure.use((opts) => {
      return opts.next({
        ctx: { fromPlugin: 'hello from myPlugin' as const },
      });
    }),
  };
}

// the app using the plugin
const plugin = createMyPlugin();
const procedureWithPlugin = publicProcedure
  .concat(plugin.pluginProc)
  .use((opts) => opts.next());

export const appRouter = router({
  hello: procedureWithPlugin.query((opts) => opts.ctx.fromPlugin),
});
```

The plugin may also call `.input()` to validate input it needs. The plugin's own `context<...>()` and `meta<...>()` declare what the host app must extend; the host's base `initTRPC` object has to be compatible.

A TODO comment in the docs source asks for a real-world plugin example, so treat this as the documented shape only.

## Checked

2026-11-07. Read in full from a clone of github.com/trpc/trpc (main, commit fe64009), www/v11/docs/server/middlewares.md (read in full): the tip about `t.middleware` and `experimental_standaloneMiddleware()` limits, the `.concat()` paragraph, the full plugin/app snippet and its comments about `.input()`, `context` and `meta`.

Removed or corrected: the invented Verify step; reworded the TODO sentence (it is an HTML comment in the source, not visible on the rendered page). The page also notes experimental_standaloneMiddleware is deprecated in favour of `.concat()`.

Method: documentation only; no commands were run.
