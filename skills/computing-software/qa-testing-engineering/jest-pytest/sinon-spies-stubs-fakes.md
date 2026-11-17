---
id: computing-software.qa-testing-engineering.jest-pytest.sinon-spies-stubs-fakes
name: sinon-spies-stubs-fakes
category: computing-software
field: qa-testing-engineering
product: jest-pytest
tags: [sinon-fakes, sinon, spies, stubs, fake-timers-sinon]
level: practitioner
status: verified
description: "Use Sinon.JS for test doubles with Mocha or any runner: spies, stubs with behaviours, fakes, sandboxes for cleanup, fake timers and sinon-chai assertions."
sources:
  - https://sinonjs.org/
  - https://github.com/sinonjs/sinon/blob/main/CHANGES.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Sinon spies, stubs and fakes

## Sandbox for automatic restore
```js
const sinon = require('sinon');
let sandbox;
beforeEach(() => { sandbox = sinon.createSandbox(); });
afterEach(() => { sandbox.restore(); });
```
The default `sinon` object is itself a sandbox: `sinon.restore()` in `afterEach` works too (ran on Sinon 22.1).

## Spies (record, don't change behaviour)
```js
const spy = sandbox.spy(logger, 'warn');
doWork();
sinon.assert.calledOnceWithExactly(spy, 'retrying', sinon.match.number);
```

## Stubs (replace behaviour)
```js
const get = sandbox.stub(api, 'get');
get.withArgs('/users/1').resolves({ id: 1 });
get.withArgs('/users/2').rejects(new Error('404'));
get.onFirstCall().returns(1).onSecondCall().throws(new TypeError('boom'));
sandbox.stub(fs, 'readFileSync').callsFake((p) => (p.endsWith('.json') ? '{}' : ''));
```

## Fakes (immutable behaviour, simpler API)
```js
const fake = sinon.fake.resolves({ ok: true });
sandbox.replace(client, 'send', fake);
await doThing();
expect(fake.callCount).to.equal(1);
expect(fake.lastArg).to.deep.include({ to: 'a@b.test' });
```
`sinon.replace`, `replaceGetter`, `replaceSetter` swap properties with fakes.

## Fake timers
```js
const clock = sandbox.useFakeTimers({ now: new Date('2024-01-01T00:00:00Z'), toFake: ['setTimeout', 'Date'] });
scheduleReminder();
await clock.tickAsync(60_000);
```

## Matchers and sinon-chai
`sinon.match.has('id')`, `sinon.match.instanceOf(Error)`, `sinon.match(/re/)`. With `sinon-chai`: `expect(spy).to.have.been.calledWith(...)` (ran; sinon-chai 4 is ESM-only and needs chai 5 or 6, so it fails under Jest's CommonJS mode with "Must use import to load ES Module").

## Gotchas
- Stubbing ES module named exports doesn't work: `sinon.stub(mod, 'f')` on a namespace import throws "ES Modules cannot be stubbed" (ran on Node 20). Stub methods on objects you inject, or use a module-mocking tool.
- Forgetting restore leaks stubs into other tests; the sandbox pattern prevents it.

## Verify
After `sandbox.restore()`, the original method is back (ran: `api.get` is the original function and `typeof api.get.restore` is `undefined`).
