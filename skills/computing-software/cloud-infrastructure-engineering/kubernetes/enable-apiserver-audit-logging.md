---
id: computing-software.cloud-infrastructure-engineering.kubernetes.enable-apiserver-audit-logging
name: enable-apiserver-audit-logging
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, audit-logging, audit-policy-file, audit-log-path, kube-apiserver, static-pod]
level: practitioner
status: docs-checked
description: "Enable API audit logging on a kubeadm cluster: write the policy, add audit flags and hostPath mounts to the kube-apiserver manifest, and confirm events are written."
sources: ["https://kubernetes.io/docs/tasks/debug/debug-cluster/audit/", "https://kubernetes.io/docs/reference/config-api/apiserver-audit.v1/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Enabling audit logging (kubeadm)

## 1. Policy
`/etc/kubernetes/audit/policy.yaml`:
```yaml
apiVersion: audit.k8s.io/v1
kind: Policy
omitStages: [RequestReceived]
rules:
- level: None
  users: ["system:kube-proxy"]
  verbs: ["watch"]
- level: None
  resources: [{group: "", resources: ["events"]}]
- level: Metadata
  resources: [{group: "", resources: ["secrets", "configmaps"]}]
- level: RequestResponse
  verbs: ["create", "update", "patch", "delete"]
  resources: [{group: "rbac.authorization.k8s.io"}]
- level: Metadata
```
Order matters: the first matching rule sets the level. Secrets never above Metadata (bodies would be
logged). Without `--audit-policy-file` no events are logged, and the policy must contain at least one rule.
The `--audit-log-maxage` flag is in days, `--audit-log-maxbackup` is the number of rotated files kept,
and `--audit-log-maxsize` is megabytes per file before rotation.

## 2. kube-apiserver manifest
```yaml
- --audit-policy-file=/etc/kubernetes/audit/policy.yaml
- --audit-log-path=/var/log/kubernetes/audit/audit.log
- --audit-log-maxage=30
- --audit-log-maxbackup=10
- --audit-log-maxsize=100
volumeMounts:
- {name: audit-policy, mountPath: /etc/kubernetes/audit, readOnly: true}
- {name: audit-logs, mountPath: /var/log/kubernetes/audit}
volumes:
- {name: audit-policy, hostPath: {path: /etc/kubernetes/audit, type: DirectoryOrCreate}}
- {name: audit-logs, hostPath: {path: /var/log/kubernetes/audit, type: DirectoryOrCreate}}
```
Apply on each control-plane node. A wrong path or missing mount crashes the apiserver; check
`crictl ps -a | grep apiserver` and its logs.

kubeadm config equivalent: `apiServer.extraArgs` (a list of `name`/`value` entries in the
`kubeadm.k8s.io/v1beta4` ClusterConfiguration API) and `apiServer.extraVolumes`, so upgrades keep
the settings.

## 3. Verify
```bash
sudo tail -n 3 /var/log/kubernetes/audit/audit.log | jq '{verb, user: .user.username, uri: .requestURI, level, stage}'
kubectl create secret generic audit-test --from-literal=a=b
sudo grep audit-test /var/log/kubernetes/audit/audit.log | jq -c '{verb, level}'
```
Ship the file with a node agent (Fluent Bit tail input) to your SIEM.

## Checked
Checked 2026-10-23 against the kubernetes/website docs (current release 1.37) and kubernetes/kubernetes source.
Confirmed: policy `audit.k8s.io/v1` structure, `omitStages`, rule matching order, levels, example rules (users/verbs/resources
fields, group-only resources), `--audit-policy-file` and `--audit-log-*` flags and units, kubeadm v1beta4 `extraArgs` (list of Arg)
and `extraVolumes`. The `crictl`, `jq` and `hostPath` details are generic examples and were not checked beyond the docs examples.
Method: documentation only; no commands were run.
