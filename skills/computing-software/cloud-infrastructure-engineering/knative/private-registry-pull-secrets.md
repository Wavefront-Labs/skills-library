---
id: computing-software.cloud-infrastructure-engineering.knative.private-registry-pull-secrets
name: private-registry-pull-secrets
category: computing-software
field: cloud-infrastructure-engineering
product: knative
tags: [imagepullsecrets, private-registry, docker-registry-secret, service-account]
level: practitioner
status: docs-checked
description: "Deploy images from a private registry using imagePullSecrets on the Service or default service account."
sources:
  - https://knative.dev/docs/serving/deploying-from-private-registry/
  - https://knative.dev/docs/serving/tag-resolution/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: let Revisions pull from a registry that needs credentials.

Prerequisites: a cluster with Knative Serving installed and credentials for the private registry.

1. Create the secret:

```bash
kubectl create secret docker-registry container-registry \
  --docker-server=<private-registry-url> \
  --docker-email=<private-registry-email> \
  --docker-username=<private-registry-user> \
  --docker-password=<private-registry-password>
```

The name `container-registry` is the example name for your `imagePullSecrets` entry. Inspect it with `kubectl get secret container-registry -o=yaml`.

2. Optional: attach it to the `default` service account of the namespace, which Revisions use unless you specify another:

```bash
kubectl patch serviceaccount default -p "{\"imagePullSecrets\": [{\"name\": \"container-registry\"}]}"
```

New pods in that namespace then carry the credentials.

3. Optional: attach it to one Service:

```yaml
spec:
  template:
    spec:
      imagePullSecrets:
      - name: <secret-name>
      containers:
        - image: ghcr.io/knative/helloworld-go:latest
```

Related: Serving resolves image tags to digests when it creates a Revision, so the controller itself must be able to reach the registry. For a registry with a self-signed certificate, mount the CA into the `controller` Deployment and set the environment variable (`SSL_CERT_FILE` or `SSL_CERT_DIR`) so the tag resolution request trusts it.

## Checked

2026-11-04. Confirmed against the Deploying images from a private container registry page and the Tag resolution page (knative/docs source): prerequisites, the `kubectl create secret docker-registry` command with its four flags, viewing the secret, that Revisions use the `default` service account unless `serviceAccountName` is set, the patch command (the page applies it to the `default` service account in the `default` namespace), the Service-level `imagePullSecrets` example, tag-to-digest resolution at Revision creation, the controller needing registry access, and the self-signed certificate mount with `SSL_CERT_FILE` or `SSL_CERT_DIR`. Added the two variable names and the tag resolution page to sources. Nothing removed.

Method: documentation only; no commands were run.
