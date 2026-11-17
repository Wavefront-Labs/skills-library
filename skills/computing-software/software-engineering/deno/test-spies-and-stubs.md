---
id: computing-software.software-engineering.deno.test-spies-and-stubs
name: test-spies-and-stubs
category: computing-software
field: software-engineering
product: deno
tags: [test, mocking, spy, stub, returns-next, using-keyword, test-doubles]
level: practitioner
status: docs-checked
description: "Use spy, stub and returnsNext from @std/testing/mock to replace collaborators, with disposable using declarations that restore originals."
sources:
  - https://raw.githubusercontent.com/denoland/docs/main/runtime/test/mocking.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
A spy records calls (count, arguments) without changing behaviour. A stub replaces the implementation and also records calls, so spy assertions work on it. A "mock" is the umbrella term, usually a hand-built stand-in whose methods are spies or stubs. All live in `jsr:@std/testing/mock`.

```ts
import { assertSpyCall, assertSpyCalls, spy } from "jsr:@std/testing/mock";

const mockDatabase = {
  save: spy((user: User) => Promise.resolve({ id: 1, ...user })),
};
// after calling code under test:
assertSpyCalls(mockDatabase.save, 1);
assertSpyCall(mockDatabase.save, 0, { args: [user] });
```

Method spies and stubs are disposable; declare with `using` and the original method is restored when the test ends (otherwise call `.restore()` in a `finally`):

```ts
using addSpy = spy(calculator, "add");
using getUserNameStub = stub(deps, "getUserName", () => "Test User");
```

Wrap dependencies in an object (like `deps`) so tests can stub them.

Different answers per call:

```ts
import { returnsNext, stub } from "jsr:@std/testing/mock";

using fetchDataStub = stub(
  dataService,
  "fetchData",
  returnsNext(["first result", "second result"]),
);
```

Choose the simplest double: spy to verify an interaction, stub when the real thing is slow, nondeterministic or external. Stub at the interface boundary, not deep in implementation, and let `using` prevent bleed between tests.

## Checked

2026-11-04. Confirmed against docs runtime/test/mocking.md: spy, stub, returnsNext, assertSpyCall(s), disposable using, restore(), spy/stub/mock distinction.

Method: documentation only; no commands were run.
