---
id: computing-software.devops-ci-cd.awx-operator.awx-operator-custom-images-and-private-registries
name: awx-operator-custom-images-and-private-registries
category: computing-software
field: devops-ci-cd
product: awx-operator
tags: [awx-operator, image, image-pull-secrets, ee-images, control-plane-ee, private-registry, mirror]
level: practitioner
status: docs-checked
description: "Run AWX from mirrored or private-registry images, set pull secrets and register default execution environments with pull credentials."
sources: ["https://github.com/ansible/awx-operator/blob/devel/docs/user-guide/advanced-configuration/deploying-a-specific-version-of-awx.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Awx operator custom images and private registries

Image variables (defaults): `image` (quay.io/ansible/awx), `image_version` (DEFAULT_AWX_VERSION or latest), `image_pull_policy` (IfNotPresent), `image_pull_secrets`, `ee_images` (quay.io/ansible/awx-ee:DEFAULT_AWX_VERSION), `ee_pull_credentials_secret`, `redis_image` (docker.io/redis) and `redis_image_version` (latest), `control_plane_ee_image`, `init_container_image` (quay.io/ansible/awx-ee) with `init_container_image_version`, and `init_projects_container_image` (quay.io/centos/centos:stream9).

```yaml
spec:
  image: myorg/my-custom-awx
  image_version: latest
  image_pull_policy: Always
  image_pull_secrets:
    - pull_secret_name
  ee_images:
    - name: my-custom-awx-ee
      image: myorg/my-custom-awx-ee
  control_plane_ee_image: myorg/my-custom-awx-ee:latest
  init_projects_container_image: myorg/my-mirrored-centos:stream9
```

`image` and `image_version` are for local mirroring. Using an AWX version other than the one bundled with the operator is not supported.

Private registry for default EEs: store credentials in a Secret and set `ee_pull_credentials_secret` (or the default name `<resourcename>-ee-pull-credentials`) with keys `url`, `username`, `password` and optional `ssl_verify` ("True" default or "False"). The images in `ee_images` become globally available EEs; `control_plane_ee_image` runs project updates. For private images there use `image_pull_secrets`, e.g. a `kubernetes.io/dockerconfigjson` Secret named `<resourcename>-cp-pull-credentials`.

Remember the AWX pull secret is separate from the EE pull credentials: `image_pull_secrets` is the list of pull secrets for the pods, while `ee_pull_credentials_secret` carries the registry URL, username, password and optional `ssl_verify` used when registering `ee_images`.

## Checked

2026-11-09. Confirmed the variable names and defaults, the example spec, the local mirroring warning, the EE pull credentials Secret format and the control plane pull secret guidance against the AWX Operator page on private registries (read in full).

Method: docs-checked 2026-11-09 against the AWX Operator docs page docs/user-guide/advanced-configuration/deploying-a-specific-version-of-awx.md
