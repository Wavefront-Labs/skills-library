---
id: computing-software.web-development.node-express.csp-nonces-in-frameworks
name: csp-nonces-in-frameworks
category: computing-software
field: web-development
product: node-express
tags: [csp-nonce-middleware, content-security-policy, helmet-csp, django-csp, rails-csp, nextjs-csp]
level: advanced
status: verified
description: "Per-request CSP nonces in Express (helmet), Next.js middleware, Django and Rails: generating, propagating to templates and framework scripts, and caching conflicts."
sources:
  - https://helmetjs.github.io/#content-security-policy
  - https://nextjs.org/docs/app/guides/content-security-policy
  - https://guides.rubyonrails.org/security.html#content-security-policy-header
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# CSP nonces in frameworks

A nonce must be random (>= 128 bits), new for every response, and present on every script you trust. Combine with `'strict-dynamic'` so scripts those load are trusted too.

## 1. Express + helmet
Ran on helmet 8.3.0: two requests returned different nonces; note helmet also keeps its default directives (`default-src 'self'`, `style-src 'self' https: 'unsafe-inline'`, `upgrade-insecure-requests`, ...) alongside your `script-src`, so review the whole header.
```js
import crypto from "node:crypto"; import helmet from "helmet";
app.use((req, res, next) => { res.locals.cspNonce = crypto.randomBytes(16).toString("base64"); next(); });
app.use(helmet({ contentSecurityPolicy: { directives: {
  scriptSrc: [(req, res) => `'nonce-${res.locals.cspNonce}'`, "'strict-dynamic'"],
  objectSrc: ["'none'"], baseUri: ["'none'"],
}}}));
// template: <script nonce="<%= cspNonce %>" src="/app.js"></script>
```

## 2. Next.js (App Router)
Generate the nonce in the request interceptor (`proxy.ts` in current Next.js docs; the same function was `middleware.ts` before the rename), set it on the CSP response header and a request header:
```ts
export function proxy(req: NextRequest) {
  const nonce = Buffer.from(crypto.randomUUID()).toString("base64");
  const csp = `script-src 'self' 'nonce-${nonce}' 'strict-dynamic'; object-src 'none'; base-uri 'none';`;
  const headers = new Headers(req.headers);
  headers.set("x-nonce", nonce); headers.set("Content-Security-Policy", csp);
  const res = NextResponse.next({ request: { headers } });
  res.headers.set("Content-Security-Policy", csp);
  return res;
}
```
Next.js reads the nonce from the CSP header and applies it to its own scripts; read `(await headers()).get("x-nonce")` for `<Script nonce>`. Pages using nonces must render dynamically: static/ISR HTML would reuse one nonce.

## 3. Django
Django 6.0 includes CSP support (`django.middleware.csp.ContentSecurityPolicyMiddleware`, `SECURE_CSP` with `django.utils.csp.CSP.NONCE`, `{{ csp_nonce }}` via the `django.template.context_processors.csp` context processor; ran on 6.1.2: a fresh nonce per request, in header and template); earlier versions use `django-csp`:
```python
# django-csp 4.0 (ran: fresh nonce per request; note it also added `default-src 'self'`)
from csp.constants import SELF, NONCE, STRICT_DYNAMIC
CONTENT_SECURITY_POLICY = {"DIRECTIVES": {"script-src": [SELF, NONCE, STRICT_DYNAMIC], "object-src": ["'none'"]}}
# template: <script nonce="{{ request.csp_nonce }}">
```

## 4. Rails
```ruby
# config/initializers/content_security_policy.rb
Rails.application.configure do
  config.content_security_policy { |p| p.script_src :self, :strict_dynamic; p.object_src :none }
  config.content_security_policy_nonce_generator = ->(request) { SecureRandom.base64(16) }
  config.content_security_policy_nonce_directives = %w[script-src]
end
```
```erb
<%= csp_meta_tag %>
<%= javascript_importmap_tags %>          <%# importmap-rails passes request.content_security_policy_nonce to its tags (checked in its source) %>
<%= javascript_tag nonce: true do %>...<% end %>
```
`csp_meta_tag` renders a `csp-nonce` meta tag (Action View docs: used by Rails UJS for dynamically inserted inline scripts). Use a random per-request value as the generator, as in the Rails security guide.

## 5. Caching conflicts
Full-page caches (CDN, Varnish, Rails/Django page cache) replay one nonce to everyone, which defeats it. Options: hash-based CSP for static pages, generate the nonce at the edge and rewrite HTML (edge workers), or do not page-cache nonce pages.

## Verify
- [ ] Two consecutive requests return different nonces in header and HTML.
- [ ] Inline script without the nonce is blocked (console CSP violation).
