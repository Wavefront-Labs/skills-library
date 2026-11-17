---
id: computing-software.qa-testing-engineering.cypress.modifying-requests-and-responses-in-intercept
name: modifying-requests-and-responses-in-intercept
category: computing-software
field: qa-testing-engineering
product: cypress
tags: [intercept-handler, cy-intercept, network-stubbing, req-reply, response-modification]
level: practitioner
status: verified
description: "Modify traffic in cy.intercept handlers: change request headers and bodies, req.reply stubs, req.continue with res.send to alter real responses, delays and network errors."
sources:
  - https://docs.cypress.io/api/commands/intercept#Intercepting-a-request
  - https://docs.cypress.io/api/commands/intercept#Intercepting-a-response
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Modifying requests and responses in intercept handlers

## Static stubs
```js
cy.intercept('GET', '/api/products*', { fixture: 'products.json' }).as('products');
cy.intercept('GET', '/api/me', { statusCode: 401, body: { error: 'expired' } });
cy.intercept('POST', '/api/pay', { forceNetworkError: true });
cy.intercept('GET', '/api/slow', { delay: 3000, body: [] });
```

## Request handler
```js
cy.intercept('POST', '/api/orders', (req) => {
  req.headers['x-test-run'] = Cypress.expose('RUN_ID');   // add header to the real request (RUN_ID from the `expose` config or --expose)
  req.body.giftWrap = true;                               // modify outgoing body
  if (req.body.qty > 99) {
    req.reply({ statusCode: 422, body: { error: 'qty too large' } });   // stub this case only
    return;
  }
  req.continue();                                         // send to server unchanged otherwise
});
```

## Response handler (real server, altered response)
```js
cy.intercept('GET', '/api/basket', (req) => {
  req.continue((res) => {
    res.body.items[0].stock = 0;          // simulate out-of-stock from real data
    res.setDelay(1500);                   // or res.setThrottle(kbps)
    res.send();                            // optional; sends modified res
  });
});
```
Shortcut: `req.on('response', (res) => {...})`; `req.on('before:response')` ran first (observed order: `before`, then the newest handler's `response`, then the older one's).

## Handler order
Intercepts defined later run first (newest-first). A handler that neither replies nor calls `req.continue()` passes the request on to the next older handler; `req.continue()` (or `req.reply()`) ends the chain, so older handlers do not run (observed: newer pass-through then older; newer `continue` and the older one never ran). Middleware handlers always run first: `cy.intercept({ method: 'GET', url: '/api/basket', middleware: true }, handler)` (the matcher object, not a 4th argument: a 4-argument call throws "accepts a maximum of 3 arguments").

## Test ideas
- Error states: 500, 503 with retry-after, timeouts (delay beyond app timeout), network errors.
- Edge data: empty lists, very long strings, unexpected fields.
- Race conditions: delay one of two parallel requests.

## Gotchas
- `req.reply` and `req.continue` are mutually exclusive per request (calling both throws "a request can only be completed once").
- `req.body` is a parsed object only when the request is JSON (`content-type: application/json`); a plain-string `fetch` body arrived as a string ("Cannot create property 'giftWrap' on string").
- Setting `req.url` to another host worked (the response came from the other server).
- `cy.request` calls are not intercepted; use the app's own `fetch`/XHR.
- Chrome, Chromium and Edge on Cypress 16 intercept on the native network: `req.httpVersion` is gone and compression headers are absent on intercepted responses (changelog 16.0.0).
- Stubbed responses skip the server; keep some tests unstubbed for integration confidence.

## Verify
Run on Cypress 16.2.0 (Electron): header/body edits reached the server, the `qty` 100 case got a stubbed 422, `res.body` edit plus `setDelay`, `setThrottle`, `forceNetworkError`, 401 stub and delay all behaved as shown. Each error-state test fails if the app ignores the error (e.g. remove error UI), and unstubbed smoke tests still exist.
