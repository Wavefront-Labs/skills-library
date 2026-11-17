---
id: computing-software.messaging-and-integration.strimzi.ca-validity-and-renewal
name: ca-validity-and-renewal
category: computing-software
field: messaging-and-integration
product: strimzi
tags: [validitydays, renewaldays, certificate-renewal]
level: sme
status: docs-checked
description: "Set CA validity and renewal periods and understand renewal behaviour."
sources: ["https://strimzi.io/docs/operators/latest/deploying.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# CA validity and renewal

**Goal:** renew certificates before they expire.

CA certificates have a validity period, counted in days from generation. For CAs the Cluster Operator creates:

- `Kafka.spec.clusterCa.validityDays` and `Kafka.spec.clientsCa.validityDays`: default **365 days**.
- `Kafka.spec.clusterCa.renewalDays` and `Kafka.spec.clientsCa.renewalDays`: default **30 days** before expiry of the current certificate.

```yaml
spec:
  clusterCa:
    validityDays: 365
    renewalDays: 30
  clientsCa:
    validityDays: 365
    renewalDays: 30
```

When a CA certificate expires, components and clients trusting the old one reject peers signed by the new CA key. To avoid loss of service the operator renews before expiry. Changing `validityDays` does **not** trigger immediate renewal; it applies the next time the certificate is renewed, automatically or manually.

Manually installed custom CA certificates take validity from your own certificate system and are not renewed automatically.

For user certificates in `KafkaUser`, `validityDays` and `renewalDays` must be configured together, with `renewalDays` less than `validityDays`.

**Checklist**

1. Keep renewal window long enough for rollouts.
2. Expect rolling restarts when CAs renew.
3. Check restart reasons such as `CaCertRenewed`.

## Checked

2026-11-03. Confirmed in the CA certificate renewal section: clusterCa/clientsCa validityDays 365 and renewalDays 30 defaults, no immediate renewal when validityDays changes, custom CAs managed externally, KafkaUser validityDays/renewalDays rules, and the CaCertRenewed restart reason.

Method: documentation only; no commands were run.
