---
id: computing-software.cloud-infrastructure-engineering.azure.aks-security-workload-identity-and-defender
name: aks-security-workload-identity-and-defender
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, aks, aks-security, workload-identity, federated-credentials, aks-rbac, azure-rbac-for-kubernetes, entra-integration, kubelogin, private-cluster, authorized-ip-ranges, defender-for-containers, azure-policy-for-kubernetes, gatekeeper, pod-security-admission, secrets-store-csi, key-vault-provider, image-cleaner, network-policy, api-server-vnet-integration, disable-local-accounts]
level: advanced
status: docs-checked
description: "Harden AKS: Entra + Azure RBAC with local accounts off, workload identity instead of secrets, private API server or authorized IPs, Defender for Containers, Policy baselines, Secrets Store CSI."
sources: ["https://learn.microsoft.com/azure/aks/entra-id-authorization", "https://learn.microsoft.com/azure/aks/workload-identity-overview", "https://learn.microsoft.com/azure/aks/workload-identity-deploy-cluster", "https://learn.microsoft.com/azure/aks/use-azure-ad-pod-identity", "https://learn.microsoft.com/azure/aks/csi-secrets-store-driver", "https://learn.microsoft.com/azure/aks/api-server-vnet-integration", "https://learn.microsoft.com/azure/aks/private-clusters", "https://learn.microsoft.com/azure/aks/use-azure-policy", "https://learn.microsoft.com/azure/aks/use-kms-etcd-encryption", "https://learn.microsoft.com/azure/aks/image-cleaner", "https://learn.microsoft.com/azure/aks/manage-ssh-node-access", "https://learn.microsoft.com/azure/defender-for-cloud/defender-for-containers-introduction"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# AKS security — identity for humans and pods, a closed API server, and policy

**Goal:** `kubectl` only via Entra with Azure RBAC, pods reach Azure services with
federated tokens instead of secrets, the API server isn't on the internet, and admission
policy blocks the obvious.

## 1. Human access
```bash
az aks update -g rg -n aks-prod --enable-azure-rbac --disable-local-accounts     # on an Entra-integrated cluster
az role assignment create --role "Azure Kubernetes Service RBAC Cluster Admin" --assignee <platform-group> --scope <cluster-id>
az role assignment create --role "Azure Kubernetes Service RBAC Writer" --assignee <team-group> --scope "<cluster-id>/namespaces/team-a"
az aks get-credentials -g rg -n aks-prod   # then kubelogin convert-kubeconfig -l azurecli
```
- Roles: *RBAC Reader / Writer / Admin / Cluster Admin*; Reader and Writer (and Admin, intended for namespaces) can be scoped to a **namespace** with the scope `<cluster-id>/namespaces/<name>`. *Azure Kubernetes Service Cluster User Role* lets you download the kubeconfig. Keep *Cluster Admin* in a PIM-eligible group.
- `--disable-local-accounts` removes the static admin credential; `az aks get-credentials --admin` stops working - that's the goal. On a cluster that already had local accounts, rotate the cluster certificates afterwards so previously issued admin certificates stop working.
- Custom roles reference data actions under `Microsoft.ContainerService/managedClusters/`; custom resources need the `customresources` data action and are not filtered by CRD group.

## 2. Workload identity (pods → Azure)
```bash
az aks update -g rg -n aks-prod --enable-oidc-issuer --enable-workload-identity
ISSUER=$(az aks show -g rg -n aks-prod --query oidcIssuerProfile.issuerUrl -o tsv)
az identity create -n id-orders -g rg
az identity federated-credential create -n aks-orders --identity-name id-orders -g rg \
  --issuer $ISSUER --subject system:serviceaccount:orders:orders-sa --audience api://AzureADTokenExchange
kubectl -n orders annotate sa orders-sa azure.workload.identity/client-id=<clientId>
# pod: metadata.labels: azure.workload.identity/use: "true"; serviceAccountName: orders-sa
```
The azure-workload-identity webhook mutates only pods that carry the `azure.workload.identity/use: "true"` label; it injects the projected token volume and sets `AZURE_FEDERATED_TOKEN_FILE`, which `DefaultAzureCredential` and `WorkloadIdentityCredential` read (do not hard-code the path). Grant the managed identity the data-plane roles it needs. A managed identity can have at most 20 federated identity credentials; changing service account annotations needs a pod restart.
Open-source pod-managed identity (AAD Pod Identity) was deprecated on 24 October 2022 and the project archived in September 2023 - migrate to workload identity.
Secrets Store CSI with Key Vault: `--enable-addons azure-keyvault-secrets-provider`; the add-on supports autorotation of mounted content and synced Kubernetes secrets (`enableSecretRotation`, default false, with `rotationPollInterval`, default 2m). Use a `SecretProviderClass` with the workload identity's client ID; mount as files, and sync to Kubernetes Secrets only when an app insists on environment variables.

## 3. Control plane exposure
- **Private cluster** (`--enable-private-cluster`): API via private endpoint + `privatelink.<region>.azmk8s.io`
  zone; CI reaches it from a self-hosted agent in the VNet or `az aks command invoke`.
- **API server VNet integration** (`--enable-apiserver-vnet-integration`): API server
  projected into a delegated subnet — simpler DNS, can still be public or private.
- Public clusters: at least `--api-server-authorized-ip-ranges 203.0.113.0/24,<nat-ip>/32`
  (include the cluster's own egress IP or nodes can't reach the API).
- Nodes: no public IPs (leave `--enable-node-public-ip` off), SSH disabled with `--ssh-access disabled` (preview), FIPS node images (`--enable-fips-image`) when required.

## 4. Defender for Containers
Enable the Containers plan in Microsoft Defender for Cloud, then deploy the sensor with `az aks update --enable-defender`. Coverage: agentless discovery and vulnerability assessment of registry images, running containers and supported nodes (daily re-scans), the Defender sensor for run-time threat detection (including antimalware, DNS and binary drift capabilities), Kubernetes audit-log based detections collected through the Azure-managed control plane integration, and control-plane posture recommendations. The same plan covers EKS and GKE through connectors and Arc-enabled Kubernetes. Alerts surface in Defender for Cloud and Microsoft Defender XDR. Alerts only fire for activity after the plan is enabled.

## 5. Admission policy
- **Azure Policy for Kubernetes** (`--enable-addons azure-policy`, Gatekeeper): assign the
  built-in initiative *Kubernetes cluster pod security baseline standards for Linux-based workloads* (audit first, then deny), and add policies for allowed images and privileged containers as needed. Use each policy's namespace exclusions for system namespaces.
- Or native **Pod Security Admission** labels per namespace
  (`pod-security.kubernetes.io/enforce: restricted`) — fine when you don't need Azure-wide compliance reporting.
- Image hygiene: `--enable-image-cleaner --image-cleaner-interval-hours 24` removes unused images from nodes (the minimum interval is 24 hours; the CLI default is one week).
- Network policy (Cilium/Azure/Calico): default-deny ingress per namespace, allow from
  ingress controller and same namespace; egress deny + allow DNS/known endpoints for crown-jewel namespaces.

## 6. Supply chain and secrets at rest
- **KMS etcd encryption** with Key Vault (`--enable-azure-keyvault-kms --azure-keyvault-kms-key-id <key> --azure-keyvault-kms-key-vault-network-access Public|Private`) for customer-managed-key control of secrets at rest.
- Sign images with Notation and verify with Ratify and Azure Policy (see the ACR documentation).
- Pull through ACR only (private endpoint, `--attach-acr`) rather than Docker Hub directly from production.

## Gotchas
- Workload identity tokens are per-service-account subject string: a typo in `system:serviceaccount:<ns>:<sa>` fails with `AADSTS70021` — compare with the federated credential exactly.
- Rehearse deny-effect policies in audit mode first and read the compliance report.
- `--disable-local-accounts` plus broken Entra integration can lock you out; `az aks update --enable-local-accounts` re-enables local accounts.

## Verify
- [ ] `kubectl auth can-i create pods -n team-a --as <user>` reflects Azure RBAC; `az aks get-credentials --admin` returns an error.
- [ ] A test pod with the SA label gets `AZURE_FEDERATED_TOKEN_FILE` and `az login --federated-token` / SDK call succeeds; same pod without the label fails.
- [ ] Defender for Cloud shows the sensor deployed on the cluster and lists image vulnerabilities for a known-old test image.
- [ ] A privileged test pod is rejected by Gatekeeper in a namespace where the baseline initiative is set to deny.

## Checked
Date: 2026-10-24. Checked against MicrosoftDocs/azure-aks-docs (entra-id-authorization, local-accounts, workload-identity-overview, workload-identity-deploy-cluster, use-azure-ad-pod-identity, csi-secrets-store-driver, api-server-vnet-integration, private-clusters, api-server-authorized-ip-ranges, use-azure-policy, use-kms-etcd-encryption, image-cleaner, manage-ssh-node-access, enable-fips-nodes, use-node-public-ips; main branch) and the Defender for Containers introduction and deployment overview pages on Microsoft Learn (updated 2026-08 and 2026-06; the Defender docs source repository is not public).
- Confirmed: Azure RBAC role names and namespace scoping; `--enable-azure-rbac`, `--disable-local-accounts` and certificate rotation afterwards; workload identity flags, label, `AZURE_FEDERATED_TOKEN_FILE`, 20-credential limit, `--audience api://AzureADTokenExchange`; pod-managed identity deprecation and archive dates; Secrets Store CSI rotation defaults; API server VNet integration and private DNS zone format; KMS, image cleaner, `--ssh-access disabled` (preview), FIPS and node public IP flags; pod security baseline initiative name; Defender coverage statements and `az aks update --enable-defender`.
- Removed as unconfirmed: `kube-audit-admin` category advice, `az security pricing` command, DaemonSet and taint-toleration remarks, the restricted initiative name, ACR image integrity policy, namespace-assignment and Gatekeeper rollout behaviours.
Method: documentation only; no commands were run.
