---
id: computing-software.cloud-infrastructure-engineering.knative.convert-deployment
name: convert-deployment
category: computing-software
field: cloud-infrastructure-engineering
product: knative
tags: [convert-deployment, workload-fit, stateless, kubernetes-deployment]
level: intro
status: docs-checked
description: "Decide whether a Kubernetes Deployment fits Knative and convert it to a Service."
sources:
  - https://knative.dev/docs/serving/convert-deployment-to-knative-service/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: replace a Deployment plus Service with a single Knative Service.

Benefits:
- A smaller footprint, because the instance scales to zero when idle.
- Better performance from the built-in autoscaling.

Is the workload a good fit? A good fit lets you delete much of the manifest. Check three things:
- All work is triggered by HTTP.
- The container is stateless: state is stored elsewhere or can be re-created.
- The workload uses only Secret and ConfigMap volumes.

Example: the page converts the Kubernetes Nginx Deployment (`my-nginx`, 2 replicas) and its Service into one Knative Service.

```yaml
apiVersion: serving.knative.dev/v1
kind: Service
metadata:
  name: my-nginx
spec:
  template:
    spec:
      containers:
        - image: nginx
          ports:
            - containerPort: 80
```

The Deployment's selector, labels and replica count, and the separate Service object with its port and selector, all disappear; the single Knative Service replaces both.

## Checked

2026-11-04. Confirmed against the page on converting a Kubernetes Deployment to a Knative Service (knative/docs source): the two benefits, the three fit criteria, the Nginx Deployment plus Service example and the resulting Knative Service manifest. Removed the sentence saying Knative generates the Route, Configuration, Revision and networking, which this page does not state.

Method: documentation only; no commands were run.
