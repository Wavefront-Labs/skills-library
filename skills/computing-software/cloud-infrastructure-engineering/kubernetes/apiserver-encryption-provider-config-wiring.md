---
id: computing-software.cloud-infrastructure-engineering.kubernetes.apiserver-encryption-provider-config-wiring
name: apiserver-encryption-provider-config-wiring
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, encryption-at-rest, encryption-provider-config, encryptionconfiguration, aescbc, kube-apiserver]
level: practitioner
status: docs-checked
description: "Wire an EncryptionConfiguration into kube-apiserver: generate a key, write the file, add the flag and hostPath mount, restart, and verify secrets are encrypted in etcd."
sources: ["https://kubernetes.io/docs/tasks/administer-cluster/encrypt-data/", "https://kubernetes.io/docs/tasks/administer-cluster/kms-provider/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Wiring encryption at rest into kube-apiserver

## 1. Key and config
```bash
head -c 32 /dev/urandom | base64          # 32-byte key
sudo mkdir -p /etc/kubernetes/enc
sudo tee /etc/kubernetes/enc/enc.yaml >/dev/null <<'EOF'
apiVersion: apiserver.config.k8s.io/v1
kind: EncryptionConfiguration
resources:
- resources: [secrets]
  providers:
  - aescbc:
      keys:
      - name: key1
        secret: <base64-key>
  - identity: {}
EOF
sudo chmod 600 /etc/kubernetes/enc/enc.yaml
```
The first provider encrypts new writes; later ones are used only to decrypt. `identity` last lets
existing plaintext Secrets still be read. Once every Secret is rewritten, remove `identity` so a
plaintext Secret can no longer be read, then restart each apiserver in turn.

## 2. kube-apiserver static pod
```yaml
spec:
  containers:
  - command:
    - kube-apiserver
    - --encryption-provider-config=/etc/kubernetes/enc/enc.yaml
    volumeMounts:
    - {name: enc, mountPath: /etc/kubernetes/enc, readOnly: true}
  volumes:
  - {name: enc, hostPath: {path: /etc/kubernetes/enc, type: DirectoryOrCreate}}
```
Edit on EVERY control-plane node with the identical file. The kubelet restarts the apiserver;
watch `crictl ps` and fix typos quickly (the API is down meanwhile).

## 3. Encrypt existing Secrets
```bash
kubectl get secrets -A -o json | kubectl replace -f -
```

## 4. Verify in etcd
```bash
sudo ETCDCTL_API=3 etcdctl --cacert=/etc/kubernetes/pki/etcd/ca.crt \
  --cert=/etc/kubernetes/pki/etcd/server.crt --key=/etc/kubernetes/pki/etcd/server.key \
  get /registry/secrets/default/my-secret | hexdump -C | head
```
Encrypted values start with `k8s:enc:aescbc:v1:key1:`; plaintext shows readable keys.

## Gotchas
- Back up `enc.yaml` with etcd backups: an etcd snapshot without the key is unrecoverable.
- Prefer a KMS provider (v2; KMS v1 is deprecated since 1.28) in production so keys stay outside the
  node; with local providers the keys sit in `enc.yaml` on the control-plane host.
- The docs rate `aescbc` as weak and not recommended (CBC padding-oracle concern), and `aesgcm` must
  be rotated every 200,000 writes; `secretbox` is listed as a newer option. Pick per your review
  requirements; this page's aescbc example mirrors the Kubernetes docs example.

## Checked
Checked 2026-10-23 against the kubernetes/website docs (current release 1.37).
Confirmed: `EncryptionConfiguration` `apiserver.config.k8s.io/v1`; provider ordering semantics; `head -c 32 /dev/urandom | base64`;
`kubectl get secrets --all-namespaces -o json | kubectl replace -f -`; etcd prefix `k8s:enc:aescbc:v1:<key name>:` and
the `/registry/secrets/<ns>/<name>` path; aesgcm 200,000-write rotation rule; provider strength table; KMS v1 deprecated since 1.28.
Wrong in the original: aescbc/secretbox described as "safer static choices" (docs call aescbc weak and not recommended).
The etcdctl certificate paths and the static-pod volume mount with `DirectoryOrCreate` match the docs example.
Method: documentation only; no commands were run.
