---
id: computing-software.messaging-and-integration.strimzi.own-ca-certificates
name: own-ca-certificates
category: computing-software
field: messaging-and-integration
product: strimzi
tags: [custom-ca, replace-ca, renew-ca]
level: sme
status: docs-checked
description: "Install, replace and renew your own CA certificates and private keys."
sources: ["https://strimzi.io/docs/operators/latest/deploying.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Using your own CA certificates

**Goal:** supply CAs instead of the generated ones.

You can replace the cluster CA and clients CA certificates and private keys. Two paths:

- install your own **before** deploying the Kafka cluster, or
- replace the defaults **after** deployment.

The steps to replace the defaults are the same as the steps to renew your own CA material. With your own certificates, Strimzi does **not** renew them automatically; renew before they expire.

Renewal options:

1. Renew the CA certificates only.
2. Renew CA certificates and private keys (or replace the defaults).

Disable automatic generation so the operator uses your secrets:

```yaml
spec:
  clusterCa:
    generateCertificateAuthority: false
  clientsCa:
    generateCertificateAuthority: false
```

By default Strimzi uses `<cluster_name>-cluster-ca`, `<cluster_name>-cluster-ca-cert`, `<cluster_name>-clients-ca` and `<cluster_name>-clients-ca-cert`, renewed automatically. To install your own, create secrets with the same names (PEM X.509 certificate as `ca.crt`, key as `ca.key`), label them `strimzi.io/kind=Kafka` and `strimzi.io/cluster=<cluster_name>`, and annotate them `strimzi.io/ca-cert-generation` / `strimzi.io/ca-key-generation`, starting at 0 and increasing on each renewal. A non-root CA needs the whole chain in the certificate file (CA, intermediates, root).

**Checklist**

1. Set `generateCertificateAuthority: false`.
2. Calendar your renewal before expiry; the Cluster Operator will not renew your CA.
3. Use a higher generation annotation value on each renewal.

## Checked

Method: docs-checked 2026-11-09 against the Strimzi deploying guide (Using your own CA certificates and private keys, 18.7.1 and 18.7.2). The earlier rolling-update claim was dropped as unconfirmed.
