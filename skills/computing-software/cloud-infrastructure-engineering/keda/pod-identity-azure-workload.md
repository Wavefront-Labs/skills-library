---
id: computing-software.cloud-infrastructure-engineering.keda.pod-identity-azure-workload
name: pod-identity-azure-workload
category: computing-software
field: cloud-infrastructure-engineering
product: keda
tags: [azure-workload-identity, podidentity, federated-credential, identityid, keda-operator]
level: advanced
status: docs-checked
description: "Configure KEDA to authenticate with Azure AD Workload Identity: Helm flags, federated credential subject, and per-TriggerAuthentication identityId overrides."
sources:
  - https://keda.sh/docs/2.17/concepts/authentication/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Azure AD Workload Identity is the newer replacement for Azure AD Pod Identity and lets workloads use an Azure AD application through federated identity credentials, with no secrets. In a TriggerAuthentication set:

```yaml
podIdentity:
  provider: azure-workload
  identityId: <identity-id>
```

`identityId` is optional; the default is the client ID taken from the annotation on the service account.

Install-time setup: access is granted to pods whose service accounts carry the right labels and annotations, and you can place them on the KEDA operator service account. With Helm use:
1. `--set podIdentity.azureWorkload.enabled=true`
2. `--set podIdentity.azureWorkload.clientId={azure-ad-client-id}`
3. `--set podIdentity.azureWorkload.tenantId={azure-ad-tenant-id}`

`enabled=true` is required for workload identity to work. Also configure a federated credential on the target managed identity or Azure AD application, using the subject `system:serviceaccount:keda:keda-operator` when KEDA is installed in the `keda` namespace.

Overrides: specifying `identityId` under `podIdentity` replaces the identity assigned during installation, so different resources can use different identities, which is more secure than one identity with broad access. Each identity used needs its own federated credential. An empty ID in an override is rejected by the admission webhook.

## Checked

2026-11-03. Confirmed on the 2.17 Authentication page: azure-workload provider, Helm flags, federated credential subject, identityId override; webhook rule on the admission page.

Method: documentation only; no commands were run.
