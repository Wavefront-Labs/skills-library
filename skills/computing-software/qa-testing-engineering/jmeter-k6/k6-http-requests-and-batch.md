---
id: computing-software.qa-testing-engineering.jmeter-k6.k6-http-requests-and-batch
name: k6-http-requests-and-batch
category: computing-software
field: qa-testing-engineering
product: jmeter-k6
tags: [k6-http, http-batch, k6-params, k6-response, load-testing]
level: practitioner
status: verified
description: "Make k6 HTTP requests correctly: methods, params (headers, tags, timeout, responseType), response handling, http.batch for parallel requests, URL grouping with http.url."
sources:
  - https://grafana.com/docs/k6/latest/using-k6/http-requests/
  - https://grafana.com/docs/k6/latest/javascript-api/k6-http/batch/
  - https://grafana.com/docs/k6/latest/javascript-api/k6-http/params/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# HTTP requests, batch and params

```js
import http from 'k6/http';
import { check } from 'k6';

export default function () {
  const res = http.post('https://api.test/orders', JSON.stringify({ sku: 'A1', qty: 1 }), {
    headers: { 'Content-Type': 'application/json', Authorization: `Bearer ${__ENV.TOKEN}` },
    tags: { name: 'POST /orders' },
    timeout: '10s',                    // default 60s
  });
  check(res, {
    'status 201': (r) => r.status === 201,
    'has id': (r) => r.json('id') !== undefined,
  });
}
```
Methods: `http.get/post/put/patch/del/head/options/request(method, url, body, params)` (all exist; run). Forms: pass an object body for `application/x-www-form-urlencoded`; `http.file()` in the body object switches to `multipart/form-data` (both content types confirmed in a run on k6 2.3.0).

## Responses
`res.status`, `res.body`, `res.json('a.b')` (gjson path), `res.headers`, `res.timings.duration|waiting|connecting|tls_handshaking`, `res.error`, `res.error_code`. `res.timings` has `duration, blocked, looking_up, connecting, tls_handshaking, sending, waiting, receiving`. `res.json('ids.1')` returned the second array element (gjson path); a missing path returns `undefined`. Use `responseType: 'none'` for large bodies you don't read (body is `null`, saves memory) or `'binary'` (body is an `ArrayBuffer`).

## Grouping dynamic URLs
Each unique URL becomes a separate metric series. For `/orders/123`:
```js
http.get(http.url`https://api.test/orders/${id}`);                 // name = template (recorded as `.../orders/${}`; run)
http.get(`https://api.test/orders/${id}`, { tags: { name: 'GET /orders/:id' } });
```
Without this, series cardinality explodes. k6 only warns past 100,000 unique time series (`timeSeriesFirstLimit` in `internal/metrics/engine/ingester.go`); 120 distinct ids produced no warning (run), so do not wait for the warning.

## Batch (parallel requests per VU)
```js
const responses = http.batch([
  ['GET', 'https://web.test/app.js', null, { tags: { name: 'static' } }],
  ['GET', 'https://web.test/app.css'],
  { method: 'GET', url: 'https://api.test/me', params: { headers: auth } },
]);
```
Mimics a browser loading assets in parallel; concurrency per host limited by `batchPerHost` option (default 6), total by `batch` (default 20); both defaults are in the k6 options reference.

## Expected statuses
`http_req_failed` counts statuses outside 200-399 as failures (redirect hops count too when only 200 is expected). A `timeout` of `500ms` against a 2 s endpoint ended at 500 ms with `status 0`, `error_code 1050`, `error: request timeout`. Override: `http.setResponseCallback(http.expectedStatuses(200, 201, 404))` or per request `responseCallback`.

## Gotchas
- `res.json()` on non-JSON throws (`cannot parse json due to an error at line 1, character 1`; run): check status first.
- `discardResponseBodies: true` option speeds tests but `res.body` becomes null; set `responseType: 'text'` on requests you need (run: global option gave `null`, with `responseType: 'text'` the body was `hello`).

## Verify
End-of-test summary shows grouped `name` tags and `http_req_failed` matching expected error rate.
