---
id: computing-software.web-development.node-express.cors-configuration-across-frameworks
name: cors-configuration-across-frameworks
category: computing-software
field: web-development
product: node-express
tags: [cors-middleware, django-cors-headers, rack-cors, express-cors, nextjs-cors, cors]
level: practitioner
status: verified
description: "Configuring CORS correctly in Express (cors), Django (django-cors-headers), Rails (rack-cors) and Next.js route handlers/middleware, including preflight, credentials and errors."
sources:
  - https://github.com/expressjs/cors#readme
  - https://github.com/adamchainz/django-cors-headers
  - https://github.com/cyu/rack-cors
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# CORS configuration across frameworks

Common shape: explicit origin allowlist, `credentials` only if cookies are needed, preflight cached with `max-age`, CORS headers on error responses too.

## 1. Express
```js
import cors from "cors";
const corsOpts = {
  origin: ["https://app.example.com", "https://admin.example.com"],
  credentials: true, methods: ["GET", "POST", "PATCH", "DELETE"],
  allowedHeaders: ["Content-Type", "Authorization", "X-Requested-With"], maxAge: 600,
};
app.use(cors(corsOpts));          // before routes, so preflight OPTIONS and errors get headers
```
Express 5 wildcard syntax for explicit OPTIONS routes: `app.options("/{*splat}", cors(corsOpts))`. Ran on express 5.3.0 and cors 2.8.6: allowed-origin preflight returns 204 with `Access-Control-Allow-Origin`, `-Credentials`, `-Methods`, `-Headers`, `-Max-Age: 600` and `Vary: Origin`; a 500 from error middleware still carried the CORS headers. A foreign origin's preflight still returns 204 with the methods/headers/max-age headers but WITHOUT `Access-Control-Allow-Origin`, so the browser blocks it (the check below is about that header).

## 2. Django
```python
INSTALLED_APPS += ["corsheaders"]
MIDDLEWARE.insert(0, "corsheaders.middleware.CorsMiddleware")   # above CommonMiddleware
CORS_ALLOWED_ORIGINS = ["https://app.example.com"]
CORS_ALLOW_CREDENTIALS = True
CORS_URLS_REGEX = r"^/api/.*$"
CORS_PREFLIGHT_MAX_AGE = 600
```
With cookies cross-origin you also need `CSRF_TRUSTED_ORIGINS` and `SESSION_COOKIE_SAMESITE = "None"` + `Secure`. Ran on django-cors-headers 4.9.0: a preflight to `/api/x` from the allowed origin returns **200** (not 204) with the allow headers; the foreign origin and a path outside `CORS_URLS_REGEX` get no CORS headers.

## 3. Rails
```ruby
# config/initializers/cors.rb
Rails.application.config.middleware.insert_before 0, Rack::Cors do
  allow do
    origins "https://app.example.com"
    resource "/api/*", headers: :any, methods: %i[get post patch delete options], credentials: true, max_age: 600
  end
end
```

## 4. Next.js
Route handlers set headers themselves and export `OPTIONS`:
```ts
const ALLOWED = new Set(["https://app.example.com"]);
function cors(req: Request) {
  const o = req.headers.get("origin") ?? "";
  return ALLOWED.has(o) ? { "Access-Control-Allow-Origin": o, "Access-Control-Allow-Credentials": "true", Vary: "Origin" } : {};
}
export async function OPTIONS(req: Request) {
  return new Response(null, { status: 204, headers: { ...cors(req), "Access-Control-Allow-Methods": "GET,POST", "Access-Control-Allow-Headers": "Content-Type", "Access-Control-Max-Age": "600" } });
}
export async function GET(req: Request) { return Response.json(data, { headers: cors(req) }); }
```
`next.config.js` `headers()` can only set static values (fine for one origin); dynamic allowlists need handlers or middleware.

## 5. Failure modes
- 500 responses without CORS headers surface in the browser as "CORS error", hiding the real error; make sure error middleware runs inside the CORS layer.
- Reverse proxies/CDNs answering OPTIONS themselves or stripping headers; caches without `Vary: Origin` serve one origin's header to another.
- Same-origin deployments (front-end and API on one domain via a proxy path) need no CORS at all; often the simplest fix.

## Verify
- [ ] `curl -X OPTIONS -H "Origin: https://app.example.com" -H "Access-Control-Request-Method: POST" -i` returns 2xx (204 on Express and Next.js, 200 on django-cors-headers) with the allow headers; a foreign origin gets no `Access-Control-Allow-Origin`.
