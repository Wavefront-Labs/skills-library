---
id: computing-software.cloud-infrastructure-engineering.garage.consul-service-discovery
name: consul-service-discovery
category: computing-software
field: cloud-infrastructure-engineering
product: garage
tags: [consul-discovery, service-registration, mtls, wan-federation]
level: advanced
status: docs-checked
description: "Configure the [consul_discovery] section with the catalog or agent API, TLS options and tokens."
sources:
  - https://garagehq.deuxfleurs.fr/documentation/reference-manual/configuration/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Garage can find peers through Consul. Nodes must know the address others can reach them on, so set `rpc_public_addr`.

Keys in `[consul_discovery]`:

- `consul_http_addr`: full HTTP(S) address of the Consul server.
- `api`: `"catalog"` (the default, registering via `/v1/catalog`) or `"agent"` (using `v1/agent`).
- `service_name`: the service name under which Garage's RPC ports are announced.
- `client_cert` and `client_key`: TLS client certificate and key; both are mandatory for TLS and only available with `api = "catalog"`, where they enable mTLS.
- `ca_cert`: CA certificate for TLS to Consul.
- `tls_skip_verify`: skips server hostname verification, and `ca_cert` is then ignored.
- `token`: token used for communication with Consul, only with `api = "agent"`. Its policy needs `service "garage"` with write, plus read on `service_prefix ""` and `node_prefix ""`.
- `datacenters`: list such as `["dc1", "dc2", "dc3"]` for WAN federation. Without it the Consul services API returns only local LAN services; with it Garage queries each datacenter directly.
- `tags` and `meta`: extra tags and service metadata added at registration.

## Checked

2026-11-04. Read the Configuration file format page in full. Confirmed every key of the section, the catalog default, the mTLS and agent token conditions, the token policy rules and the WAN datacenters behaviour. Removed the word bearer from the token description, which the page does not use.
Method: documentation only; no commands were run.
