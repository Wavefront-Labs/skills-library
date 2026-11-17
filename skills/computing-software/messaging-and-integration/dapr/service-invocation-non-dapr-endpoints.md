---
id: computing-software.messaging-and-integration.dapr.service-invocation-non-dapr-endpoints
name: service-invocation-non-dapr-endpoints
category: computing-software
field: messaging-and-integration
product: dapr
tags: [service-invocation, httpendpoint, external-http, tls, client-certificate, fqdn, resiliency, brownfield]
level: practitioner
status: docs-checked
description: "Call non-Dapr HTTP services via the invoke API with an HTTPEndpoint or full URL, the precedence over app IDs, and clientTLS with rootCA or certificate and key."
sources:
  - https://github.com/dapr/docs/blob/v1.15/daprdocs/content/en/developing-applications/building-blocks/service-invocation/howto-invoke-non-dapr-endpoints.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Service invocation also reaches plain HTTP services, so brownfield or external endpoints gain resiliency policies, tracing and metrics, scoping, middleware, discovery and header-based authentication.

Two ways to name the target:

```sh
localhost:3500/v1.0/invoke/<HTTPEndpoint-name>/method/<my-method>
localhost:3500/v1.0/invoke/<URL>/method/<my-method>
```

For example `curl http://localhost:3500/v1.0/invoke/palpatine/method/order66` for an HTTPEndpoint called palpatine, or `curl http://localhost:3500/v1.0/invoke/https://darthsidious.starwars/method/order66` for a fully qualified URL with an `http://` or `https://` prefix. Dapr apps are still called by app ID: `curl http://localhost:3602/v1.0/invoke/orderprocessor/method/checkout`.

Precedence when the runtime resolves the name:

1. A named `HTTPEndpoint` resource.
2. An FQDN URL with `http://` or `https://`.
3. An `appID`.

TLS: an HTTPEndpoint accepts any combination of root certificate, client certificate and private key. Root CA only:

```yaml
apiVersion: dapr.io/v1alpha1
kind: HTTPEndpoint
metadata:
  name: "external-http-endpoint-tls"
spec:
  baseUrl: https://service-invocation-external:443
  headers:
  - name: "Accept-Language"
    value: "en-US"
  clientTLS:
    rootCA:
      secretKeyRef:
        name: dapr-tls-client
        key: ca.crt
```

The page's second example uses a client certificate and private key instead of `rootCA`: `certificate` (`secretKeyRef` name `dapr-tls-client`, key `tls.crt`) and `privateKey` (name `dapr-tls-key`, key `tls.key`).

## Checked

2026-11-08. Benefits list, both URL forms and examples, precedence order, appId call and both clientTLS examples confirmed on the Invoke Non-Dapr Endpoints page. Changed: stopped calling the client certificate example mutual TLS, a label the page does not use.

Method: documentation only; every cited page read in full; no commands were run.
