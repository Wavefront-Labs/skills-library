---
id: computing-software.cloud-infrastructure-engineering.kubernetes.kubernetes-audit-logging
name: kubernetes-audit-logging
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, audit-logging, audit-policy, apiserver, requestreceived, responsestarted, responsecomplete, webhook-backend, falco, siem, forensics, managed-kubernetes, eks, gke, aks, cloudtrail, audit-levels, omitstages]
level: advanced
status: docs-checked
description: "kube-apiserver audit policy stages/levels, log-vs-webhook backends, the specific verbs/resources worth alerting on, and the managed-Kubernetes audit gaps."
sources: ["https://kubernetes.io/docs/tasks/debug/debug-cluster/audit/", "https://kubernetes.io/docs/reference/config-api/apiserver-audit.v1/"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Kubernetes audit logging — the record of who did what to the API

**Goal:** have a record that actually answers "who created/read/deleted this"
after an incident, instead of discovering post-hoc that audit logging was on but
set to a level that recorded nothing useful, or that it was never shipped
anywhere durable. CIS Benchmark checks that reference audit config are in
`computing-software.cloud-infrastructure-engineering.kubernetes.cis-kubernetes-benchmark-and-kube-bench`.

## 1. Stages — events can be generated at four points
`RequestReceived` (as soon as the audit handler receives the request) → `ResponseStarted`
(response headers sent; generated only for long-running requests such as watch) → `ResponseComplete`
(body finished) → `Panic` (only when a panic occurred). Most policies set
`omitStages: [RequestReceived]` so that each request produces fewer events, and keep
`ResponseComplete` where the full outcome is known.

## 2. Levels — the dial that determines whether logs are useful at all
- `None` — don't log matching requests at all (use to exclude noisy,
  low-value traffic: health checks, `get`/`watch` on ConfigMaps by every node's
  kubelet).
- `Metadata` — who, what verb, what resource, when — **no request/response
  body**. Cheap, high-volume-friendly, but a `Metadata`-only audit of `secrets`
  tells you *someone read a Secret*, not *what was in it* or *whether the value
  changed* on an update.
- `Request` — adds the request body. For `secrets`, this means the plaintext
  value being written is **in the audit log** on every create/update — audit log
  storage then needs the same access control and retention care as Secrets
  themselves, which is easy to forget when audit logs ship to a general SIEM with
  broader read access than the cluster's RBAC.
- `RequestResponse` — adds both bodies; highest volume, most forensic value.
  Common practice: `Metadata` broadly, `RequestResponse` narrowly on genuinely
  sensitive resources/verbs (RBAC objects, exec, Secrets access by non-system
  identities) rather than blanket `RequestResponse` everywhere.
```yaml
apiVersion: audit.k8s.io/v1
kind: Policy
rules:
- level: RequestResponse
  resources: [{group: "rbac.authorization.k8s.io", resources: ["*"]}]
- level: Metadata
  resources: [{group: "", resources: [secrets, configmaps]}]
- level: None
  users: [system:kube-proxy]
  verbs: [watch]
- level: Metadata
  omitStages: [RequestReceived]
```
Rules are evaluated **top to bottom, first match wins** — ordering bugs (a
broad catch-all rule placed before a narrow exclusion) are the most common
reason a policy "should" log something and doesn't.

## 3. `kubectl exec`/`attach`/`port-forward` deserve an explicit rule
These are requests on the `pods/exec`, `pods/attach` and `pods/portforward` subresources. A rule
for `pods` does not match subresources (the Kubernetes example policy notes that `pods` does not
match any subresource of pods), so name them explicitly, for example
`resources: [{group: "", resources: ["pods/exec", "pods/attach", "pods/portforward"]}]`, and
keep them at `Metadata` or higher. Interactive exec into a running container is a common
incident-response and insider-threat vector. Review a sample event for these subresources to see
which fields your chosen level records; the audit levels `Request` and `RequestResponse` add the
request and response bodies and do not apply to non-resource requests.

