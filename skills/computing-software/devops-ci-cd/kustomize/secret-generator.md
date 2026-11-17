---
id: computing-software.devops-ci-cd.kustomize.secret-generator
name: secret-generator
category: computing-software
field: devops-ci-cd
product: kustomize
tags: [secretgenerator, secret, tls, type, base64]
level: practitioner
status: docs-checked
description: "Generate Secrets from files, literals or env files with a type, namespace and options; output values are base64 encoded."
sources:
  - "https://kubectl.docs.kubernetes.io/references/kustomize/kustomization/secretgenerator/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

`secretGenerator` works like `configMapGenerator`: each entry creates one Secret from `files`, `literals` or `envs`.

```yaml
secretGenerator:
- name: app-tls
  files:
  - secret/tls.crt
  - secret/tls.key
  type: "kubernetes.io/tls"
- name: app-tls-namespaced
  namespace: apps          # defaults to "default"
  files:
  - tls.crt=catsecret/tls.crt
  - tls.key=secret/tls.key
  type: "kubernetes.io/tls"
- name: env_file_secret
  envs:
  - env.txt
  type: Opaque
- name: secret-with-annotation
  files:
  - app-config.yaml
  type: Opaque
  options:
    annotations:
      app_config: "true"
    labels:
      app.kubernetes.io/name: "app2"
```

The Secret type is set with `type`. The build output encodes values as base64 and names the Secret with a hash suffix such as `app-tls-c888dfbhf8`.

From the Kubernetes task page, literals work too: `username=admin` and `password=secret` under `literals`, and the Deployment can use `secret: secretName: example-secret-1` with kustomize substituting the hashed name.

Important: the reference page notes that the Secrets are base64 encoded. Base64 is an encoding, not encryption, so keep plain secret source files out of version control.

## Checked

2026-11-03. Confirmed against: the secretGenerator reference page, the built-ins page and the task page.
Removed or reworded: the external-secret recommendation.

Method: documentation only; no commands were run.
