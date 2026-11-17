---
id: computing-software.devops-ci-cd.flux.object-identity-multitenant
name: object-identity-multitenant
category: computing-software
field: devops-ci-cd
product: flux
tags: [object-identity, serviceaccounts-token, spiffe, tenant-isolation, credential-provider]
level: advanced
status: docs-checked
description: "Take cloud or cluster credentials from the Flux object ServiceAccount instead of the controller pod, for strict tenant isolation."
sources:
  - https://fluxcd.io/flux/installation/configuration/object-identity/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
With object identity the identity comes from the Flux object (through its `serviceAccountName`), not from the controller pod. In multi-tenant clusters, platform admins must stop tenants using controller workload identity, because that would give them the identity the controller uses for external resources; forcing object identity achieves this.

Controllers must be configured per credential provider.

Kubernetes provider: the controller needs permission to request ServiceAccount tokens (TokenRequest API), the `create` verb on `serviceaccounts/token`, granted with a ClusterRole and ClusterRoleBinding:

```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  name: flux-object-identity
rules:
  - apiGroups: [""]
    resources: ["serviceaccounts/token"]
    verbs: ["create"]
```

Bind it to the ServiceAccounts of source-controller, kustomize-controller, helm-controller, notification-controller, image-reflector-controller and image-automation-controller in `flux-system`.

The `spiffe` credential provider needs the controller configured with the SPIFFE Workload API, the flag `--spiffe-broker-endpoint`, and at least one repeatable `--spiffe-broker-id` flag.

Lockdown: set a default ServiceAccount, looked up in the namespace of the Flux object, so tenants must name a ServiceAccount explicitly. Flags (the page uses the `default` account, which should have no identity configured):
- `--default-service-account` on source-controller, notification-controller, image-reflector-controller and image-automation-controller (default for `.spec.serviceAccountName`).
- `--default-kubeconfig-service-account` on kustomize-controller and helm-controller (remote cluster kubeconfig ConfigMap `.data.serviceAccountName`).
- `--default-decryption-service-account` on kustomize-controller (SOPS, `Kustomization.spec.decryption.serviceAccountName`).

## Checked

2026-11-08. Read in full: https://fluxcd.io/flux/installation/configuration/object-identity/ (raw source in the fluxcd/website repository).

Removed or corrected: the single-tenant/multi-tenant framing and the verification step, which are not on the page; added the documented default-service-account flags.

Method: documentation only; no commands were run.
