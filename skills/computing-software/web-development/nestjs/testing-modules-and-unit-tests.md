---
id: computing-software.web-development.nestjs.testing-modules-and-unit-tests
name: testing-modules-and-unit-tests
category: computing-software
field: web-development
product: nestjs
tags: [nestjs, testing, vitest, unit-testing, testingmodule]
level: practitioner
status: docs-checked
description: "Unit test NestJS classes with Test.createTestingModule, compile, get and resolve, and auto-mock missing dependencies with useMocker."
sources:
  - https://github.com/nestjs/docs.nestjs.com/blob/master/content/fundamentals/unit-testing.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Install `npm i --save-dev @nestjs/testing`. New projects use Vitest, but the APIs are runner-agnostic. Name unit tests `*.spec.ts` next to the class.

Isolated test (no DI): `new CatsController(new CatsService())`.

With Nest's testing module:

```typescript
beforeEach(async () => {
  const moduleRef = await Test.createTestingModule({
    controllers: [CatsController],
    providers: [CatsService],
  }).compile();

  catsService = moduleRef.get(CatsService);
  catsController = moduleRef.get(CatsController);
});

it('should return an array of cats', async () => {
  const result = ['test'];
  vi.spyOn(catsService, 'findAll').mockImplementation(() => result);
  expect(await catsController.findAll()).toBe(result);
});
```

`createTestingModule()` takes the same metadata as `@Module()`; `compile()` is async. `get()` retrieves static instances; for transient or request-scoped use `await moduleRef.resolve(CatsService)` (each call is a different instance).

Auto mocking: when a class has many dependencies, `useMocker()` supplies mocks for all missing ones:

```typescript
.useMocker((token) => {
  if (token === CatsService) {
    return { findAll: vi.fn().mockResolvedValue(['test1', 'test2']) };
  }
})
```

Retrieve them with `moduleRef.get(CatsService)`.

Gotchas:
- `REQUEST` and `INQUIRER` cannot be auto-mocked (predefined); overwrite them with a custom provider or `overrideProvider()`.
- `setLogger()` on the builder swaps the test logger; by default only error logs reach the console.

## Checked

2026-11-04. Confirmed against the official NestJS docs source: isolated and module-based tests, spec suffix, useMocker, REQUEST and INQUIRER limits, setLogger default (unit-testing page). Removed: invented Verify step.

Method: documentation only; no commands were run.
