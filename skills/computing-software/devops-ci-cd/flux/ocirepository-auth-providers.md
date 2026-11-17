---
id: computing-software.devops-ci-cd.flux.ocirepository-auth-providers
name: ocirepository-auth-providers
category: computing-software
field: devops-ci-cd
product: flux
tags: [ocirepository, authentication, imagepullsecret, provider, ecr]
level: sme
status: docs-checked
description: "Authenticate OCIRepository to registries with secretRef, serviceAccountName or the generic, aws, azure and gcp providers."
sources:
  - https://fluxcd.io/flux/components/source/ocirepositories/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Public repositories need neither `.spec.secretRef` nor `.spec.serviceAccountName`.

`.spec.secretRef.name` is an optional reference to a Secret in the same namespace as the OCIRepository, holding credentials for the OCI repository:

```yaml
spec:
  provider: generic
  secretRef:
    name: ghcr-auth
```

`.spec.provider` is optional and its values are `generic` (the default), `aws`, `azure` and `gcp`. The `generic` provider covers public repositories, static credentials via `secretRef` or `serviceAccountName`, or a Kubernetes ServiceAccount token used for object identity.

`.spec.serviceAccountName` names a ServiceAccount in the same namespace. With `generic`, the controller uses the image pull secrets attached to it for static authentication, or its token for object identity if it opts in via credential annotations. With `aws`, `azure` or `gcp`, the ServiceAccount is used to acquire an object identity.

AWS: the `aws` provider authenticates with the EKS worker node IAM role or IAM Role for Service Accounts (IRSA), and so reaches ECR. If the worker node IAM role has ECR access, source-controller on that node does too. For IRSA, patch the bootstrap `flux-system/kustomization.yaml` to annotate the source-controller ServiceAccount:

```yaml
patches:
  - patch: |
      apiVersion: v1
      kind: ServiceAccount
      metadata:
        name: source-controller
        annotations:
          eks.amazonaws.com/role-arn: <role arn>
    target:
      kind: ServiceAccount
      name: source-controller
```

The AWS managed policy `arn:aws:iam::aws:policy/AmazonEC2ContainerRegistryReadOnly` can be attached to the IAM role when using IRSA.

Azure: the `azure` provider uses Workload Identity and Kubelet Managed Identity to reach ACR. GCP: when GKE nodes have the right OAuth scope for GCR and Artifact Registry, source-controller on them has access too.

Trigger a reconcile with `flux reconcile source oci <repository-name>`.

## Checked

2026-11-08. Read the Flux OCIRepository page sections on `.spec.url`, provider (generic, AWS, start of Azure, GKE node note), `.spec.secretRef`, `.spec.serviceAccountName` and triggering a reconcile. The rest of the page (verification, layer selectors, status) was not read in full. Removed the registry list, the `docker login` and `~/.docker/config.json` CLI advice and the `flux create secret oci` command, none of which appear on this page.

Method: documentation only; no commands were run.
