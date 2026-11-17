---
id: computing-software.qa-testing-engineering.test-automation.in-process-http-mocking
name: in-process-http-mocking
category: computing-software
field: qa-testing-engineering
product: test-automation
tags: [nock, responses-library, respx, http-mocking, unit-test-isolation]
level: practitioner
status: verified
description: "Mock outbound HTTP inside unit and integration tests with nock (Node), responses (requests) and respx (httpx): matching, asserting calls, disabling real network."
sources:
  - https://github.com/nock/nock
  - https://github.com/getsentry/responses
  - https://lundberg.github.io/respx/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# In-process HTTP mocking (nock, responses, respx)

Intercepts the HTTP client library inside the test process: no server, fast, deterministic. Use for unit/component tests of code that calls external APIs; use WireMock/contract tests for broader integration.

## Node: nock
```js
const nock = require('nock');   // nock 15 is ESM-only: on Node 24 `require` returns `{ default }`, so use `require('nock').default` or `import nock from 'nock'`
beforeAll(() => nock.disableNetConnect());          // any unmocked request throws
afterAll(() => nock.enableNetConnect());
afterEach(() => nock.cleanAll());

test('fetches rate', async () => {
  const scope = nock('https://api.fx.test')
    .get('/rates').query({ base: 'NZD' })
    .matchHeader('authorization', /^Bearer /)
    .reply(200, { USD: 0.61 });
  expect(await getRate('NZD', 'USD')).toBe(0.61);
  scope.done();                                     // asserts all interceptors were used
});
```
Errors and delays: `.replyWithError(Object.assign(new Error('reset'), { code: 'ECONNRESET' }))` (an Error object, as in the nock README; with nock 15.0.5 a plain `{ code: 'ECONNRESET' }` object emitted no error at all and the request just hung, while a string or Error object worked), `.delay(2000)`. With `disableNetConnect()` an unmocked request fails with `code: 'ENETUNREACH'` (NetConnectNotAllowedError). Node 18+ native `fetch` (undici) is supported in nock 14+ (v14.0.0 release notes: "support for native fetch", drops Node < 18; ran with fetch on 15.0.5); older nock only patches `http`/`https`: use `undici`'s `MockAgent` otherwise.

## Python requests: responses
```python
import responses
@responses.activate
def test_rate():
    responses.get("https://api.fx.test/rates", json={"USD": 0.61}, status=200,
                  match=[responses.matchers.query_param_matcher({"base": "NZD"})])
    assert get_rate("NZD", "USD") == 0.61
    assert responses.calls[0].request.headers["Authorization"].startswith("Bearer ")
```
Unmatched requests raise `requests.exceptions.ConnectionError`. `@responses.activate` does not fail on unused mocks by default; `responses.RequestsMock(assert_all_requests_are_fired=True)` raises `AssertionError: Not all requests have been executed` on exit.

## Python httpx: respx
```python
import respx, httpx
@respx.mock(assert_all_called=True)
async def test_rate(respx_mock):      # the decorator-with-arguments form injects its own router
    route = respx_mock.get("https://api.fx.test/rates", params={"base": "NZD"}).mock(return_value=httpx.Response(200, json={"USD": 0.61}))
    assert await get_rate("NZD", "USD") == 0.61
    assert route.called
```
Side effects: `.mock(side_effect=httpx.ConnectTimeout)`. Gotcha (run on respx with httpx): inside `@respx.mock(assert_all_called=True)` the module-level `respx.get(...)` adds routes to the global router, not the decorator's, so the call fails with `AllMockedAssertionError: ... not mocked!`; use the injected `respx_mock` argument (or the bare `@respx.mock` form with `respx.get`). An unmocked URL raises `AllMockedAssertionError`; an uncalled route fails `assert_all_called`.

## Practices
- Disable real network globally in the unit test suite so a missing mock fails loudly.
- Mock at the HTTP boundary, not your own client wrapper, to keep serialisation and error handling under test.
- Keep fixture payloads from real (scrubbed) responses; validate them against the provider's schema periodically.

## Gotchas
- Mocks match the library, not the protocol: switching from requests to httpx silently bypasses `responses` mocks: an httpx call under `@responses.activate` tried a real connection and raised `httpx.ConnectError`.
- Over-specified matchers (exact header sets) make tests brittle; match what matters.

## Verify
Remove a mock: the test fails with a "no match" / disallowed network error, not a real outbound call.
