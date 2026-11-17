---
id: computing-software.web-development.trpc.infer-procedure-builder-resolver-options
name: infer-procedure-builder-resolver-options
category: computing-software
field: web-development
product: trpc
tags: [trpc, inferprocedurebuilderresolveroptions, typescript, resolver, helper]
level: advanced
status: docs-checked
description: "Type a standalone handler function with inferProcedureBuilderResolverOptions so ctx and input stay correctly typed when you split logic out of the router."
sources:
  - https://github.com/trpc/trpc/blob/main/www/v11/docs/server/procedures.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
When you want to move a resolver out of the router file (or share a helper across procedures built on the same base), you need the type of the `opts` the builder would pass. `inferProcedureBuilderResolverOptions` extracts it from a procedure builder:

```ts
import { inferProcedureBuilderResolverOptions } from '@trpc/server';

async function getMembersOfOrganization(
  opts: inferProcedureBuilderResolverOptions<typeof organizationProcedure>,
) {
  // input and ctx are now correctly typed!
  const { ctx, input } = opts;
  return await prisma.user.findMany({
    where: { membership: { organizationId: ctx.Organization.id } },
  });
}

export const appRouter = t.router({
  listMembers: organizationProcedure.query(async (opts) => {
    return await getMembersOfOrganization(opts);
  }),
});
```

In the docs example `ctx` and `input` are correctly typed inside the helper.

The docs suggest it for separating a procedure's handler from its definition at the router, or for a helper function that works with multiple procedures. Inferring the input and output types of a procedure is covered separately in the client infer-types docs.

## Checked

2026-11-04: read in full against the tRPC docs repo (trpc/trpc, docs repo www/v11/docs/): server/procedures.md (Inferring the options type of a Base Procedure). Every parameter name, default, error string and code sample left in this skill appears on those pages. Removed: the invented Verify step, the inferRouterInputs/inferRouterOutputs names and the controller-style wording.

Method: documentation only; no commands were run.
