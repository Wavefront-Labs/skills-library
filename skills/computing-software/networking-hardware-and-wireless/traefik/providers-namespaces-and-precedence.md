---
id: computing-software.networking-hardware-and-wireless.traefik.providers-namespaces-and-precedence
name: providers-namespaces-and-precedence
category: computing-software
field: networking-hardware-and-wireless
product: traefik
tags: [networking-hardware-and-wireless, traefik, provider-namespace, cross-provider, precedence, at-suffix, providers]
level: practitioner
status: docs-checked
description: "Reference middlewares or services across Traefik providers with the name@provider suffix and settle cross-provider conflicts."
sources:
  - https://github.com/traefik/traefik/blob/master/docs/content/reference/install-configuration/providers/overview.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# providers namespaces and precedence
Providers fall into four categories: label-based, key-value-based, annotation-based and file-based. Objects declared in a provider (middlewares, services, TLS options, server transports) live in that provider's namespace. To reference an object from another provider, suffix its name with `@` and the provider name, such as `auth@file` or `redirect@docker`.

```yaml
# a Docker label using a middleware declared in a file
labels:
  - "traefik.http.routers.app.middlewares=secured@file"
```
Kubernetes has its own namespaces, which is a different concept. For a CRD-declared middleware used from a plain Ingress annotation, the Kubernetes namespace is part of the name, for example `ns-name@kubernetescrd` (with `safeNaming` enabled the separator becomes `_`, as the reference describes).

Gotchas: the Kubernetes namespace is not the provider namespace; when referencing a Kubernetes object cross-provider, the Kubernetes namespace is part of the name. When routes from different providers share the same numeric priority, `providers.precedence` (for example `--providers.precedence=kubernetescrd,kubernetes,file`) determines which route takes precedence.

## Checked
2026-11-03. Confirmed against the Traefik providers overview page: the four provider categories, provider namespaces, the `<resource-name>@<provider-name>` form, the Kubernetes namespace note with `safeNaming`, and `providers.precedence`. Removed: the claims that router names cannot contain `@` (confirmed only for TCP routers elsewhere), that unsuffixed names resolve in the same provider, and the dashboard Verify step.
Method: documentation only; no commands were run.


