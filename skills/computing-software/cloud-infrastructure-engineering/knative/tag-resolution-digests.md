---
id: computing-software.cloud-infrastructure-engineering.knative.tag-resolution-digests
name: tag-resolution-digests
category: computing-software
field: cloud-infrastructure-engineering
product: knative
tags: [tag-resolution, image-digest, self-signed-certificate, proxy]
level: advanced
status: docs-checked
description: "Understand digest resolution and trust a self-signed registry CA or corporate proxy from the Serving controller."
sources:
  - https://knative.dev/docs/serving/tag-resolution/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: keep Revisions consistent by pinning image tags to digests, and make that work with your registry.

Knative Serving resolves image tags to a digest when you create a Revision. This gives consistency for Deployments. The Serving controller must be configured to access the container registry for this to work; behind a corporate proxy you must proxy the tag resolution requests between the controller and your registry.

Custom certificates: for a registry with a self-signed certificate, configure the default Knative Serving `controller` Deployment to trust it by mounting your certificates into the Deployment and setting an environment variable pointing at them. If a `custom-certs` secret holds your CA certificates, add a volume from that secret, a `volumeMounts` entry on the `controller` container, and `SSL_CERT_DIR` set to the mount path, in namespace `knative-serving`. Knative Serving accepts the `SSL_CERT_FILE` and `SSL_CERT_DIR` variables.

Corporate proxy: Knative accepts the `HTTP_PROXY` and `HTTPS_PROXY` environment variables, so set them on the `controller` container of the same Deployment.

## Checked

Method: docs-checked 2026-11-09 against the Tag resolution page (raw markdown in knative/docs, read in full). Dropped the `registries-skipping-tag-resolving` and `digest-resolution-timeout` config-deployment keys and the private registry note, none of which appear on this page.
