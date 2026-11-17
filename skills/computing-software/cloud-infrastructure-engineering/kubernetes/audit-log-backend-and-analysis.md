---
id: computing-software.cloud-infrastructure-engineering.kubernetes.audit-log-backend-and-analysis
name: audit-log-backend-and-analysis
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, audit-logging, audit-log-path, audit-log-maxage, audit-log-analysis, webhook-backend, cks, audit-batch]
level: practitioner
status: docs-checked
description: "Configure the kube-apiserver audit log backend (path, rotation, batching, webhook) on kubeadm static pods and map forensic questions to audit event fields."
sources: ["https://kubernetes.io/docs/tasks/debug/debug-cluster/audit/#log-backend", "https://kubernetes.io/docs/tasks/debug/debug-cluster/audit/#webhook-backend", "https://kubernetes.io/docs/reference/config-api/apiserver-audit.v1/", "https://kubernetes.io/docs/reference/command-line-tools-reference/kube-apiserver/"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Audit log backend and analysis

## Log backend flags (kube-apiserver)
```yaml
- --audit-policy-file=/etc/kubernetes/audit/policy.yaml
- --audit-log-path=/var/log/kubernetes/audit/audit.log   # "-" = stdout
- --audit-log-maxage=7          # days to keep rotated files
- --audit-log-maxbackup=10      # number of rotated files
- --audit-log-maxsize=100       # MB before rotation
- --audit-log-format=json
# --audit-log-mode: batch | blocking | blocking-strict (the Kubernetes docs do not recommend batch for the log backend)
```
Static pod: **both** the policy file and the log directory need hostPath volumes + mounts:
```yaml
volumeMounts:
- {name: audit-policy, mountPath: /etc/kubernetes/audit/policy.yaml, readOnly: true}
- {name: audit-log, mountPath: /var/log/kubernetes/audit/}
volumes:
- {name: audit-policy, hostPath: {path: /etc/kubernetes/audit/policy.yaml, type: File}}
- {name: audit-log, hostPath: {path: /var/log/kubernetes/audit/, type: DirectoryOrCreate}}
```
Without these mounts the apiserver cannot read the policy and audit records are not persisted.
Ship the log to external storage; files on control-plane nodes are subject to the
`maxage`/`maxbackup`/`maxsize` rotation limits.

**Webhook backend**: `--audit-webhook-config-file` (kubeconfig format) +
`--audit-webhook-mode` (batch is the default for the webhook backend); in batch mode, if incoming
events overflow the buffer (`--audit-webhook-batch-buffer-size`, default 10000) they are dropped.
Metrics: `apiserver_audit_event_total` (events exported) and `apiserver_audit_error_total`
(events dropped due to an error during export).

## Analysis: which audit event fields answer which question
Audit events are JSON objects (`audit.k8s.io/v1` Event) when `--audit-log-format=json`. The fields:
| Question | Fields to filter on |
|---|---|
| Who deleted or changed X? | `verb`, `objectRef.resource`, `objectRef.namespace`, `objectRef.name`, `user.username`, `requestReceivedTimestamp` |
| Who read Secrets? | `objectRef.resource == "secrets"` with `verb` `get`/`list`/`watch`, plus `user.username` |
| Exec or attach into pods | `objectRef.subresource` (`exec`, `attach`, `portforward`) |
| Probing and denied calls | `responseStatus.code` (403 = forbidden) grouped by `user.username` |
| Impersonation | presence of `impersonatedUser` (with `user` as the real caller) |
Filter on `stage == "ResponseComplete"` to avoid counting one request at several stages
(`RequestReceived`, `ResponseStarted`, `ResponseComplete`, `Panic`). What gets logged at all is
set by the policy file's `level` per rule, so an event you need must be covered by a rule.

## Managed
On managed control planes you do not set these flags; see the sibling skill
`computing-software.cloud-infrastructure-engineering.kubernetes.managed-cluster-audit-logs-eks-gke-aks`.

## Verify
- [ ] The newest line of the log file is a recent JSON event; rotated files are bounded by maxbackup/maxsize.
- [ ] A test `kubectl exec` shows up with `objectRef.subresource: exec` in the destination you ship logs to.

## Checked
Checked 2026-10-24 against the kubernetes/website "Auditing" page (log and webhook backend flags,
hostPath mounts, metrics), the kube-apiserver flag reference (`--audit-log-format` json/legacy,
`--audit-log-mode` batch/blocking/blocking-strict) and the `audit.k8s.io/v1` Go types (field names
and stages).
Method: documentation only; no commands were run.
