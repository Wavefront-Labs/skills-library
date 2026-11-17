---
id: computing-software.cloud-infrastructure-engineering.kubernetes.kubectl-create-secret-types
name: kubectl-create-secret-types
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, secrets, kubectl-create-secret, secret-types, docker-registry-secret, tls-secret, ckad, cka]
level: practitioner
status: docs-checked
description: "Create each Secret type with kubectl create secret generic/tls/docker-registry or stringData YAML, know the type-enforced keys, and avoid leaking values."
sources: ["https://kubernetes.io/docs/concepts/configuration/secret/#secret-types", "https://kubernetes.io/docs/reference/kubectl/generated/kubectl_create/kubectl_create_secret/", "https://kubernetes.io/docs/tasks/configmap-secret/managing-secret-using-kubectl/", "https://github.com/kubernetes/kubernetes/tree/master/staging/src/k8s.io/kubectl/pkg/cmd/create"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Creating Secrets: types and kubectl commands

## Types (validated keys)
| type | Required keys | Create with |
|---|---|---|
| `Opaque` | any | `kubectl create secret generic` |
| `kubernetes.io/tls` | `tls.crt`, `tls.key` | `kubectl create secret tls` |
| `kubernetes.io/dockerconfigjson` | `.dockerconfigjson` | `kubectl create secret docker-registry` |
| `kubernetes.io/basic-auth` | at least one of `username`, `password` | YAML |
| `kubernetes.io/ssh-auth` | `ssh-privatekey` | `kubectl create secret generic --type=kubernetes.io/ssh-auth` or YAML |
| `kubernetes.io/service-account-token` | populated by controller | YAML with the `kubernetes.io/service-account.name` annotation (legacy mechanism; prefer TokenRequest) |
| `bootstrap.kubernetes.io/token` | `token-id`, `token-secret` | kubeadm |

## Commands
```bash
# from literals (lands in shell history! prefer files or stdin)
kubectl create secret generic db -n app --from-literal=username=app --from-literal=password="$PW"
# from files: key = filename unless key= given
kubectl create secret generic db -n app --from-file=password=./pw.txt --from-file=./ca.crt
# from env file (KEY=VALUE lines)
kubectl create secret generic app-env -n app --from-env-file=.env
kubectl create secret tls web-tls -n app --cert=tls.crt --key=tls.key
kubectl create secret docker-registry regcred -n app --docker-server=ghcr.io \
  --docker-username=bot --docker-password="$TOKEN" --docker-email=ops@example.com
kubectl create secret generic ssh --type=kubernetes.io/ssh-auth --from-file=ssh-privatekey=id_ed25519
# generate YAML for review or GitOps
kubectl create secret generic db --from-literal=password=x --dry-run=client -o yaml
```
YAML with `stringData` avoids manual base64; it is merged into `data` on write.

## Read / rotate
```bash
kubectl get secret db -o jsonpath='{.data.password}' | base64 -d
kubectl create secret generic db --from-file=password=./new.txt --dry-run=client -o yaml | kubectl apply -f -   # update in place
```
Pods consuming via env vars need a restart; volume-mounted secrets are refreshed after the kubelet sync period plus cache propagation delay (never with `subPath`).

## Gotchas
- base64 is encoding, not encryption. Anyone with `get secrets` reads them; enable etcd
  encryption at rest and keep `list secrets` RBAC tight.
- `echo "pw" | base64` includes the newline — use `echo -n` or `printf`.
- `--from-file` on a directory adds every regular file as a key.
- Each Secret is limited to 1 MiB.
- `immutable: true` for secrets that never change: the kubelet does not need to watch them, which reduces kube-apiserver load.

## Verify
- [ ] `kubectl get secret x -o jsonpath='{.type}'` is the intended type; no plaintext secrets in git.

## Checked
Checked 2026-10-24 against the Kubernetes Secret documentation (website main, v1.37) and kubectl source (main): type list and required keys, the 1 MiB limit, `generic --type`, `--from-env-file`, `docker-registry --docker-*` flags, the kubelet sync-period plus cache delay and no updates for `subPath`, immutable Secrets and kubelet watches, `echo -n` newline advice. Removed the unconfirmed `~1 min` figure.
Method: documentation only; no commands were run.
