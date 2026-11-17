---
id: computing-software.messaging-and-integration.strimzi.nodeport-listener
name: nodeport-listener
category: computing-software
field: messaging-and-integration
product: strimzi
tags: [nodeport-listener, external-access, preferrednodeportaddresstype]
level: advanced
status: docs-checked
description: "Expose Kafka outside the cluster through node ports."
sources: ["https://strimzi.io/docs/operators/latest/deploying.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Node port listener

**Goal:** give external clients access through Kubernetes node ports.

Clients need a bootstrap hostname and port plus the certificate used for TLS. Configure a `nodeport` listener in the `Kafka` resource:

```yaml
spec:
  kafka:
    listeners:
      - name: external4
        port: 9094
        type: nodeport
        tls: true
        authentication:
          type: tls
```

Use listener `tls` to enable encryption and `authentication` to choose the client mechanism. Extra `configuration` properties for nodeport listeners:

- `preferredNodePortAddressType`: the first address type checked as the node address.
- `externalTrafficPolicy`: whether the service routes to node-local or cluster-wide endpoints.
- `nodePort`: overrides assigned node port numbers for the bootstrap and broker services.

The service names follow the naming rules, for example `my-cluster-kafka-external4-bootstrap`. Related guidance: Strimzi has a troubleshooting section for TLS hostname verification with node ports.

**Checklist**

1. Open firewall access to the node ports.
2. Decide the node address type clients will use.
3. Distribute the cluster CA certificate to clients.

## Checked

2026-11-03. Confirmed in Accessing Kafka using node ports: nodeport listener example and the preferredNodePortAddressType, externalTrafficPolicy and nodePort configuration properties.

Method: documentation only; no commands were run.
