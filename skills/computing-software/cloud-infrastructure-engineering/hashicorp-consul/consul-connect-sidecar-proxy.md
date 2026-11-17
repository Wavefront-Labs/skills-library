---
id: computing-software.cloud-infrastructure-engineering.hashicorp-consul.consul-connect-sidecar-proxy
name: consul-connect-sidecar-proxy
category: computing-software
field: cloud-infrastructure-engineering
product: hashicorp-consul
tags: [consul, sidecar-proxy, connect, envoy-sidecar]
level: practitioner
status: docs-checked
description: "Add a Consul Connect sidecar_service with upstreams, run the Envoy proxy, and check mTLS between two services."
sources: ["https://developer.hashicorp.com/consul/docs/services/configuration/services-configuration-reference", "https://developer.hashicorp.com/consul/docs/connect/intentions"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Register the service with a `sidecar_service` block and an upstream.

```hcl
service {
  name = "web"
  port = 8080
  connect {
    sidecar_service {
      proxy {
        upstreams = [{ destination_name = "api", local_bind_port = 9191 }]
      }
    }
  }
}
```

```sh
consul connect envoy -sidecar-for web
```

The app calls `localhost:9191` and the proxies handle mTLS and intentions.

Gotchas: do not configure `sidecar_service` when `native = true`. `consul connect envoy` needs the gRPC API reachable (gRPC uses the same TLS settings as the HTTPS API, so if HTTPS is enabled gRPC requires it too). With ACLs enabled, pass a token with `service:write` for the target service using `-token` or `CONSUL_HTTP_TOKEN`; the generated bootstrap JSON contains that token, so treat it as a secret. Envoy's admin API binds `localhost:19000` by default (`-admin-bind`).

Verify: `curl localhost:9191` from the web host reaches api, and `consul intention check web api` prints `Allowed`.

## Checked

2026-11-03. Confirmed against the service definition reference (native and sidecar_service are exclusive), the consul connect envoy command page (-sidecar-for, -admin-bind default, gRPC TLS note, ACL token requirement and secrecy of the bootstrap JSON) and the consul intention check page (Allowed or Denied output). Removed: the connect-enabled prefix, the kind advice, the 0.0.0.0 binding advice and the Envoy /clusters check, which the pages do not state.

Method: documentation only; no commands were run.
