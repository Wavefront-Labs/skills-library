---
id: computing-software.devops-ci-cd.argo-events.argo-events-trigger-k8s-policy-resource-labels
name: argo-events-trigger-k8s-policy-resource-labels
category: computing-software
field: devops-ci-cd
product: argo-events
tags: [argo-events, trigger-policy, resource-labels, backoff, erroronbackofftimeout, k8s-trigger]
level: advanced
status: docs-checked
description: "Decide whether a triggered Kubernetes object succeeded by polling its labels with a backoff, and fail the trigger on timeout."
sources: ["https://github.com/argoproj/argo-events/blob/master/docs/sensors/triggers/k8s-object-trigger.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Argo events trigger k8s policy resource labels

A trigger `policy` tells the Sensor whether the object it created reached a success state, so it can stop or continue. Because the Sensor can trigger any resource, the K8s policy determines state from the resource's labels (`Resource Labels` policy):

```yaml
policy:
  k8s:
    backoff:
      duration: 1000000000   # nanoseconds, here 1 second
      factor: 2
      jitter: 0.1
      steps: 5
    labels:
      workflows.argoproj.io/phase: Succeeded
    errorOnBackoffTimeout: true
```

- `backoff`: wait before checking the labels, repeated up to `steps` times, with the duration multiplied by `factor` and perturbed by `jitter`. Note `duration` here is given in nanoseconds.
- `labels`: labels the object must carry to be considered successful (here the Argo Workflow phase label).
- `errorOnBackoffTimeout`: whether the trigger is marked failed if the backoff times out while the state is still undetermined; defaults to false.

A complete example is `examples/sensors/trigger-with-policy.yaml`.

## Checked

2026-11-07: Read in full from a local clone of the argoproj/argo-events docs (master), which is the source of the cited GitHub page: docs/sensors/triggers/k8s-object-trigger.md. Confirmed: Resource Labels policy, backoff duration/factor/jitter/steps, labels, errorOnBackoffTimeout default false. Removed or changed: the sentence generalising the policy to Argo Workflow, HTTP and Lambda triggers (other pages). The example manifests the page links to (under examples/) were not opened; only snippets printed on the page were checked.

Method: documentation only; no commands were run.
