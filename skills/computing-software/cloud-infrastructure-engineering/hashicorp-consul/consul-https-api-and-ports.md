---
id: computing-software.cloud-infrastructure-engineering.hashicorp-consul.consul-https-api-and-ports
name: consul-https-api-and-ports
category: computing-software
field: cloud-infrastructure-engineering
product: hashicorp-consul
tags: [consul, https-api, consul-ports, consul-http-addr]
level: practitioner
status: docs-checked
description: "Turn on the Consul HTTPS port 8501, disable plaintext 8500 once clients are migrated, and set CLI environment for TLS and tokens."
sources: ["https://developer.hashicorp.com/consul/docs/agent/config/config-files", "https://developer.hashicorp.com/consul/commands/tls/cert"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
By default the HTTP API listens on 8500 in plaintext. In production serve HTTPS and disable HTTP.

```hcl
ports { http = -1, https = 8501, grpc = -1, grpc_tls = 8503 }
tls { defaults { verify_incoming = false } }   # clients may use server-auth-only TLS for HTTPS
```

```sh
export CONSUL_HTTP_ADDR=https://127.0.0.1:8501
export CONSUL_CACERT=/etc/consul.d/certs/consul-agent-ca.pem
export CONSUL_HTTP_TOKEN_FILE=/etc/consul.d/token
```

Gotchas: the HTTPS listener has its own `tls.https` block whose settings, including `verify_incoming`, override `tls.defaults`; it is only enabled when `ports.https` is defined. With `verify_incoming` true, clients including the CLI must present a certificate (`CONSUL_CLIENT_CERT` and `CONSUL_CLIENT_KEY`). `client_addr` defaults to 127.0.0.1, loopback only. `CONSUL_HTTP_TOKEN_FILE` reads the ACL token from a file instead of `CONSUL_HTTP_TOKEN`.

Verify: `curl --cacert ca.pem https://127.0.0.1:8501/v1/status/leader` returns the leader address, and `curl http://127.0.0.1:8500/v1/status/leader` fails to connect.

## Checked

2026-11-03. Confirmed against the ports reference (8500 HTTP enabled and 8501 HTTPS disabled by default, 8503 gRPC TLS), the general options page (ports keys, -1 disables, client_addr default), the TLS options page (tls.defaults, tls.https overrides, verify_incoming) and the consul command API options (CONSUL_CACERT, CONSUL_HTTP_ADDR, CONSUL_HTTP_TOKEN_FILE, CONSUL_CLIENT_CERT). Removed: the process-listing rationale and the staged rollout advice.

Method: documentation only; no commands were run.
