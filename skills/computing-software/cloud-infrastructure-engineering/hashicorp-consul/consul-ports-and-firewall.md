---
id: computing-software.cloud-infrastructure-engineering.hashicorp-consul.consul-ports-and-firewall
name: consul-ports-and-firewall
category: computing-software
field: cloud-infrastructure-engineering
product: hashicorp-consul
tags: [consul, consul-ports, firewall, rpc-8300]
level: practitioner
status: docs-checked
description: "List the Consul ports (8300 RPC, 8301 and 8302 gossip, 8500 and 8501 HTTP/HTTPS, 8502 and 8503 gRPC, 8600 DNS) with defaults and what to allow."
sources: ["https://developer.hashicorp.com/consul/docs/reference/architecture/ports", "https://developer.hashicorp.com/consul/docs/reference/agent/configuration-file/general"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Server agent defaults from the ports reference:

```text
8300 TCP        Server RPC          enabled   servers <-> servers; clients -> servers in the same datacenter
8301 TCP+UDP    LAN Serf            enabled   servers and clients in the datacenter
8302 TCP+UDP    WAN Serf            enabled   servers in a federated network
8500 TCP        HTTP API            enabled   (CLI uses it by default)
8501 TCP        HTTPS API           disabled  enable in agent config or `consul agent`
8502 TCP        gRPC                disabled  Consul Dataplane; gRPC TLS is recommended instead
8503 TCP        gRPC TLS            enabled on servers, disabled on clients
8600 TCP+UDP    DNS                 enabled
```

On client agents the same ports apply, except gRPC TLS (8503) is disabled by default.

Details:
- With WAN federation and no mesh gateways, 8300 and 8302 need incoming and outgoing traffic between all federated servers. With mesh gateways, servers must accept 8300 and 8302 traffic from the local mesh gateways.
- 8500, 8501 and 8600 on servers need not be open when clients serve the HTTP(S) API and DNS calls; Consul does not use those ports for internal communication.
- With recursors configured, you need outbound access to the upstream DNS servers on port 53.
- With Enterprise admin partitions, all clients in all partitions still need access to 8301 on all servers, and servers need access to 8301 on all clients.
- Sidecar proxies get automatically assigned ports from `ports.sidecar_min_port` (default 21000) to `ports.sidecar_max_port` (default 21255); `0` disables automatic assignment.
- The `http`, `https`, `dns` and `grpc` listener addresses default to `client_addr`.

## Checked

2026-11-03. Confirmed against the Consul v1.22 docs source: reference/architecture/ports (all ports, protocols, defaults, server and client differences) and reference/agent/configuration-file/general (sidecar port range, listener addresses). Fixed: the old list said 8501 was a normal open port (it is disabled by default), 8502 was the gRPC default with 8503 as an alternative (8503 is the enabled gRPC TLS port on servers), and 8500/8501 were TCP only without noting defaults. Removed: the `nc` Verify step, the claims about UDP flapping and cloud security groups, and the "confirm" markers.
Method: documentation only; no commands were run.
