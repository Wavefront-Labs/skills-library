---
id: computing-software.cryptography-implementation.key-management.injecting-secrets-into-workloads
name: injecting-secrets-into-workloads
category: computing-software
field: cryptography-implementation
product: key-management
tags: [key-management, cryptography-implementation, external-secrets, secrets-store-csi-driver, vault-agent-injector, kubernetes, secret-injection, secret-sprawl, workload-identity]
level: practitioner
status: draft
description: "Deliver secrets to pods and services with Secrets Store CSI driver, Vault Agent injector or External Secrets Operator, and choose file mounts over env vars."
sources: ["https://secrets-store-csi-driver.sigs.k8s.io/", "https://developer.hashicorp.com/vault/docs/platform/k8s/injector", "https://external-secrets.io/latest/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Injecting secrets into workloads

## Options
| Tool | Mechanism | Creates a K8s Secret? |
|---|---|---|
| Secrets Store CSI driver + provider (AWS, Azure, GCP, Vault) | Mounts secrets as files in a tmpfs volume at pod start | Optional (`secretObjects` sync) |
| Vault Agent injector | Sidecar logs in with the pod SA, renders templates to a shared memory volume, renews leases | No |
| External Secrets Operator | Controller copies from the external store into native K8s Secrets on a refresh interval | Yes |

## Examples
Vault Agent annotations:
```yaml
annotations:
  vault.hashicorp.com/agent-inject: "true"
  vault.hashicorp.com/role: "orders"
  vault.hashicorp.com/agent-inject-secret-db: "secret/data/orders/db"
  vault.hashicorp.com/agent-inject-template-db: |
    {{- with secret "secret/data/orders/db" -}}postgres://{{ .Data.data.user }}:{{ .Data.data.pass }}@db/orders{{- end }}
```
External Secrets:
```yaml
apiVersion: external-secrets.io/v1
kind: ExternalSecret
metadata: {name: orders-db}
spec:
  refreshInterval: 1h
  secretStoreRef: {name: aws-sm, kind: ClusterSecretStore}
  target: {name: orders-db}
  data:
    - secretKey: password
      remoteRef: {key: prod/orders/db, property: password}
```

## Choosing
- Want secrets never stored in etcd: CSI driver without sync, or Vault Agent.
- Apps that only read env vars or native Secrets, GitOps-friendly: External Secrets (and encrypt etcd).
- Dynamic database credentials with leases: Vault Agent (handles renewal).

## Files over environment variables
Env vars leak via `/proc/<pid>/environ`, crash reports, child processes and debug endpoints. Mount files with
`0400` permissions, and have apps re-read on change for rotation (CSI rotation and Agent re-render update files;
env vars require a restart).

## Verify
- [ ] Rotating the external secret updates the mounted file within the refresh interval.
- [ ] Pod spec and logs contain no secret values.
- [ ] RBAC prevents other namespaces from reading the synced Secret.
