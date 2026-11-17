---
id: computing-software.cloud-infrastructure-engineering.kubernetes.managed-cluster-audit-logs-eks-gke-aks
name: managed-cluster-audit-logs-eks-gke-aks
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, audit-logging, eks-audit-logs, gke-audit-logs, aks, managed-kubernetes]
level: practitioner
status: gated
description: "Turn on and query Kubernetes audit logs in EKS (CloudWatch), GKE (Cloud Audit Logs) and AKS (diagnostic settings), with costs and useful queries."
sources: ["https://docs.aws.amazon.com/eks/latest/userguide/control-plane-logs.html", "https://learn.microsoft.com/en-us/azure/aks/monitor-aks", "https://learn.microsoft.com/en-us/azure/aks/monitor-aks-reference", "https://github.com/kubernetes/kubernetes/blob/release-1.37/staging/src/k8s.io/apiserver/pkg/apis/audit/v1/types.go", "https://cloud.google.com/kubernetes-engine/docs/how-to/audit-logging"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Audit logs in EKS, GKE and AKS

Managed control planes do not expose audit files; each cloud ships them to its log service.

## EKS
```bash
aws eks update-cluster-config --name prod \
  --logging '{"clusterLogging":[{"types":["audit","authenticator"],"enabled":true}]}'
```
Log group `/aws/eks/prod/cluster`, audit streams `kube-apiserver-audit-*`. CloudWatch Logs
Insights over the Kubernetes audit event fields:
```
fields @timestamp, user.username, verb, objectRef.resource, objectRef.namespace, objectRef.name, responseStatus.code
| filter objectRef.resource = "secrets" and verb in ["get","list","watch"]
| sort @timestamp desc | limit 100
```
You pay standard CloudWatch Logs ingestion and storage for control plane logs; set log group
retention.

## GKE
Admin Activity audit logs (writes) are always on and free, while Data Access logs (reads) are
off by default and enabled through the IAM audit config
(gated: unconfirmed, source is paywalled or blocked). GKE documentation is not in a readable source repository for this review, so
confirm these defaults and the log filter below in the GKE audit logging docs.
```
resource.type="k8s_cluster"
logName="projects/<p>/logs/cloudaudit.googleapis.com%2Factivity"
protoPayload.resourceName:"secrets"
```
The filter above is (gated: unconfirmed, source is paywalled or blocked). It comes from GKE
documentation that could not be read.

## AKS
Diagnostic setting on the cluster resource with category `kube-audit` (all audit events) or
`kube-audit-admin` (excludes `get` and `list` events, much less data), sent to Log Analytics.
Microsoft recommends resource-specific mode, where audit events land in the `AKSAudit` table
(`kube-audit`) or `AKSAuditAdmin` (`kube-audit-admin`); Azure diagnostics mode uses
`AzureDiagnostics | where Category == "kube-audit"`. `kube-audit` collection can be expensive:
disable it when not needed, prefer `kube-audit-admin`, or set the `AKSAudit` table to the
Basic logs plan.
```kusto
AKSAudit
| take 10          // inspect the columns, then filter on verb and object reference
```

## Verify
Create and delete a test Secret, then find both events with the user identity in the cloud log.

## Checked
Checked 2026-10-27 against the Amazon EKS User Guide source (control plane logging:
`--logging` syntax, log group `/aws/eks/<cluster>/cluster`, `kube-apiserver-audit-*` streams,
CloudWatch charges), the Kubernetes audit.k8s.io/v1 Event type in kubernetes/kubernetes
release-1.37 (`user`, `verb`, `objectRef`, `responseStatus` fields) and MicrosoftDocs/azure-aks-docs
(Monitor AKS: `kube-audit` cost warning, `kube-audit-admin` excluding get and list,
resource-specific mode, `AKSAudit` and `AKSAuditAdmin` tables, `AzureDiagnostics` category).
Removed an AKSAudit query whose column names could not be confirmed, the "few minutes" delivery
time and the unconfirmed claim that managed audit policies cannot be changed. GKE claims are
gated because GKE docs were not readable.

Method: documentation only; no commands were run.