## 4. Backends — where the events actually go
- `--audit-log-path` writes to a local file on the control-plane node — useless
  if the node is also what got compromised/destroyed; always ship off-node.
- `--audit-webhook-config-file` streams events to an external receiver
  (a SIEM, an event pipeline, a cloud function). The default `--audit-webhook-mode` is `batch`:
  events are buffered and sent asynchronously, so a slow or down receiver does not block API
  responses; `blocking` blocks responses on each event and
  `blocking-strict` also fails the request if auditing fails at the `RequestReceived` stage.
  Monitor the receiver's health independently. The log backend defaults to `blocking`.
- On managed Kubernetes, the provider decides which control-plane audit logs exist, where they go
  and how long they are retained. Check in the provider's documentation and on each cluster that
  audit logging is enabled, and that retention covers your incident-response window.

## 5. What a mature setup actually alerts on
- Any `create`/`update`/`patch` on `clusterrolebindings`/`rolebindings` binding
  to `cluster-admin` or any wildcard-permission role.
- `exec`/`attach` into `kube-system` or any namespace holding secrets a given
  team shouldn't touch.
- `get`/`list` on `secrets` by an identity with no legitimate reason to (cross-
  reference against the RBAC audit in `k8s-rbac-and-security`'s `can-i --list`
  sweep — an alert that fires on *every* legitimate Secret read by apps that need
  it is useless noise).
- Any request from `system:anonymous` that wasn't rejected.
- Impersonation headers (`Impersonate-User`) on a request not from a known
  automation identity.

## Gotchas
- The policy field `omitManagedFields: true` (also settable per rule) strips `managedFields` from
  logged request and response objects; it is mostly noise, so turn it on to reduce
  `Request`/`RequestResponse` log volume.
- High-volume `watch` traffic (every controller, every `kubectl get -w`) can
  dominate audit log volume if not explicitly excluded — a policy that doesn't
  address `watch` verbs separately tends to produce mostly-watch-noise logs that
  bury the events you actually care about.
- `--audit-log-maxage`, `--audit-log-maxbackup` and `--audit-log-maxsize` rotate and delete local files,
  so without an external shipper old events are deleted with no second copy — audit logs
  written only to local files on a kubeadm control-plane node are one disk-full
  event away from gaps, in addition to the single-node-compromise risk in §4.

## Verify
- [ ] Audit events ship off the control-plane node (webhook/managed-provider
      logging), not only to a local file.
- [ ] `pods/exec`, `pods/attach` and `pods/portforward` have an explicit audit rule.
- [ ] RBAC-object and Secret access have explicit, deliberate levels — not
      whatever the first matching rule happened to produce.
- [ ] Managed-Kubernetes control-plane audit logging is confirmed *enabled* and
      its retention period matches your incident-response requirements.
- [ ] At least the alert list in §5 has a working detection, tested against a
      deliberate benign trigger (e.g. a test `cluster-admin` binding in a
      throwaway cluster) to confirm it actually fires.

## Checked
Checked 2026-10-23 against the kubernetes/website docs (current release 1.37) and kubernetes/kubernetes audit v1 types.
Confirmed: stage definitions (ResponseStarted only for long-running requests); levels and first-match rule order; resources
wildcard `*` and subresource matching; `omitManagedFields` policy and rule fields; backends, `--audit-webhook-mode` default
`batch` and `--audit-log-mode` default `blocking`; `--audit-log-max*` flags. Wrong in the original: "up to four events per
request", webhook failures described as silently non-blocking by default without the mode distinction, and the claim that the
exec command lives in the request body (removed, unconfirmed). Removed unconfirmed managed-provider specifics (EKS, GKE, AKS
defaults); the former prose `sources` entries are replaced with the Kubernetes audit pages.
Method: documentation only; no commands were run.
