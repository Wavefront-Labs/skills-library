---
id: computing-software.networking-hardware-and-wireless.traefik.middleware-errors
name: middleware-errors
category: computing-software
field: networking-hardware-and-wireless
product: traefik
tags: [networking-hardware-and-wireless, traefik, errors, error-pages, statusrewrites, custom-error-page, middleware]
level: practitioner
status: docs-checked
description: "Serve custom error pages from another service with the errors middleware, status ranges and the query template variables."
sources:
  - https://github.com/traefik/traefik/blob/master/docs/content/reference/routing-configuration/http/middlewares/errorpages.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# middleware errors
The `errors` middleware returns a custom page instead of the default for configured status codes. Options: `status` (required in practice: codes, comma-separated codes, dash ranges, or a mix such as `404,418,505-599`; ranges are inclusive), `statusRewrites` (map codes or ranges to a different status), `service` (required; serves the page), `query` (URL of the page on that service) and `errorRequestHeaders`.

```yaml
http:
  middlewares:
    test-errors:
      errors:
        status:
          - "500"
          - "501"
          - "503"
          - "505-599"
        statusRewrites:
          "418": 404
          "502-504": 500
        service: error-handler-service
        query: "/{status}.html"
```
`query` variables: `{status}` (the response status), `{originalStatus}` (the original status if `statusRewrites` changed it) and `{url}` (the escaped request URL).

Gotchas: by default the client `Host` header is forwarded to the error service; set `passHostHeader: false` on the service to send the error service's own host. By default all request headers, including `Authorization` and `Cookie`, are forwarded to the error service; if it is in a separate trust domain, set `errorRequestHeaders` to an explicit list (an empty list forwards none). On Kubernetes, set `serversTransport` on the middleware's `service` to customise the connection; the Service annotation is not applied there.

## Checked
2026-11-03. Confirmed against the Traefik errors reference page (docs/content/reference/routing-configuration/http/middlewares/errorpages.md): options, status syntax, statusRewrites, query variables, Host and errorRequestHeaders behaviour, serversTransport note. Removed: the unsourced loop warning about the error router, and the invented Verify step.
Method: documentation only; no commands were run.
