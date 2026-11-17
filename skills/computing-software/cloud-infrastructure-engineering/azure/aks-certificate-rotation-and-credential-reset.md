---
id: computing-software.cloud-infrastructure-engineering.azure.aks-certificate-rotation-and-credential-reset
name: aks-certificate-rotation-and-credential-reset
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, aks, aks-cert-rotation, aks-credential-reset, rotate-certs, cluster-admin-kubeconfig, service-principal]
level: advanced
status: docs-checked
description: "Rotate AKS cluster certificates with az aks rotate-certs, invalidate leaked admin kubeconfigs, check expiry, and reset or replace service principal credentials."
sources: ["https://learn.microsoft.com/azure/aks/certificate-rotation", "https://learn.microsoft.com/azure/aks/rotate-certificates", "https://learn.microsoft.com/azure/aks/update-credentials", "https://learn.microsoft.com/azure/aks/local-accounts", "https://learn.microsoft.com/azure/aks/system-assigned-managed-identity"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# AKS certificate rotation and credential reset

**Goal:** respond to a leaked admin kubeconfig or expiring certificates, and keep cluster identities current.

## When to rotate certificates
- A `--admin` (clusterAdmin) kubeconfig leaked: its client certificate is valid until rotation.
- Clusters created before May 2019 have cluster CA certificates that expire after two years; clusters created after May 2019 have 30-year CA certificates. The cluster CA is rotated manually; kubelet client (and, where enabled, serving) certificates auto-rotate on clusters with Kubernetes RBAC.
Check expiry:
```bash
az aks get-credentials -g rg -n aks01
kubectl config view --raw -o jsonpath="{.clusters[?(@.name == 'aks01')].cluster.certificate-authority-data}" | base64 -d | openssl x509 -text | grep -A2 Validity
```

## Rotate
```bash
az aks rotate-certs -g rg -n aks01
```
- Rotates the cluster CA, certificates and service account tokens; it recreates all nodes, scale sets and disks and can cause **up to 30 minutes of downtime** - schedule a window. If the command fails, `az aks show` reports a Certificate Rotating state; rerun it.
- Existing kubectl certificates stop working (x509 "signed by unknown authority"); everyone re-runs `az aks get-credentials`.
- Things holding cluster certs (CI/CD agents, GitOps outside the cluster, monitoring) need new credentials.

## Prevent the problem
Disable local accounts so no certificate-based admin kubeconfig exists; everyone uses Entra ID:
```bash
az aks update -g rg -n aks01 --disable-local-accounts      # on an Entra-integrated cluster; at create time use --enable-aad --disable-local-accounts
```
Then `--admin` credentials are unavailable. Disabling local accounts on an existing cluster does not revoke certificates people already hold; rotate the cluster certificates afterwards.

## Service principal clusters
```bash
az aks update-credentials -g rg -n aks01 --reset-service-principal \
  --service-principal <appId> --client-secret '<new-secret>'
```
A service principal created for a cluster has a one-year expiry. Better: migrate to managed identity (nothing to rotate; you cannot switch back to a service principal afterwards):
```bash
az aks update -g rg -n aks01 --enable-managed-identity
```
The update reimages all nodes (cordon, drain, reimage), which causes downtime, and it only works when a newer node image (VHD) is available to consume. Re-run `az aks update --attach-acr` afterwards if the cluster pulls from ACR, and re-grant any other rights the service principal held.

## Gotchas
- Anything holding cluster certificates (CI/CD agents, external GitOps, monitoring) needs new credentials after rotation.

## Verify
- [ ] Old kubeconfig rejected (x509 error) after rotation and `kubectl get nodes` works with fresh credentials; no service principal secrets remain (managed identity).

## Checked
Date: 2026-10-24. Checked against MicrosoftDocs/azure-aks-docs (certificate-rotation, rotate-certificates, update-credentials, local-accounts, system-assigned-managed-identity; main branch).
- Confirmed: CA lifetimes (two years before May 2019, 30 years after); CA rotation is manual with `az aks rotate-certs`, which recreates nodes and can cause up to 30 minutes of downtime; kubectl certificates must be refreshed afterwards; `--reset-service-principal` with `--service-principal`/`--client-secret`; one-year service principal expiry; `--disable-local-accounts` and the need to rotate certificates afterwards; `--enable-managed-identity` reimages nodes and cannot be reverted.
- Removed as unconfirmed: the `/tmp` admin kubeconfig example, the break-glass group advice, the node-image-only upgrade step, and the expired-secret symptom list.
Method: documentation only; no commands were run.
