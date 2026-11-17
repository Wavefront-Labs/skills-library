---
id: computing-software.devops-ci-cd.argo-events.argo-events-trigger-sources-git-s3-configmap-url
name: argo-events-trigger-sources-git-s3-configmap-url
category: computing-software
field: devops-ci-cd
product: argo-events
tags: [argo-events, trigger-source, git, s3, configmap, file, url, inline, resource]
level: advanced
status: docs-checked
description: "Fetch the trigger resource from Git, S3-compatible storage, a ConfigMap, a file or a URL instead of defining it inline."
sources: ["https://github.com/argoproj/argo-events/blob/master/docs/tutorials/03-trigger-sources.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Argo events trigger sources git s3 configmap url

A trigger source is where the trigger resource comes from: external (Git, S3, a K8s ConfigMap, a file, any URL) or internal (`inline` or `resource` in the Sensor). Most examples use `resource`.

Git: the Sensor needs an SSH key and known hosts.

```sh
kubectl -n argo-events create secret generic git-ssh --from-file=key=.ssh/<YOUR_SSH_KEY_FILE_NAME>
kubectl -n argo-events create secret generic git-known-hosts --from-file=ssh_known_hosts=.ssh/known_hosts
```

Then use `examples/tutorials/03-trigger-sources/sensor-git.yaml`, which references a hello-world workflow in the Argo Git project (GitArtifact spec in the API docs).

S3: any S3-compatible store, e.g. Minio. Create a Secret `artifacts-minio` with `accesskey` and `secretkey`, expose the server by a Service, create a bucket `workflows` holding `hello-world.yaml`, and apply `sensor-minio.yaml`.

ConfigMap: apply `trigger-store.yaml` (a ConfigMap named `trigger-store`) and a sensor `sensor-cm.yaml` that refers to it.

File and URL sources are self-explanatory; samples are under `examples/sensors`.

In each case POST to the webhook endpoint and check `kubectl -n argo-events get wf` for the created Workflow.

## Checked

2026-11-07: Read in full from a local clone of the argoproj/argo-events docs (master), which is the source of the cited GitHub page: docs/tutorials/03-trigger-sources.md. Confirmed: list of trigger sources, Git secrets commands, S3 secret artifacts-minio keys, bucket workflows and hello-world.yaml, trigger-store ConfigMap, File and URL pointer. Removed or changed: nothing; every claim matched the page. The example manifests the page links to (under examples/) were not opened; only snippets printed on the page were checked.

Method: documentation only; no commands were run.
