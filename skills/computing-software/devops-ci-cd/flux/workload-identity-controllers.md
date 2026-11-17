---
id: computing-software.devops-ci-cd.flux.workload-identity-controllers
name: workload-identity-controllers
category: computing-software
field: devops-ci-cd
product: flux
tags: [workload-identity, irsa, aks, gke, provider]
level: advanced
status: docs-checked
description: "Give Flux controllers cloud access through EKS IRSA, AKS or GKE workload identity by annotating controller ServiceAccounts at bootstrap."
sources:
  - https://fluxcd.io/flux/installation/configuration/workload-identity/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Controller-level workload identity lets Flux reach container registries, KMS, S3 and similar without static secrets on EKS, AKS and GKE. It suits single-tenant setups; for strict tenant isolation use object identity instead.

Annotate the controller ServiceAccounts with bootstrap patches. EKS (IRSA), for registry access and SOPS KMS respectively:

```yaml
patches:
  - patch: |
      apiVersion: v1
      kind: ServiceAccount
      metadata:
        name: controller
        annotations:
          eks.amazonaws.com/role-arn: <ECR ROLE ARN>
    target:
      kind: ServiceAccount
      name: "(source-controller|image-reflector-controller)"
```

with the same pattern using `<KMS ROLE ARN>` for kustomize-controller. AKS uses annotations `azure.workload.identity/client-id` and `azure.workload.identity/tenant-id` plus the pod label `azure.workload.identity/use: "true"`. GKE uses the annotation `iam.gke.io/gcp-service-account`.

In the Flux objects, use the controller identity and leave service accounts unset:
- For every kind except Kustomization and HelmRelease, set `.spec.provider` to `aws`, `azure` or `gcp` and leave `.spec.serviceAccountName` unset.
- For remote cluster access, set `.data.provider` in the ConfigMap that `.spec.kubeConfig.configMapRef` points to, with no `.data.serviceAccountName`.
- For SOPS decryption, leave `.spec.decryption.serviceAccountName` unset. There is no provider field; the provider comes from the SOPS metadata in the encrypted file.

## Checked

2026-11-08. Read in full: https://fluxcd.io/flux/installation/configuration/workload-identity/ (raw source in the fluxcd/website repository).

Removed or corrected: the closing test step, which is not on the page.

Method: documentation only; no commands were run.
