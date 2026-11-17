---
id: computing-software.cloud-infrastructure-engineering.gateway-api.http-to-https-redirect
name: http-to-https-redirect
category: computing-software
field: cloud-infrastructure-engineering
product: gateway-api
tags: [httproute, https-redirect, listener, sectionname, tls, requestredirect]
level: practitioner
status: docs-checked
description: "Redirect HTTP to HTTPS: Gateway with both http and https listeners, a redirect HTTPRoute pinned to the http listener, and a separate Route on https for the backends."
sources:
  - https://github.com/kubernetes-sigs/gateway-api/blob/main/site/content/en/guides/user-guides/http-redirect-rewrite.md
  - https://github.com/kubernetes-sigs/gateway-api/blob/main/site/content/en/guides/getting-started/migrating-from-ingress.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Pattern: one Gateway with two listeners, two HTTPRoutes.

Gateway (sketch):

```yaml
listeners:
- name: http
  protocol: HTTP
  port: 80
- name: https
  protocol: HTTPS
  port: 443
  tls:
    mode: Terminate
    certificateRefs:
    - name: redirect-example   # a Secret
```

Redirect route, attached only to the HTTP listener via `sectionName`:

```yaml
kind: HTTPRoute
spec:
  parentRefs:
  - name: <gateway-name>
    sectionName: http
  hostnames: ["redirect.example"]
  rules:
  - filters:
    - type: RequestRedirect
      requestRedirect:
        scheme: https
        statusCode: 301
```

A second HTTPRoute attaches to listener `https` and forwards to the application backends.

The guide needs a Gateway with both HTTP and HTTPS listeners; one HTTPRoute attached to the HTTP listener (via `sectionName: http`) does the redirect, and another attached to the HTTPS listener forwards to the application backends. The guide secures the Gateway with a Kubernetes Secret in `certificateRefs`, and notes there are multiple ways to secure a Gateway.

Status codes: 301 (permanent) is typical for an HTTP to HTTPS upgrade; 302 is the default if none is specified. A redirect keeps the original hostname, path and port, so `GET http://redirect.example/cinnamon` gets a 301 with `location: https://redirect.example/cinnamon`.

Migration note: in Ingress this was an implementation annotation (the migration guide's example uses `example-ingress-controller.example.org/tls-redirect`). Request redirects, including TLS redirect, are now part of Gateway API (HTTPRoute), via the filter and `statusCode` / `scheme` fields.

Also scope the redirect Route by `hostnames` so it covers exactly the intended domains (the migration guide's redirect Route covers `foo.example.com` and `bar.example.com`, attached to the `http` listener).

## Checked

2026-11-08. Read in full: the HTTP path redirects and rewrites guide and the Migrating from Ingress guide (raw markdown on GitHub), and the guide's redirect example manifest. Confirmed: Gateway with HTTP and HTTPS listeners, redirect HTTPRoute pinned to the http listener with sectionName, a separate HTTPRoute on the HTTPS listener, requestRedirect scheme https with statusCode 301, 302 as the default code, URL components preserved, the Secret in certificateRefs, and the Ingress annotation-to-native-filter mapping. Removed: the cleartext-traffic argument for two Routes, which is not stated on the pages. The Gateway snippet is a condensed sketch.

Method: documentation only; no commands were run.
