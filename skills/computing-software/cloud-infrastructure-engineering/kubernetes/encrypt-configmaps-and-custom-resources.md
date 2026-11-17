---
id: computing-software.cloud-infrastructure-engineering.kubernetes.encrypt-configmaps-and-custom-resources
name: encrypt-configmaps-and-custom-resources
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, secrets-encryption-at-rest, encrypt-configmaps, encryptionconfiguration, custom-resources, wildcards]
level: practitioner
status: docs-checked
description: "Extend encryption at rest beyond Secrets to ConfigMaps, custom resources and wildcard groups, and rewrite existing objects so they are actually encrypted."
sources: ["https://kubernetes.io/docs/tasks/administer-cluster/encrypt-data/", "https://kubernetes.io/docs/reference/config-api/apiserver-config.v1/", "https://kubernetes.io/docs/tasks/administer-cluster/kms-provider/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Encrypting ConfigMaps and other resources

```yaml
apiVersion: apiserver.config.k8s.io/v1
kind: EncryptionConfiguration
resources:
- resources: [secrets, configmaps]
  providers:
  - kms: {apiVersion: v2, name: vault, endpoint: unix:///var/run/kmsplugin/socket.sock}
  - identity: {}
- resources: ["*.vault.example.com"]       # every resource in one API group (CRDs)
  providers:
  - kms: {apiVersion: v2, name: vault, endpoint: unix:///var/run/kmsplugin/socket.sock}
  - identity: {}
```
Wildcards need Kubernetes v1.27 or newer: `*.<group>` for a group, `*.` for the core group,
`*.*` for everything (including custom resources added after the API server starts); encrypting a
custom resource at all needs v1.26. Wildcards that overlap within a list or across entries are
not allowed. To exempt a kind from a wildcard, add an earlier `resources` item naming it with the
`identity` provider (the docs example exempts `events`).

## Choose carefully
- Encrypt: ConfigMaps if teams put credentials in them; CRs that carry secrets (database
  credentials in operator CRs, cert-manager or external-secrets objects).
- Be deliberate with `*.*`: the Kubernetes docs example exempts Events from it with an earlier
  `identity` entry.

## Re-encrypt existing objects
Only new writes are encrypted. Rewrite existing ones (the docs show the Secret form; run as
an administrator and retry on conflicts):
```bash
kubectl get configmaps -A -o json | kubectl replace -f -
kubectl get <crd-plural>.vault.example.com -A -o json | kubectl replace -f -
```

## Verify
```bash
etcdctl get /registry/configmaps/default/app-config | hexdump -C | head -3
```
The value starts with `k8s:enc:` followed by the provider (for KMS v2, `k8s:enc:kms:v2:<name>`).

## Checked

Checked 2026-10-26 against Kubernetes documentation v1.37 (kubernetes/website commit 2026-10-25, feature gate pages, KMS and encryption task pages). Confirmed: wildcard forms `*.<group>`, `*.` and `*.*` and the v1.27 requirement; custom resource encryption needs v1.26; overlapping wildcards are disallowed and exemptions use an earlier `identity` entry; the `replace` sweep; the `k8s:enc:` prefix; the v2 provider fields. Removed as unconfirmed: the performance and outage claims about `*.*`, the first-match rule wording, and the etcd key layout for custom resources.

Method: documentation only; no commands were run.
