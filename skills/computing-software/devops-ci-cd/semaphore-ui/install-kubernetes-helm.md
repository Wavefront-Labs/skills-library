---
id: computing-software.devops-ci-cd.semaphore-ui.install-kubernetes-helm
name: install-kubernetes-helm
category: computing-software
field: devops-ci-cd
product: semaphore-ui
tags: [kubernetes, helm, helm-chart, installation, semaphore-ui]
level: intro
status: docs-checked
description: "Where the official Semaphore Helm chart lives and how to approach a Kubernetes deployment."
sources:
  - https://semaphoreui.com/docs/admin-guide/installation/k8s
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Install Semaphore on Kubernetes

Goal: deploy Semaphore UI to a Kubernetes cluster with the official Helm chart.

Semaphore publishes a Helm chart named `semaphore` in the `semaphoreui` repository on Artifact Hub (artifacthub.io, package `semaphoreui/semaphore`). The Semaphore docs page only links to the chart's documentation on Artifact Hub.

Practical approach:
1. Read the chart's documentation on Artifact Hub.
2. Provide the same settings the Docker install needs: database dialect, host and credentials, the admin user, and `access_key_encryption`.
3. Keep secrets in Kubernetes Secrets, not in values files. For encryption keys, a mounted Secret works with `encryption.keys_folder`, which skips Kubernetes dot-prefixed entries and follows symlinks.
4. Pick PostgreSQL or MySQL rather than the SQLite default when more than a few people depend on the service or you plan several nodes.
5. Put a load balancer or ingress in front that supports WebSocket traffic; the HA page's NGINX example gives `/api/ws` its own location (see the reverse proxy skills).

For several replicas you need the Enterprise HA setup with Redis (see the HA skills); SQLite does not work for that.

Verify: `kubectl get pods` shows the Semaphore pod ready and the ingress URL serves the login page.

## Checked

2026-11-04: checked against the Kubernetes installation and high availability pages. The docs page only links to the chart; unconfirmed claims about chart values were removed.

Method: documentation only; no commands were run.
