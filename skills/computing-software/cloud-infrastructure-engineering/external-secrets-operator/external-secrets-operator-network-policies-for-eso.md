---
id: computing-software.cloud-infrastructure-engineering.external-secrets-operator.external-secrets-operator-network-policies-for-eso
name: external-secrets-operator-network-policies-for-eso
category: computing-software
field: cloud-infrastructure-engineering
product: external-secrets-operator
tags: [security, networkpolicy, egress, exfiltration]
level: advanced
status: docs-checked
description: "Write default-deny NetworkPolicies for the ESO core controller, webhook and cert controller with the documented ports."
sources:
  - https://raw.githubusercontent.com/external-secrets/external-secrets/main/docs/guides/security-best-practices.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
ESO ships no NetworkPolicies, and a badly restricted ESO can be used to exfiltrate data. Default deny, then allow:

- Core controller: egress to the kube-apiserver and the secret provider (prefer private endpoints); ingress on 8080 from the monitoring agent.
- Cert controller: egress to the kube-apiserver; ingress on 8080 from monitoring and 8081 from the kubelet for healthz and readyz.
- Webhook: egress to the kube-apiserver; ingress on 10250 from the kube-apiserver, 8080 from monitoring, 8081 from the kubelet.

Review policies when infrastructure changes. Combine with a policy engine, and disable any provider you do not use.

## Checked

2026-11-03. Claims were read against guides/security-best-practices.md in the external-secrets docs source. Removed: nothing.

Method: documentation only; no commands were run.
