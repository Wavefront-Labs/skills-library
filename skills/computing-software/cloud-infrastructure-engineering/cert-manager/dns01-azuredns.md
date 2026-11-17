---
id: computing-software.cloud-infrastructure-engineering.cert-manager.dns01-azuredns
name: dns01-azuredns
category: computing-software
field: cloud-infrastructure-engineering
product: cert-manager
tags: [azuredns, azure, dns01, workload-identity, managed-identity, service-principal, aks]
level: advanced
status: docs-checked
description: "Configure cert-manager DNS01 with Azure DNS: workload identity (recommended), kubelet identity, service principal, required role and ambient-credential flags."
sources:
  - https://cert-manager.io/docs/configuration/acme/dns01/azuredns/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
All methods need the role "DNS Zone Contributor" on the DNS zone. Solver block: `dns01.azureDNS` with `hostedZoneName`, `resourceGroupName`, `subscriptionID`, `environment` (e.g. `AzurePublicCloud`).

1. Managed identity with AAD Workload Identity (recommended, v1.11.0+): `az aks update --enable-oidc-issuer --enable-workload-identity`; Helm `podLabels: azure.workload.identity/use: "true"`; create the identity with `az identity create`; federate it with `az identity federated-credential create` using the cluster OIDC `--issuer` and `--subject system:serviceaccount:cert-manager:cert-manager`. Issuer sets `managedIdentity.clientID` (optional `tenantID`), which override the injected `AZURE_CLIENT_ID`/`AZURE_TENANT_ID`.
2. AAD Pod Identity: deprecated since 10/24/2022. Needs `AzureIdentity` and `AzureIdentityBinding`; pod label `aadpodidbinding`; one identity per pod only.
3. AKS kubelet identity: grant the role to `identityProfile.kubeletidentity.objectId`. Every container in the cluster can then use it. With several node-pool identities set `managedIdentity.clientID` or `managedIdentity.resourceID` (mutually exclusive).
4. Service principal: `az ad sp create-for-rbac`, drop the broad Contributor role, then `clientID`, `clientSecretSecretRef` (`name`, `key: client-secret`) and `tenantID`.

Ambient credentials are on for ClusterIssuer (`--cluster-issuer-ambient-credentials`, default true) and off for Issuer (`--issuer-ambient-credentials=true`, not recommended). If off, you get the error "ClientID was omitted without providing one of" the ambient flags.

## Checked

2026-11-03. Confirmed on the cert-manager AzureDNS page (configuration/acme/dns01/azuredns): four methods, DNS Zone Contributor role, workload identity steps and v1.11.0 gate, podLabels, federated credential subject, managedIdentity overrides, Pod Identity deprecation date and single-identity limit, kubelet identity caveats and clientID or resourceID exclusivity, service principal steps, ambient credential flags and error text. Nothing removed.
Method: documentation only; no commands were run.
