---
id: computing-software.software-engineering.typescript.javascript-error-handling
name: javascript-error-handling
category: computing-software
field: software-engineering
product: typescript
tags: [javascript, js-errors, error-cause, custom-errors, aggregateerror, unknown-in-catch, typescript]
level: practitioner
status: docs-checked
description: "Handle errors well in JS/TS: custom Error subclasses, Error.cause chains, catch(e: unknown) narrowing, finally and using, AggregateError, and never throwing non-Error values."
sources:
  - https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Error
  - https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Error/cause
  - https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Statements/try...catch
  - https://www.typescriptlang.org/tsconfig/#useUnknownInCatchVariables
  - https://www.typescriptlang.org/docs/handbook/release-notes/typescript-5-2.html
  - https://nodejs.org/api/cli.html#--unhandled-rejectionsmode
  - https://typescript-eslint.io/rules/only-throw-error/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# JavaScript error handling

**Goal:** errors that keep their stack and cause, can be told apart safely, and are
never silently lost.

## Custom errors
```ts
export class NotFoundError extends Error {
  readonly status = 404;
  constructor(public readonly resource: string, options?: ErrorOptions) {
    super(`${resource} not found`, options);
    this.name = "NotFoundError";            // shows in stack traces and logs
  }
}
```
Keep a small hierarchy (`AppError` base with `code`/`status`), or discriminate on a `code`
string when errors cross boundaries (workers, serialisation) where `instanceof` fails.

## Wrap with cause
```ts
try {
  await db.query(sql);
} catch (err) {
  throw new Error(`loading invoice ${id} failed`, { cause: err });   // ES2022
}
```
Don't lose the original by re-throwing a new Error without it.

## catch variables are unknown
With `strict` (`useUnknownInCatchVariables`), `catch (e)` has type `unknown`: anything can be
thrown, including strings and `undefined`.
```ts
catch (e) {
  if (e instanceof NotFoundError) return res.status(404).end();
  const msg = e instanceof Error ? e.message : String(e);
  log.error({ err: e }, msg);
  throw e;
}
```
Always `throw new Error(...)`, never strings or plain objects (no stack). Lint:
`no-throw-literal`, `@typescript-eslint/only-throw-error`.

## finally and using
```ts
const conn = await pool.connect();
try { return await work(conn); } finally { conn.release(); }

await using conn2 = await openConnection();   // value must implement [Symbol.asyncDispose]() (TS 5.2+)
```
`return` inside `finally` overrides the thrown error - avoid.

## Multiple failures
```ts
const results = await Promise.allSettled(tasks);
const errors = results.filter((r) => r.status === "rejected").map((r) => r.reason);
if (errors.length) throw new AggregateError(errors, "2 of 5 uploads failed");
```
`Promise.any` rejects with an `AggregateError` too.

## Async specifics
An un-awaited rejected promise becomes an unhandled rejection (crashes Node by default).
`return await` inside `try` so the catch actually sees the rejection.

## Result types (optional)
For expected failures (validation), returning `{ ok: false, error }` unions keeps control flow
explicit; reserve throwing for unexpected conditions.

## Verify
- [ ] Every custom error sets `name`; wrapped errors pass `{ cause }`.
- [ ] Lint forbids throwing non-Error values.

## Checked
Checked 2026-10-25 against MDN, the TypeScript-Website docs, the bundled lib.es2022.error.d.ts and esnext.disposable.d.ts, the Node.js CLI docs and the typescript-eslint rule docs. Confirmed: `ErrorOptions` with `cause` (ES2022 lib); useUnknownInCatchVariables is part of the strict family (4.4); `await using` and `Symbol.asyncDispose` in TS 5.2; `Promise.any` rejecting with AggregateError; a `return` in `finally` overriding a pending throw; `--unhandled-rejections` defaulting to throw; the only-throw-error rule exists. Removed the unconfirmed logger behaviour claim and the invented pool API.
Method: documentation only; no commands were run.
