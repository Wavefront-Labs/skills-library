---
id: computing-software.cloud-infrastructure-engineering.rancher.agent-tls-mode-strict-vs-system-store
name: agent-tls-mode-strict-vs-system-store
category: computing-software
field: cloud-infrastructure-engineering
product: rancher
tags: [agent-tls-mode, strict, system-store, cacerts, agenttlsstrictcheck, global-settings]
level: advanced
status: docs-checked
description: "Understand agent-tls-mode strict versus system-store, the AgentTlsStrictCheck condition, how to check readiness with kubectl, and where the setting can be changed."
sources:
  - https://ranchermanager.docs.rancher.com/getting-started/installation-and-upgrade/installation-references/tls-settings
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The `agent-tls-mode` setting controls how Rancher's agents (`cluster-agent`, `fleet-agent`, `system-agent`) validate Rancher's certificate.

- `strict`: agents only trust certificates issued by the CA in the `cacerts` setting.
- `system-store`: agents trust any certificate from a public CA in the operating system trust store, including Let's Encrypt. The page flags this as a security risk because those authorities are outside your control.

New installs from Rancher v2.9.0 default to `strict`. Installs created earlier, and upgrades, are set to `system-store`. Strict needs Rancher to have access to the CA that issued the certificate agents see, which is not automatic for external certificates, so extra configuration (such as uploading the CA) may be needed before switching.

Each downstream cluster carries a status condition `AgentTlsStrictCheck`; `"True"` means its agents are ready for strict mode. The page gives this check:

```bash
kubectl get cluster.management.cattle.io -o jsonpath='{range .items[?(@.metadata.name!="local")]}{.metadata.name},{.status.conditions[?(@.type=="AgentTlsStrictCheck")].status}{"\n"}{end}'
```

Change the value on the **Global Settings** page (the `agent-tls-mode` row near the bottom) or with the `agentTLSMode` Helm option. If you set it through Helm you may only modify it with Helm. In the UI, Rancher first verifies every downstream cluster has `AgentTlsStrictCheck` true, which prevents certificate-mismatch outages.

## Checked

2026-11-04. Checked against the Rancher Manager documentation pages: TLS Settings (Agent TLS Enforcement). Nothing removed.

Method: documentation only; no commands were run.
