---
id: computing-software.web-development.trpc.reusable-base-procedures
name: reusable-base-procedures
category: computing-software
field: web-development
product: trpc
tags: [trpc, base-procedure, authedprocedure, middleware, reuse]
level: practitioner
status: docs-checked
description: "Build reusable base procedures (publicProcedure, authedProcedure, organizationProcedure) by chaining use() and input() so auth and validation are written once."
sources:
  - https://github.com/trpc/trpc/blob/main/www/v11/docs/server/procedures.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The recommended pattern is to rename and export `t.procedure` as `publicProcedure`, then derive further named base procedures for common needs. Because the builder is immutable, each derived procedure adds behaviour without changing its parent.

```ts
export const authedProcedure = t.procedure.use(async function isAuthed(opts) {
  const { ctx } = opts;
  if (!ctx.user) {
    throw new TRPCError({ code: 'UNAUTHORIZED' });
  }
  return opts.next({ ctx: { user: ctx.user } }); // user now non-null
});

export const organizationProcedure = authedProcedure
  .input(z.object({ organizationId: z.string() }))
  .use(function isMemberOfOrganization(opts) {
    const membership = opts.ctx.user.memberships.find(
      (m) => m.Organization.id === opts.input.organizationId,
    );
    if (!membership) throw new TRPCError({ code: 'FORBIDDEN' });
    return opts.next({ ctx: { Organization: membership.Organization } });
  });
```

A procedure built on `organizationProcedure` can add its own `.input()` (for example an email); the inputs are merged, so the handler sees both `organizationId` and `email`, and `ctx` contains the non-null `user` and the `Organization`.

The docs call this a simplified example: in practice you may combine headers, context, middleware and metadata to authenticate and authorize your users.

## Checked

2026-11-07. Read in full from a clone of github.com/trpc/trpc (main, commit fe64009), www/v11/docs/server/procedures.md (read in full): the base procedures section, the authedProcedure and organizationProcedure snippet, and the comments about merged input and ctx in addMember.

Removed or corrected: the invented Verify step; softened "combine" to "may combine" to match the page.

Method: documentation only; no commands were run.
