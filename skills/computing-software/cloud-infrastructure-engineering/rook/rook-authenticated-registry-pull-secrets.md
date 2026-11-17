---
id: computing-software.cloud-infrastructure-engineering.rook.rook-authenticated-registry-pull-secrets
name: rook-authenticated-registry-pull-secrets
category: computing-software
field: cloud-infrastructure-engineering
product: rook
tags: [authenticated-registry, imagepullsecrets, docker-registry, serviceaccount, image-mirror]
level: practitioner
status: docs-checked
description: "Let Rook pods pull images from an authenticated registry by creating a docker-registry secret and adding it to the Rook service accounts."
sources:
  - https://rook.io/docs/rook/latest-release/Getting-Started/Prerequisites/authenticated-registry/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
To use images from an authenticated registry such as a cache or mirror, add `imagePullSecrets` to every relevant Rook service account.

Step 1: create the secret in the namespace of the operator and cluster (the docs use `rook-ceph`):
```
kubectl -n rook-ceph create secret docker-registry my-registry-secret \
  --docker-server=DOCKER_REGISTRY_SERVER --docker-username=DOCKER_USER \
  --docker-password=DOCKER_PASSWORD --docker-email=DOCKER_EMAIL
```

Step 2: edit each service account, for example `kubectl -n rook-ceph edit serviceaccount rook-ceph-default`, and add:
```
imagePullSecrets:
- name: my-registry-secret
```

Service accounts to patch, all in namespace `rook-ceph`:
- `rook-ceph-system`: pods created by the Rook operator
- `rook-ceph-default`: most pods in the namespace
- `rook-ceph-mgr`: manager pods
- `rook-ceph-osd`: OSD pods
- `rook-ceph-rgw`: object gateway pods

Change the namespace everywhere if your operator and cluster live elsewhere. After every service account carries the pull secret, all pods should be able to pull from the private registry.

## Checked

2026-11-03. Read the Rook authenticated-registry page (cited in sources) against this skill: the `imagePullSecrets` snippet, the secret and service account names and the namespace were matched to the page text. Removed the unsourced troubleshooting self-check about `ImagePullBackOff`.

Method: documentation only; no commands were run.
