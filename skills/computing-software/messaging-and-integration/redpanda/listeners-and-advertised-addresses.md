---
id: computing-software.messaging-and-integration.redpanda.listeners-and-advertised-addresses
name: listeners-and-advertised-addresses
category: computing-software
field: messaging-and-integration
product: redpanda
tags: [listeners, advertised-listeners, kafka-api, redpanda-yaml, rpc-server, pandaproxy]
level: practitioner
status: docs-checked
description: "Define Kafka API listeners and advertised addresses in redpanda.yaml: unique listener names, per-listener authentication_method and TLS, and listener to advertised pairs."
sources:
  - https://docs.redpanda.com/streaming/current/manage/security/listener-configuration/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
A listener is an interface address plus a TCP port. Clients must be able to reach every broker, so when client and broker sit on different subnets you must advertise a reachable location.

```yaml
redpanda:
  kafka_api:
    - address: 0.0.0.0
      port: 9092
```

**Advertise.** By default the advertised address equals the bound address. For outside clients set a routable IP or FQDN. `0.0.0.0` fails startup validation. A DNS name must resolve for clients and match the TLS certificate SAN.

```yaml
redpanda:
  advertised_kafka_api:
    - address: 192.168.4.1 # Broker’s routable IP or FQDN
      port: 9092
```

**Multiple listeners.** Give each listener a unique `name` and reuse that exact name in the matching advertised entry:

```yaml
redpanda:
  kafka_api:
    - name: local # Unique listener name
      address: 127.0.0.1
      port: 9092
    - name: subnet
      address: 192.168.4.1
      port: 9093
  advertised_kafka_api:
    - name: local # Must match the listener name
      address: 127.0.0.1
      port: 9092
    - name: subnet
      address: 192.168.4.1
      port: 9093
```

**Pairs that can be advertised**

| Listener | Advertised | Used by |
|---|---|---|
| `kafka_api` | `advertised_kafka_api` | Kafka clients |
| `rpc_server` | `advertised_rpc_api` | other brokers |
| `pandaproxy_api` | `advertised_pandaproxy_api` | HTTP proxy clients |

Each listener can set its own `authentication_method` (for example `sasl` on one port and `mtls_identity` on another), and TLS is configured per name under `kafka_api_tls`.

## Checked

2026-11-04. All YAML examples and the listener table were confirmed on the Configure Listeners page. The pairing of authentication_method with TLS is from the TLS listener and mixed-mode examples on the same page.

Method: documentation only; no commands were run.
