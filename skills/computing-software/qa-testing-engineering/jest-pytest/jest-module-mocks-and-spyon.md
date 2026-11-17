---
id: computing-software.qa-testing-engineering.jest-pytest.jest-module-mocks-and-spyon
name: jest-module-mocks-and-spyon
category: computing-software
field: qa-testing-engineering
product: jest-pytest
tags: [jest-mock-modules, spyon, jest-mock, manual-mocks, jest]
level: practitioner
status: verified
description: "Mock modules in Jest: jest.mock with factories and automock, __mocks__ manual mocks, jest.spyOn with restore, requireActual for partial mocks, and hoisting rules."
sources:
  - https://jestjs.io/docs/mock-functions
  - https://jestjs.io/docs/manual-mocks
  - https://jestjs.io/docs/jest-object#jestspyonobject-methodname
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Module mocks in Jest (jest.mock, manual mocks, spyOn)

## jest.mock with factory
```ts
import { sendEmail } from './email';
import { placeOrder } from './orders';

jest.mock('./email', () => ({
  sendEmail: jest.fn().mockResolvedValue({ id: 'msg-1' }),
}));

test('sends confirmation', async () => {
  await placeOrder({ sku: 'SKU-1' });
  expect(sendEmail).toHaveBeenCalledWith(expect.objectContaining({ template: 'order-confirmation' }));
});
```
`jest.mock` calls are hoisted above imports by babel-jest/ts-jest (ran: with `transform: {}` and no hoisting, `jest.mock` after `require` did not apply). Factory variables must be prefixed `mock` (`const mockSend = jest.fn()`) to be referenced inside the factory.

## Partial mock
```ts
jest.mock('./pricing', () => ({
  ...jest.requireActual('./pricing'),
  fetchRates: jest.fn().mockResolvedValue({ GBP: 1 }),
}));
```

## Automock and typed access
`jest.mock('./email')` without a factory auto-mocks all exports (functions return undefined). Typed: `jest.mocked(sendEmail).mockResolvedValueOnce(...)`.

## Manual mocks
`src/__mocks__/email.ts` adjacent to `src/email.ts`; activate with `jest.mock('./email')`. For node_modules packages, `__mocks__/axios.ts` next to `node_modules` is used automatically (except core Node modules, which need explicit `jest.mock('fs')`).

## spyOn
```ts
const spy = jest.spyOn(console, 'error').mockImplementation(() => {});
const nowSpy = jest.spyOn(Date, 'now').mockReturnValue(1_700_000_000_000);
afterEach(() => jest.restoreAllMocks());
```
spyOn keeps the real implementation unless replaced; works on object methods (and module namespace objects in CJS, not ESM).

## Reset semantics
- `mockClear`: clear calls. `mockReset`: clear + remove implementations (on Jest 30 a spy then returns `undefined`, not the original, and `jest.fn(() => 5)` also returns `undefined`). `mockRestore`: restore original (spyOn only; on a plain `jest.fn` it also drops the implementation).
- Vitest differs: its `mockReset` restores the original implementation.
- Config: `clearMocks: true` / `restoreMocks: true` in jest.config to reset between tests.

## ESM
In native ESM mode use `jest.unstable_mockModule('./email.js', () => ({...}))` before a dynamic `await import()`.

## Gotchas
- Mocking modules you own heavily couples tests to structure; mock at boundaries (HTTP, email, clock).
- Mocks leaking across tests: enable `restoreMocks`.

## Verify
Mocks are reset between tests by config, and each mocked module is a boundary (network, time, side effect).
