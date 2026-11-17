---
id: computing-software.devops-ci-cd.argo-events.argo-events-trigger-k8s-object-operations
name: argo-events-trigger-k8s-object-operations
category: computing-software
field: devops-ci-cd
product: argo-events
tags: [argo-events, k8s-trigger, create, update, patch, delete, operation, rbac]
level: practitioner
status: docs-checked
description: "Create, update, patch or delete any Kubernetes object from a Sensor trigger, with parameters to inject event data."
sources: ["https://github.com/argoproj/argo-events/blob/master/docs/sensors/triggers/k8s-object-trigger.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Argo events trigger k8s object operations

Besides Argo Workflows, the `k8s` trigger can act on any Kubernetes object, custom resources included (Pod, Deployment, Job, CronJob, ...), which sets up event-driven pipelines for existing workloads.

`k8s.operation` is one of:
- `create`: creates the object if not available in the cluster.
- `update`: updates the object.
- `patch`: patches it using the given patch strategy.
- `delete`: deletes the object if it exists.

Example creating a Pod with the event payload as an argument; the Sensor's service account must be able to create Pods:

```yaml
spec:
  template:
    serviceAccountName: create-pod-sa
  triggers:
    - template:
        name: webhook-pod-trigger
        k8s:
          operation: create
          source:
            resource:
              apiVersion: v1
              kind: Pod
              metadata:
                generateName: hello-world-
              spec:
                containers:
                  - name: hello-container
                    command: [echo]
                    args: ["hello-world"]
                    image: busybox
          parameters:
            - src:
                dependencyName: test-dep
              dest: spec.containers.0.args.0
```

`parameters` write event content into the resource by destination path (here `spec.containers.0.args.0`). The parameter above sets no `dataKey`; after the Pod completes, its logs show a JSON event with a `context` object and a base64-encoded `data` string.

## Checked

2026-11-07: Read in full from a local clone of the argoproj/argo-events docs (master), which is the source of the cited GitHub page: docs/sensors/triggers/k8s-object-trigger.md. Confirmed: operation values create/update/patch/delete, Pod example, serviceAccountName, parameter destination, logged event shape. Removed or changed: the claim that without dataKey the whole event body is used, reworded to what the page shows. The example manifests the page links to (under examples/) were not opened; only snippets printed on the page were checked.

Method: documentation only; no commands were run.
