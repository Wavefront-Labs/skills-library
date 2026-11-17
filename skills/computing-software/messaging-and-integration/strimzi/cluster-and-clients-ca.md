---
id: computing-software.messaging-and-integration.strimzi.cluster-and-clients-ca
name: cluster-and-clients-ca
category: computing-software
field: messaging-and-integration
product: strimzi
tags: [cluster-ca, clients-ca, internal-tls]
level: advanced
status: docs-checked
description: "Understand the two internal CAs that sign Strimzi certificates."
sources: ["https://strimzi.io/docs/operators/latest/deploying.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Cluster CA and clients CA

**Goal:** know which CA signs what.

Every Strimzi component needs private keys and certificates. All component certificates are signed by an internal CA, the **cluster CA**. A second internal CA, the **clients CA**, signs certificates for Kafka clients using mTLS. Both have self-signed public key certificates.

Trust rules:

- Brokers trust certificates signed by either CA.
- Components that clients do not connect to trust only the cluster CA.
- Unless TLS encryption is disabled on external listeners, client applications must trust certificates signed by the cluster CA, including clients doing mTLS.

By default the Cluster Operator generates and renews both CAs. Manage them with `Kafka.spec.clusterCa` and `Kafka.spec.clientsCa`:

```yaml
spec:
  clusterCa:
    validityDays: 365
    renewalDays: 30
    generateCertificateAuthority: true
  clientsCa:
    validityDays: 365
```

Defaults: validity 365 days and renewal 30 days before expiry. You can instead install your own CA certificates or use cert-manager to issue end-entity certificates; the Cluster Operator does not renew those.

**Checklist**

1. Distribute the cluster CA certificate to clients.
2. Keep generation on unless you supply your own CA.
3. Set validity per CA.

## Checked

Method: docs-checked 2026-11-09 against the Strimzi deploying guide (Internal cluster CA and clients CA; Certificate renewal and validity periods). The earlier early-access claim was dropped as unconfirmed.
