---
id: computing-software.cloud-infrastructure-engineering.kubernetes.detect-secret-access-in-audit-logs
name: detect-secret-access-in-audit-logs
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, audit-logging, audit-secret-access, audit-log-analysis, secret-exposure, siem]
level: practitioner
status: docs-checked
description: "Hunt in audit logs for Secret reads, list/watch of secrets, pods/exec and token creation by audit event field, and build alerts that avoid system noise."
sources: ["https://kubernetes.io/docs/tasks/debug/debug-cluster/audit/", "https://kubernetes.io/docs/reference/config-api/apiserver-audit.v1/", "https://kubernetes.io/docs/reference/labels-annotations-taints/audit-annotations/", "https://kubernetes.io/docs/concepts/security/rbac-good-practices/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Detecting Secret access and exec in audit logs

Prerequisite: the audit policy must log the relevant requests. Audit levels are `None`, `Metadata`
(user, timestamp, resource, verb; no request or response body), `Request` and `RequestResponse`.
`Metadata` is enough for every query below and avoids writing Secret contents to the log, so use
`Metadata` (not `RequestResponse`) for `secrets` unless you have a specific need. Make sure a rule
covers `secrets`, `pods/exec`, `pods/attach` and `serviceaccounts/token`.

Audit events are `audit.k8s.io/v1` Event objects. The fields used below: `verb`, `user.username`,
`impersonatedUser`, `objectRef.{resource,subresource,namespace,name}`, `requestURI`, `userAgent`,
`requestReceivedTimestamp`, `responseStatus.code`, `stage`, and `annotations`.

## Secret reads by humans or unexpected service accounts
Filter events where `objectRef.resource == "secrets"` and `verb` is `get`, `list` or `watch`, then
exclude your known system identities (control plane components, kube-system controllers) by
`user.username`. Report `requestReceivedTimestamp`, `user.username`, `verb`, `objectRef.namespace`,
`objectRef.name`, `userAgent` and `responseStatus.code`.
Kubernetes' RBAC good-practices page warns that `list` and `watch` on Secrets also effectively
reveal their contents (for example `kubectl get secrets -A -o yaml` returns every Secret), so treat
cluster-wide lists by humans as high severity.

## Exec and attach
Filter on `objectRef.subresource` equal to `exec` or `attach` (resource `pods`). Report the user,
`objectRef.name`, `objectRef.namespace` and `requestURI`.

## Token minting and impersonation
- Token creation: `objectRef.resource == "serviceaccounts"` with `objectRef.subresource == "token"`.
- Impersonation: events that have `impersonatedUser`; `user` is then the real caller.

## Denied attempts (reconnaissance)
Events whose `annotations["authorization.k8s.io/decision"]` is `forbid` (the documented values are
`forbid` and `allow`) and `objectRef.resource == "secrets"`; group by `user.username` and `verb`.

## Counting each request once
A request can appear at several stages (`RequestReceived`, `ResponseStarted`, `ResponseComplete`,
`Panic`); filter on `stage == "ResponseComplete"` for counts.

## Turning it into alerts
- Baseline which service accounts legitimately read which Secrets (controllers, certificate and
  secret-sync operators); alert on anything new.
- Ship the audit log to your log or SIEM platform and express the filters above in its query language.
  On managed clusters, see
  `computing-software.cloud-infrastructure-engineering.kubernetes.managed-cluster-audit-logs-eks-gke-aks`.

## Checked
Checked 2026-10-24 against the kubernetes/website Auditing page (audit levels), the `audit.k8s.io/v1`
Event Go types (field names, stages, `requestURI`, `impersonatedUser`), the audit annotations page
(`authorization.k8s.io/decision` with values `forbid` or `allow`) and the RBAC good-practices page
(`list` and `watch` on Secrets expose contents). Removed: jq pipelines, the claim that the exec
command is visible in `requestURI`, and third-party detection rule names, which no checked documentation covers.
Method: documentation only; no commands were run.
