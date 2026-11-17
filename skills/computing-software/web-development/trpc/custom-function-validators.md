---
id: computing-software.web-development.trpc.custom-function-validators
name: custom-function-validators
category: computing-software
field: web-development
product: trpc
tags: [trpc, validator, input, output, plain-function]
level: practitioner
status: docs-checked
description: "Validate without a library by passing a function to .input() or .output() that returns the typed value or throws."
sources:
  - https://github.com/trpc/trpc/blob/main/www/v11/docs/server/validators.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
A validator is only TypeScript: any function that takes unknown input and returns the typed value (throwing on failure) works for `.input()` and `.output()`.

```ts
export const appRouter = t.router({
  hello: publicProcedure
    .input((value): string => {
      if (typeof value === 'string') {
        return value;
      }
      throw new Error('Input is not a string');
    })
    .output((value): string => {
      if (typeof value === 'string') {
        return value;
      }
      throw new Error('Output is not a string');
    })
    .query((opts) => {
      return `hello ${opts.input}`;
    }),
});
```

In the docs example the return type annotation (`: string`) types `opts.input`. The docs do not recommend a custom validator unless you have a specific need (use a validation library in most cases), but stress that there is no magic here: it is just TypeScript.

## Checked

2026-11-04: read in full against the tRPC docs repo (trpc/trpc, docs repo www/v11/docs/): server/validators.md (The most basic validator: a function). Every parameter name, default, error string and code sample left in this skill appears on those pages. Removed: the invented Verify step, the claim that a library gives better messages, the 'tiny cases / branded type' advice, and a misread of the Standard Schema PR note.

Method: documentation only; no commands were run.
