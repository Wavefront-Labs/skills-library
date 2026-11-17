---
id: computing-software.cloud-infrastructure-engineering.longhorn.airgap-install
name: airgap-install
category: computing-software
field: cloud-infrastructure-engineering
product: longhorn
tags: [airgap, private-registry, images, imagepullsecrets, helm]
level: advanced
status: docs-checked
description: "Install Longhorn 1.13.0 offline: save and load images with the provided scripts, edit the manifest or Helm privateRegistry values, and fix missing pull secrets."
sources:
  - https://longhorn.io/docs/1.13.0/deploy/install/airgap/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: install from a private registry.

Mirror all Longhorn and CSI images first.

```bash
wget https://raw.githubusercontent.com/longhorn/longhorn/v1.13.0/deploy/longhorn-images.txt
wget https://raw.githubusercontent.com/longhorn/longhorn/v1.13.0/scripts/save-images.sh
chmod +x save-images.sh
./save-images.sh --image-list longhorn-images.txt --images longhorn-images.tar.gz
# on the air-gapped side, with scripts/load-images.sh downloaded the same way
./load-images.sh --image-list longhorn-images.txt --images longhorn-images.tar.gz --registry <YOUR-PRIVATE-REGISTRY>
```

Manifest method: download `deploy/longhorn.yaml`, create the `longhorn-system` namespace, and if the registry needs auth create a `docker-registry` secret and add it under `imagePullSecrets.name` in `longhorn-driver-deployer`, `longhorn-manager`, `longhorn-global-manager` and `longhorn-ui`. Set `CSI_ATTACHER_IMAGE`, `CSI_PROVISIONER_IMAGE`, `CSI_NODE_DRIVER_REGISTRAR_IMAGE`, `CSI_RESIZER_IMAGE`, `CSI_SNAPSHOTTER_IMAGE` and repoint `longhorn-manager`, `longhorn-engine`, `longhorn-instance-manager`, `longhorn-share-manager`, `longhorn-ui` images to the registry, then `kubectl apply -f longhorn.yaml`.

Helm method: since v1.13.0 Longhorn adds the registry prefix automatically, and setting `registryUrl` makes it pull only from that registry. In `chart/values.yaml` set `privateRegistry.createSecret`, `registryUrl`, `registryUser`, `registryPasswd`, `registrySecret` (the secret name must include the registry name). Custom image names go under `image.longhorn.*` and `image.csi.*` without the registry prefix. Then `helm install longhorn ./chart --namespace longhorn-system --create-namespace`.

If `longhorn-manager` fails for a missing pull secret, create the secret and a `Setting` named `registry-secret` in `longhorn-system` with `value: <SECRET_NAME>`, then reinstall.

Do not change image tags (instance manager tags are date based) and keep the `longhornio` account name.

## Checked

2026-11-04: read the source page(s) in full against every claim above: https://longhorn.io/docs/1.13.0/deploy/install/airgap/

No claim needed changing.

Method: documentation only; no commands were run.
