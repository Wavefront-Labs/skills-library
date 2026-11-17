---
id: computing-software.networking-hardware-and-wireless.traefik.middleware-grpcweb-and-encodedcharacters
name: middleware-grpcweb-and-encodedcharacters
category: computing-software
field: networking-hardware-and-wireless
product: traefik
tags: [networking-hardware-and-wireless, traefik, grpcweb, encodedcharacters, allowencodedslash, path-security, middleware]
level: practitioner
status: docs-checked
description: "Configure grpcWeb allowOrigins and relax encoded path character rejection with the encodedCharacters middleware."
sources:
  - https://github.com/traefik/traefik/blob/master/docs/content/reference/routing-configuration/http/middlewares/grpcweb.md
  - https://github.com/traefik/traefik/blob/master/docs/content/reference/routing-configuration/http/middlewares/encodedcharacters.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# middleware grpcweb and encodedcharacters
`grpcWeb` converts gRPC Web requests to HTTP/2 gRPC requests before forwarding them; Traefik must talk gRPC to the backends (h2c or HTTP/2 over TLS). It has one option, `allowOrigins`: a list of allowed origins (default empty); a `*` wildcard matches all requests.

`encodedCharacters` controls which ambiguous encoded characters are allowed in the request path. By default potentially dangerous encoded characters are rejected. Options, all default `false`: `allowEncodedSlash` (`%2F`), `allowEncodedBackSlash` (`%5C`), `allowEncodedSemicolon` (`%3B`), `allowEncodedPercent` (`%25`), `allowEncodedQuestionMark` (`%3F`) and `allowEncodedHash` (`%23`).

```yaml
http:
  middlewares:
    web:
      grpcWeb:
        allowOrigins: ["https://app.example.com"]
    test-encodedchars:
      encodedCharacters:
        allowEncodedSlash: true
```
Gotcha: before enabling an option, check that your backend is fully compliant with RFC 3986, so Traefik and the backend do not interpret the same URL differently (split view).

## Checked
2026-11-03. Confirmed against the Traefik grpcWeb and encodedCharacters reference pages (docs/content/reference/routing-configuration/http/middlewares/grpcweb.md and encodedcharacters.md): options, defaults, encodings, wildcard and the RFC 3986 warning. Removed: the entrypoint `http.encodedCharacters` remark, the "single option on its own router" advice, and the Verify step. Description rewritten to match.
Method: documentation only; no commands were run.
