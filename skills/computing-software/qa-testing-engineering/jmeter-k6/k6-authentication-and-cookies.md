---
id: computing-software.qa-testing-engineering.jmeter-k6.k6-authentication-and-cookies
name: k6-authentication-and-cookies
category: computing-software
field: qa-testing-engineering
product: jmeter-k6
tags: [k6-auth, k6-cookies, cookie-jar, oauth-load-test, token-reuse]
level: practitioner
status: verified
description: "Handle authentication in k6 load tests: token fetch in setup vs per VU, OAuth client credentials, basic/digest/NTLM, cookie jars, and avoiding login storms on the IdP."
sources:
  - https://grafana.com/docs/k6/latest/using-k6/cookies/
  - https://grafana.com/docs/k6/latest/examples/http-authentication/
  - https://grafana.com/docs/k6/latest/javascript-api/k6-http/cookiejar/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Authentication and cookie jar handling

## Decide the auth model first
- **Measure login?** Then log in per iteration (realistic but loads the IdP).
- **Measure the API?** Get tokens once and reuse; don't load-test the identity provider by accident (and get rate-limited).

## Token once in setup (shared)
```js
export function setup() {
  const res = http.post(`${__ENV.IDP}/oauth/token`, {
    grant_type: 'client_credentials', client_id: __ENV.CID, client_secret: __ENV.CSECRET,
  });
  return { token: res.json('access_token') };
}
export default function (data) {
  http.get(`${__ENV.API}/orders`, { headers: { Authorization: `Bearer ${data.token}` } });
}
```
Tokens expiring mid-test: refresh per VU when `exp` is near, or issue long-lived test tokens.

## Token per VU (different users)
```js
let token;   // VU-global, persists across iterations of this VU (run: undefined on iteration 0, kept on 1 and 2)
export default function () {
  if (!token) token = login(users[exec.vu.idInTest % users.length]);
  ...
}
```

## Other schemes
- Basic: `http.get('https://user:pass@api.test/x')` or `Authorization: Basic ${encoding.b64encode('u:p')}`.
- Digest: `{ auth: 'digest' }` param with credentials in URL. NTLM: `{ auth: 'ntlm' }`. These are the only two values with an effect; `auth: 'basic'` does nothing (k6 applies Basic auth automatically when the URL has `user:pass@`). Run: `http://user:pass@host/` sent `Authorization: Basic dXNlcjpwYXNz`, equal to `encoding.b64encode('user:pass')`. Digest and NTLM support is per the k6 `Params` docs (checked in the docs source).

## Cookies
Each VU has a cookie jar; cookies set by responses are sent automatically on later requests to matching domains, and the jar is **reset each iteration** (behaves like a new browser session). Control:
```js
const jar = http.cookieJar();
jar.set('https://app.test', 'consent', 'all');
http.get('https://app.test/', { cookies: { ab_variant: 'B' } });     // per request
http.get(url, { jar: new http.CookieJar() });                         // isolated, empty jar for this request
```
`{ jar: null }` does NOT bypass the jar: run on k6 2.3.0 it still sent the VU jar's cookies. Request-scoped `cookies` are sent in addition to the jar's cookies and are not stored in it (run: `ab_variant=B; sid=abc; consent=all`).
Keep session across iterations: set option `noCookiesReset: true` (run with 3 iterations: without it the second iteration started with no cookies, with it the cookies from iteration 1 were still sent).

## Gotchas
- `setup()` runs once per test; its return value is serialised (a function in it fails with `error marshaling setup() data to JSON`, run).
- Logging tokens to console leaks them into CI logs.

## Verify
IdP request count during the test matches the chosen model (once vs per VU vs per iteration).
