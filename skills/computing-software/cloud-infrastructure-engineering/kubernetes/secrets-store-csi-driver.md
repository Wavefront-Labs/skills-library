---
id: computing-software.cloud-infrastructure-engineering.kubernetes.secrets-store-csi-driver
name: secrets-store-csi-driver
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, secrets-store-csi, secrets-store-csi-driver, secretproviderclass, vault, aws-secrets-manager, azure-key-vault, csi]
level: practitioner
status: docs-checked
description: "Mount secrets from Vault, AWS, Azure or GCP into pods with the Secrets Store CSI Driver: SecretProviderClass, optional sync to Secrets, rotation, and mount failure triage."
sources: ["https://secrets-store-csi-driver.sigs.k8s.io/", "https://secrets-store-csi-driver.sigs.k8s.io/topics/sync-as-kubernetes-secret", "https://secrets-store-csi-driver.sigs.k8s.io/topics/secret-auto-rotation", "https://github.com/aws/secrets-store-csi-driver-provider-aws"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Secrets Store CSI Driver

## Model
A DaemonSet CSI driver (`secrets-store.csi.k8s.io`) plus a **provider** DaemonSet (AWS,
Azure, GCP, Vault) fetches secrets at pod mount time, using the identity mechanism of each
provider (AWS: IRSA by default, or EKS Pod Identity with `usePodIdentity: "true"`). Nothing is stored
in etcd unless you opt into sync.

## Install
```bash
helm repo add secrets-store-csi-driver https://kubernetes-sigs.github.io/secrets-store-csi-driver/charts
helm install csi-secrets-store secrets-store-csi-driver/secrets-store-csi-driver -n kube-system \
  --set syncSecret.enabled=true --set enableSecretRotation=true --set rotationPollInterval=2m
# then the provider, e.g. AWS:
helm repo add aws-secrets-manager https://aws.github.io/secrets-store-csi-driver-provider-aws
helm install secrets-provider-aws aws-secrets-manager/secrets-store-csi-driver-provider-aws -n kube-system
```

## SecretProviderClass + pod
```yaml
apiVersion: secrets-store.csi.x-k8s.io/v1
kind: SecretProviderClass
metadata: {name: db-creds, namespace: shop}
spec:
  provider: aws
  parameters:
    objects: |
      - objectName: "prod/shop/db"
        objectType: "secretsmanager"
        jmesPath:                  # aliases containing a hyphen need extra quoting in the AWS provider
          - {path: username, objectAlias: dbuser}
          - {path: password, objectAlias: dbpass}
  secretObjects:                       # optional: also create a k8s Secret
  - secretName: db-creds
    type: Opaque
    data:
    - {objectName: dbuser, key: username}
    - {objectName: dbpass, key: password}
---
# in the pod spec
volumes:
- name: secrets
  csi:
    driver: secrets-store.csi.k8s.io
    readOnly: true
    volumeAttributes: {secretProviderClass: db-creds}
# container: volumeMounts: [{name: secrets, mountPath: /mnt/secrets, readOnly: true}]
```

## Behaviour to design around
- The synced Secret exists **only while at least one pod mounts the volume**; env vars
  referencing it fail on a fresh cluster until a mounting pod runs.
- Rotation updates the mounted files and the synced Secret; **env vars never update**, so
  apps must re-read files (or use Reloader to restart on Secret change). Auto rotation is an alpha feature, off by default
  (`enableSecretRotation=true` in Helm); `rotationPollInterval` (default 2m) is the minimum time
  between rotations, and only providers with a gRPC server support it.
- Mount failure blocks pod start (ContainerCreating). Read `kubectl describe pod` events
  (`FailedMount ... rpc error`) and the provider pod logs on that node.
- The SecretProviderClass is namespaced and must be in the pod's namespace.

## Triage
```bash
kubectl describe pod <pod> | sed -n '/Events/,$p'
kubectl -n kube-system logs <csi-driver pod on the pod's node> -c secrets-store --since=10m
kubectl -n kube-system logs <provider pod on the pod's node> --since=10m          # auth/permission errors
kubectl get secretproviderclasspodstatuses -n shop                       # per-pod mount status
```
Common: IAM/role trust missing for the service account, wrong object name/region, provider
not installed on that node pool (tolerations), Windows nodes need the Windows driver manifest, and the AWS
provider does not support Fargate node groups.

## Choosing vs External Secrets Operator
CSI avoids etcd copies and gives per-pod identity; ESO is simpler for apps that want a
normal Secret and for GitOps diffs. Many platforms run ESO by default and CSI for high-value secrets.

## Checked

Checked 2026-10-27 against the Secrets Store CSI Driver docs source (kubernetes-sigs/secrets-store-csi-driver, `docs/book/src`) and the AWS provider README (aws/secrets-store-csi-driver-provider-aws).

- Helm repo and chart, `syncSecret.enabled=true`, `enableSecretRotation=true`, `rotationPollInterval`, `SecretProviderClass` `secrets-store.csi.x-k8s.io/v1` with `secretObjects`, synced Secret existing only while a pod mounts it, env vars needing a restart (Reloader), `SecretProviderClassPodStatus`, FailedMount troubleshooting, same-namespace requirement, container name `secrets-store`: confirmed.
- Rotation is documented as alpha, uses `--enable-secret-rotation` and `--rotation-poll-interval` (default 2m, a minimum cache duration), and needs providers with a gRPC server.
- AWS provider: Helm install commands, `objectType: secretsmanager`, `jmesPath` with `path` and `objectAlias`, IRSA default and `usePodIdentity`, Fargate unsupported confirmed; aliases with hyphens need the quoted form, so the example aliases were changed.
- Removed unconfirmed claims: tmpfs volume, DaemonSet names for logs, identity details for non-AWS providers.

Method: documentation only; no commands were run.
