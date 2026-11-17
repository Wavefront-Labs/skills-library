---
id: computing-software.devops-ci-cd.backstage.scaffolder-dry-run-actions
name: scaffolder-dry-run-actions
category: computing-software
field: devops-ci-cd
product: backstage
tags: [dry-run, supports-dry-run, ctx-is-dry-run, backstage]
level: advanced
status: docs-checked
description: "Make custom scaffolder actions safe to test by declaring supportsDryRun and checking ctx.isDryRun."
sources:
  - https://backstage.io/docs/features/software-templates/dry-run-testing
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Scaffolder templates can be tested with a dry run, which simulates actions without changing your environment. Actions take part only if they opt in.

Opt in by setting `supportsDryRun: true` in the object passed to `createTemplateAction`:

```ts
export function exampleAction() {
  return createTemplateAction({
    id: 'action:example',
    description: 'Example action',
    supportsDryRun: true,
    schema: {
      input: {
        example: z => z.string(),
      },
    },
    async handler(ctx) {
      if (ctx.isDryRun) {
        ctx.logger.info('Dry run: would call the external API');
        return;
      }
      // real side effects here
    },
  });
}
```

- `supportsDryRun: true` goes in the configuration object of `createTemplateAction`.
- Inside the handler, check `ctx.isDryRun` and return early (after logging) instead of making real changes, as the docs example does.
- A dry run can output non-sensitive inputs as feedback.
- Add a unit test that calls the handler with `isDryRun: true` in the context.

## Checked

2026-11-03. Confirmed against the Backstage Dry Run Testing page: `supportsDryRun`, `ctx.isDryRun`, early return, test pattern. Removed: the claim that actions without the flag are not run, and unsupported advice on the template editor and documenting support.

Method: documentation only; no commands were run.
