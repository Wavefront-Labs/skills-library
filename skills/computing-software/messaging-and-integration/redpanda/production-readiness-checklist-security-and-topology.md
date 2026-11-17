---
id: computing-software.messaging-and-integration.redpanda.production-readiness-checklist-security-and-topology
name: production-readiness-checklist-security-and-topology
category: computing-software
field: messaging-and-integration
product: redpanda
tags: [production-readiness, security, tls, authentication, replication-factor, maintenance-mode, advertised-listeners]
level: practitioner
status: docs-checked
description: "Pre-production security and topology checks: SASL, superusers, TLS on all listeners, advertised hostnames, auto-balancing, replication factor three, no brokers in maintenance."
sources:
  - https://docs.redpanda.com/streaming/current/deploy/redpanda/manual/production/production-readiness/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
- **Authentication:** `rpk cluster config get kafka_enable_authorization` should print `true`. Without SASL authentication anyone can potentially connect to the brokers.
- **Superusers:** confirm the Admin API is secured and users in `superusers` have strong credentials.
- **TLS:** every public interface needs TLS: Kafka API, Admin REST API, internal RPC server, Schema Registry and HTTP Proxy. Check the startup logs on each broker (`journalctl -u redpanda.service | grep tls`) for `enabled: 1` on `kafka_api_tls`, `admin_api_tls`, `rpc_server_tls`, `schema_registry_api_tls` and `pandaproxy_api_tls`. The Admin API endpoint `/v1/security/report` also produces a security report covering TLS, authentication and authorization:

```bash
curl 'http://localhost:9644/v1/security/report'
```

- **Advertised hostnames:** on multi-interface hosts set `advertised_kafka_api` to the public interface and `advertised_rpc_api` to the private one. Use hostnames, not IP addresses.
- **Auto-balancing:** `rpk cluster config get partition_autobalancing_mode` should print `continuous`.
- **Replication factor:** `rpk topic list` must show REPLICAS above 1. Set the floor and default to at least 3:

```bash
rpk cluster config set minimum_topic_replications=3
rpk cluster config set default_topic_replications=3
```

- **Maintenance and decommission:** `rpk cluster maintenance status` should show no broker in maintenance mode, and no broker should be left in a decommissioned state.
- **Support:** confirm `sudo rpk debug bundle` works on each host.

Recommended extras on the page: Prometheus, Grafana or Datadog scraping every broker, system logs kept at least 7 days, a regular rolling-upgrade policy, and multi-AZ deployment.

## Checked

Each check, command and the logging field names were confirmed on the Production Readiness Checklist page (Critical and Recommended requirements), read in full.

Method: docs-checked 2026-11-09 against the Production Readiness Checklist page, read in full; no commands were run.
