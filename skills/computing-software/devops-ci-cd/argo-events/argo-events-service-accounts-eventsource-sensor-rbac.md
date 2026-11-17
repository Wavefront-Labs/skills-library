---
id: computing-software.devops-ci-cd.argo-events.argo-events-service-accounts-eventsource-sensor-rbac
name: argo-events-service-accounts-eventsource-sensor-rbac
category: computing-software
field: devops-ci-cd
product: argo-events
tags: [argo-events, service-account, rbac, resource-eventsource, least-privilege, sensor]
level: practitioner
status: docs-checked
description: "Grant EventSources and Sensors the minimum RBAC they need, and know which triggers need no service account at all."
sources: ["https://github.com/argoproj/argo-events/blob/master/docs/service-accounts.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Argo events service accounts eventsource sensor rbac

EventSource: set `spec.template.serviceAccountName`, but it is needed only for the `resource` EventSource type, which requires `list` and `watch` on the watched resource. To watch Deployments:

```sh
kubectl -n your-namespace create sa my-sa
kubectl -n your-namespace create role deployments-watcher --verb=list,watch --resource=deployments.apps
kubectl -n your-namespace create rolebinding deployments-watcher-role-binding --role=deployments-watcher --serviceaccount=your-namespace:my-sa
```

For cluster scope use `create clusterrole` and `create clusterrolebinding` instead.

Sensor: `spec.template.serviceAccountName` is needed only when the Sensor has a `k8s` or `argoWorkflow` trigger. The example `operate-workflow-sa` has more permission than necessary, so create a least-privilege account:
- argoWorkflow `submit`: `create` and `list` on `workflows.argoproj.io`.
- argoWorkflow `resubmit`, `retry`, `resume`, `suspend`: `update` and `get` on `workflows.argoproj.io`.
- `k8s` trigger (including workflows): `create` on that resource.
- AWS Lambda, HTTP, Slack, NATS, Kafka and OpenWhisk triggers: no service account needed.

Triggered Workflows have their own service account inside the Workflow spec (not `spec.template.serviceAccountName`); configure it as per Argo Workflows service-account documentation. For other triggered K8s resources such as a Deployment follow least privilege.

## Checked

2026-11-07: Read in full from a local clone of the argoproj/argo-events docs (master), which is the source of the cited GitHub page: docs/service-accounts.md. Confirmed: resource EventSource RBAC (list, watch) and the kubectl commands, k8s/argoWorkflow trigger permissions, triggers needing no service account, operate-workflow-sa remark. Removed or changed: nothing; every claim matched the page. The example manifests the page links to (under examples/) were not opened; only snippets printed on the page were checked.

Method: documentation only; no commands were run.
