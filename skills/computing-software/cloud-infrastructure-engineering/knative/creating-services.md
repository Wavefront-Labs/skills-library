---
id: computing-software.cloud-infrastructure-engineering.knative.creating-services
name: creating-services
category: computing-software
field: cloud-infrastructure-engineering
product: knative
tags: [kn-service-create, knative-service, revision, creating-services, route-configuration]
level: intro
status: docs-checked
description: "Create a Service with YAML or kn service create and know what Knative generates from it."
sources:
  - https://knative.dev/docs/serving/services/creating-services/
  - https://knative.dev/docs/serving/services/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: deploy an application as a Knative Service.

Prerequisites: a Kubernetes cluster with Knative Serving installed, and optionally the `kn` CLI.

With YAML:

```yaml
apiVersion: serving.knative.dev/v1
kind: Service
metadata:
  name: helloworld-go
  namespace: default
spec:
  template:
    spec:
      containers:
        - image: ghcr.io/knative/helloworld-go:latest
          env:
            - name: TARGET
              value: "Go Sample v1"
```

Apply with `kubectl apply -f <filename>.yaml`. With the CLI:

```bash
kn service create helloworld-go --image ghcr.io/knative/helloworld-go:latest
```

After creation Knative:
- creates a new immutable Revision for this version of the app;
- programs the network: a route, ingress, service and load balancer;
- scales pods automatically with traffic, including down to zero.

Object model: each Service is defined by a Route and a Configuration with the same name, created by the service controller from the Service spec. Every configuration update creates a new Revision, an immutable snapshot that uses Kubernetes resources to scale pods. Changes to the Service's spec, labels or annotations are copied to its Route and Configuration. The Service carries `RoutesReady`, `ConfigurationsReady` and `Ready` conditions.

## Checked

2026-11-04. Confirmed against the creating-services page and the Knative Services overview page (knative/docs source): prerequisites, the YAML and `kn service create` examples, the three tasks Knative performs after creation, Route and Configuration of the same name created by the service controller, immutable Revisions, changes copied to the Route and Configuration, and the `RoutesReady`, `ConfigurationsReady` and `Ready` conditions. Added the overview page to sources. Nothing removed.

Method: documentation only; no commands were run.
