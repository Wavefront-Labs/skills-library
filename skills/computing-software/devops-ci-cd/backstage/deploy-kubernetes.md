---
id: computing-software.devops-ci-cd.backstage.deploy-kubernetes
name: deploy-kubernetes
category: computing-software
field: devops-ci-cd
product: backstage
tags: [kubernetes-deployment, postgres-secret, backstage-namespace, backstage]
level: practitioner
status: docs-checked
description: "Deploy Backstage and PostgreSQL to Kubernetes with a namespace, secrets, storage and a Deployment."
sources:
  - https://backstage.io/docs/deployment/k8s
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

The Kubernetes guide shows Backstage running as a stateless application with an external PostgreSQL database: you reference your Docker image in a Deployment and apply it to a cluster.

Steps from the docs:

1. Create a namespace manifest for `backstage` and apply it with `kubectl apply -f kubernetes/namespace.yaml`.
2. Create PostgreSQL credentials as a Secret. Values are base64-encoded, for example `echo -n "backstage" | base64`.
3. Create storage: a PersistentVolume and PersistentVolumeClaim (the docs example uses 2G and `ReadWriteOnce`).
4. Deploy PostgreSQL with a Deployment and Service.
5. Deploy Backstage with a Deployment and Service that reference the image and the database secret.

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: postgres-secrets
  namespace: backstage
type: Opaque
data:
  POSTGRES_USER: <base64>
  POSTGRES_PASSWORD: <base64>
```

Backstage reads the database credentials from environment variables mapped in `app-config.production.yaml`, for example `${POSTGRES_HOST}` and `${POSTGRES_PASSWORD}`, injected from the Secret through `envFrom` or `env` entries.

The example uses minikube and a local `hostPath` volume for testing. In production the image tag is generally a full URL to a container registry, and the Service is exposed through an ingress or external load balancer.

## Checked

2026-11-03. Confirmed on the Kubernetes deployment page: stateless app with external PostgreSQL, minikube for local testing, namespace, base64 Secret for PostgreSQL credentials, a PersistentVolume and claim of 2G with `ReadWriteOnce` and `hostPath`, PostgreSQL Deployment and Service, `envFrom` secret references and `${POSTGRES_HOST}`, `kubectl apply -f`, the production registry image tag and ingress or load balancer exposure. Removed: the "Spotify-style" wording and the managed-PostgreSQL and secret-tooling advice, which the page does not give.

Method: documentation only; no commands were run.
