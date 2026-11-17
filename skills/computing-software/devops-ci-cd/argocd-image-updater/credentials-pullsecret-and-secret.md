---
id: computing-software.devops-ci-cd.argocd-image-updater.credentials-pullsecret-and-secret
name: credentials-pullsecret-and-secret
category: computing-software
field: devops-ci-cd
product: argocd-image-updater
tags: [argocd-image-updater, pullsecret, secret, dockerconfigjson, kubectl-create-secret, credentials, pull-secret]
level: practitioner
status: docs-checked
description: "Reference registry credentials from Kubernetes Secrets: a docker-registry pull secret via pullsecret:ns/name, or a username:password field via secret:ns/name#field."
sources: ["https://github.com/argoproj-labs/argocd-image-updater/blob/master/docs/basics/authentication.md", "https://github.com/argoproj-labs/argocd-image-updater/blob/master/docs/configuration/images.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Credentials from Kubernetes Secrets

Pull secret. A secret with a `.dockerconfigjson` field in `.data`, the same kind Kubernetes uses to pull images. Create one:

```shell
kubectl create -n argocd secret docker-registry dockerhub-secret \
  --docker-username someuser \
  --docker-password s0m3p4ssw0rd \
  --docker-server "https://registry-1.docker.io"
```

Reference it as `pullsecret:argocd/dockerhub-secret`.

Generic secret. Useful when many registries share credentials and you do not want a pull secret per registry. Store `<username>:<password>` in any field of `.data`, and reference it as `secret:<namespace>/<secret_name>#<field_name>`, for example `secret:argocd/some-secret#creds`.

Rules:

- by default the updater reads secrets only from its own namespace
- in the `ImageUpdater` CR, the namespace in a `secret:` or `pullsecret:` reference must equal the CR's namespace; cross-namespace references are rejected with an error and the image is skipped
- pull secrets must exist in the cluster where the updater runs or has access to

Per image: `commonUpdateSettings.pullSecret: pullsecret:argocd/dockerhub-secret`. Per registry: `credentials: pullsecret:argocd/dockerhub-secret`.

## Checked

2026-11-04. Confirmed against authentication.md (pull secret and generic secret notation, the kubectl create secret docker-registry example, same-namespace default), images.md (pullSecret, cross-namespace references rejected, secret must exist where the updater runs) and registries.md (credentials property).

Method: documentation only; no commands were run.
