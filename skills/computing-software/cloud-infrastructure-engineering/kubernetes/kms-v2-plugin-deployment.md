---
id: computing-software.cloud-infrastructure-engineering.kubernetes.kms-v2-plugin-deployment
name: kms-v2-plugin-deployment
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, secrets-encryption-at-rest, kms-plugin, kms-v2, vault, envelope-encryption]
level: practitioner
status: docs-checked
description: "Deploy a KMS v2 plugin (cloud KMS or Vault) as a static pod on each control-plane node, wire the socket into kube-apiserver and monitor its health."
sources: ["https://kubernetes.io/docs/tasks/administer-cluster/kms-provider/", "https://github.com/kubernetes-sigs/aws-encryption-provider", "https://github.com/Azure/kubernetes-kms", "https://kubernetes.io/docs/tasks/administer-cluster/encrypt-data/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Deploying a KMS v2 plugin

KMS v2 (stable since 1.29) uses envelope encryption: the apiserver encrypts data with a
single-use DEK derived from a seed, and the plugin, a gRPC server on a UNIX socket on the
control-plane host, protects that seed with a key held in the external KMS. Example open-source
plugins that implement it: aws-encryption-provider (AWS KMS, kubernetes-sigs) and
kubernetes-kms (Azure Key Vault); the flags below are those of aws-encryption-provider.

## Plugin as a static pod
```yaml
# /etc/kubernetes/manifests/kms-plugin.yaml (every control-plane node)
apiVersion: v1
kind: Pod
metadata: {name: kms-plugin, namespace: kube-system}
spec:
  containers:
  - name: plugin
    image: <plugin-image>:<tag>
    command: ["/aws-encryption-provider"]
    args: ["--listen=/var/run/kmsplugin/socket.sock", "--key=<key-arn>", "--region=<region>"]
    volumeMounts: [{name: sock, mountPath: /var/run/kmsplugin}]
  volumes: [{name: sock, hostPath: {path: /var/run/kmsplugin, type: DirectoryOrCreate}}]
```
Give the plugin access to the key through the platform's own identity (see the plugin's README
for the permissions it needs) rather than static keys in the manifest.

## Wire into the apiserver
```yaml
# /etc/kubernetes/enc/enc.yaml
resources:
- resources: [secrets]
  providers:
  - kms: {apiVersion: v2, name: cloudkms, endpoint: unix:///var/run/kmsplugin/socket.sock, timeout: 3s}
  - identity: {}
```
Add `--encryption-provider-config=/etc/kubernetes/enc/enc.yaml` and hostPath mounts for the
config and socket directory to kube-apiserver.

## Failure modes
- The API server polls the plugin's `Status` about every minute (every 10 seconds when it is not
  healthy) and `/healthz/kms-providers` reports plugin health; alert on it.
- DEKs that the API server has already unwrapped stay cached and keep decrypting without calling
  the KMS; a DEK that is not cached needs a working plugin and key. Keep a plugin on every
  control-plane node.

## Verify
```bash
kubectl get --raw=/healthz/kms-providers
kubectl create secret generic t --from-literal=a=b && etcdctl <cert flags> get /registry/secrets/default/t | head -c 40
```
Stored data prefixed `k8s:enc:kms:v2:cloudkms:` (the provider `name` after `v2:`) confirms it.

## Checked

Checked 2026-10-26 against Kubernetes documentation v1.37 (kubernetes/website commit 2026-10-25, feature gate pages, KMS and encryption task pages), the aws-encryption-provider README and source tree (`pkg/plugin/plugin_v2.go` present; static pod on the same node as each API server is its documented simple deployment; flags `--key`, `--region`, `--listen`, `--health-port`) and the Azure kubernetes-kms README (prefix `k8s:enc:kms:v2:azurekmsprovider`). Confirmed: KMS v2 stable since 1.29; plugin as a gRPC server on a UNIX socket on the control-plane hosts; `Status` polling every minute or 10 seconds when unhealthy; `/healthz/kms-providers`; cached DEKs decrypt without a KMS call; provider fields `apiVersion: v2`, `name`, `endpoint`, `timeout`; the encryption config file and `--encryption-provider-config` mounts. Removed as unconfirmed: the Vault and GCP plugin remarks, the managed-cluster checkbox claim, `hostNetwork` and priority class on the plugin pod, and the readiness-failure and disabled-key behaviours.

Method: documentation only; no commands were run.
