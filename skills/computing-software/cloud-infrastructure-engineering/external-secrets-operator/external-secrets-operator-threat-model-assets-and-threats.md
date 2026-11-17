---
id: computing-software.cloud-infrastructure-engineering.external-secrets-operator.external-secrets-operator-threat-model-assets-and-threats
name: external-secrets-operator-threat-model-assets-and-threats
category: computing-software
field: cloud-infrastructure-engineering
product: external-secrets-operator
tags: [threat-model, assets, controls, exfiltration]
level: sme
status: docs-checked
description: "Use the ESO threat model assets A01-A04, threats T01-T07 and controls C01-C05 to assess an installation."
sources:
  - https://raw.githubusercontent.com/external-secrets/external-secrets/main/docs/guides/threat-model.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Scope: a Helm install with default settings on a public cloud. ESO has three components: webhook, cert controller and core controller. Validation by the webhook is not a security control. Data classification is Critical with highest impact organisation takeover.

Assets: A01 cluster-level read/write access to Secrets; A02 cert-controller write access to ValidatingWebhookConfigurations and CRDs (to inject caBundle); A03 provider credentials (env vars, mounted tokens, files or Kubernetes Secrets); A04 the conversion webhook's ability to modify resources.

Threats: T01 MITM tampering of the webhook; T02 webhook DoS (it does not authenticate the apiserver); T03 stolen controller token reading cluster secrets; T04 over-broad provider credentials; T05 exfiltration through crafted resources (copy across namespaces, to an unauthorised provider, or to a malicious account of an authorised provider); T06 supply chain; T07 malicious workloads in the ESO namespace.

Controls: C01 NetworkPolicy deny-all; C02 least-privilege RBAC and provider-side permissions; C03 policy engine (restrict providers, auth mechanisms, security-relevant fields such as `caBundle`, `region`, `role`, `url`, and namespaceSelector usage); C04 provider access policy such as VPC endpoint policies; C05 disable unused CRDs.

## Checked

2026-11-03. Claims were read against guides/threat-model.md in the external-secrets docs source. Removed: nothing.

Method: documentation only; no commands were run.
