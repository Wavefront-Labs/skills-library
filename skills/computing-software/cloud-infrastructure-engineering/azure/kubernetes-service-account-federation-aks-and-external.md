---
id: computing-software.cloud-infrastructure-engineering.azure.kubernetes-service-account-federation-aks-and-external
name: kubernetes-service-account-federation-aks-and-external
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, workload-identity-federation, kubernetes-federation, service-account-federation, aks, workload-identity, oidc-issuer]
level: advanced
status: docs-checked
description: "Federate Kubernetes service accounts to Entra: AKS OIDC issuer + workload identity webhook, and self-managed/EKS/GKE clusters using their issuer with the azure-workload-identity webhook."
sources: ["https://learn.microsoft.com/azure/aks/workload-identity-deploy-cluster", "https://learn.microsoft.com/azure/aks/workload-identity-overview", "https://learn.microsoft.com/azure/aks/workload-identity-migrate-from-pod-identity", "https://azure.github.io/azure-workload-identity/docs/", "https://azure.github.io/azure-workload-identity/docs/installation/self-managed-clusters.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Kubernetes service account federation (AKS and external clusters)

**Goal:** a pod authenticates to Azure as a specific managed identity based on its namespace and
service account, with no secrets mounted.

## AKS
```bash
az aks update -g rg -n aks1 --enable-oidc-issuer --enable-workload-identity
ISSUER=$(az aks show -g rg -n aks1 --query oidcIssuerProfile.issuerUrl -o tsv)
az identity create -g rg -n id-orders
CLIENT_ID=$(az identity show -g rg -n id-orders --query clientId -o tsv)
az identity federated-credential create -g rg --identity-name id-orders -n aks1-orders \
  --issuer "$ISSUER" --subject system:serviceaccount:orders:orders-sa --audience api://AzureADTokenExchange
```
```yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  name: orders-sa
  namespace: orders
  annotations: { azure.workload.identity/client-id: "<CLIENT_ID>" }
---
# pod template
metadata:
  labels: { azure.workload.identity/use: "true" }   # label, on the POD, not the SA
spec:
  serviceAccountName: orders-sa
```
The mutating webhook (only for pods labelled `azure.workload.identity/use: "true"`) injects a projected token volume and sets `AZURE_FEDERATED_TOKEN_FILE` (plus the client and tenant ID variables). `DefaultAzureCredential` picks it up; read the token path from the variable rather than hard-coding it.

## External / self-managed clusters (EKS, GKE, kubeadm, Arc)
1. Use the cluster's OIDC issuer URL: EKS and GKE clusters have one by default (EKS: `aws eks describe-cluster --name <cluster> --query "cluster.identity.oidc.issuer" --output text`), or host your own: generate a key pair, set the API server flags `--service-account-issuer`, `--service-account-key-file` and `--service-account-signing-key-file`, and publish the OpenID discovery document and the JWKS at the issuer URL.
2. Install the webhook: `helm repo add azure-workload-identity https://azure.github.io/azure-workload-identity/charts`, then `helm install workload-identity-webhook azure-workload-identity/workload-identity-webhook --namespace azure-workload-identity-system --create-namespace --set azureTenantID=<tenant>`.
3. Create the FIC with that issuer and `system:serviceaccount:<ns>:<sa>` subject; annotate SA and label pods as above.

## Gotchas
- Pods created before the label/annotation existed need restart — injection happens at admission.
- One identity for many clusters needs one FIC per cluster issuer, and a managed identity can have at most 20 FICs; AKS identity bindings let multiple clusters share one identity through a single FIC.
- A new issuer URL (for example a recreated self-managed cluster) invalidates the FICs created for the old one.
- By default the token volume is added to all containers of a labelled pod; list containers to skip in the `azure.workload.identity/skip-containers` pod annotation (semicolon-separated).
- Migrating from AAD Pod Identity (deprecated 2022, archived 2023): move apps to the Azure Identity SDK or use the migration sidecar approaches in the AKS migration guide.

## Verify
- [ ] `kubectl exec <pod> -- env | grep AZURE_` shows the injected variables.
- [ ] Decoding the payload of the token in `$AZURE_FEDERATED_TOKEN_FILE` shows `iss` = issuer and `sub` = FIC subject.
- [ ] App call to Key Vault/Storage succeeds; pods in another namespace with the same SA name fail.

## Checked
Date: 2026-10-24. Checked against MicrosoftDocs/azure-aks-docs (workload-identity-overview, workload-identity-deploy-cluster, workload-identity-migrate-from-pod-identity, use-azure-ad-pod-identity; main branch) and the Azure/azure-workload-identity repository docs (installation: mutating-admission-webhook, managed-clusters, self-managed-clusters/configurations; main branch).
- Confirmed: AKS flags and FIC command with `--audience api://AzureADTokenExchange`; SA annotation and pod label; token env var; 20-FIC limit; `skip-containers` pod annotation; helm repo URL, chart, namespace and `azureTenantID` value; API server issuer flags; EKS issuer lookup command; pod-managed identity deprecation.
- Removed as unconfirmed: EKS and GKE issuer URL formats, blob static website hosting advice, the NMI remark, and the claim that the AKS issuer URL never changes.
Method: documentation only; no commands were run.
