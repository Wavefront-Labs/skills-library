---
id: computing-software.cloud-infrastructure-engineering.k3s.k3s-conditional-image-import
name: k3s-conditional-image-import
category: computing-software
field: cloud-infrastructure-engineering
product: k3s
tags: [k3s, cache-json, image-import, startup-time]
level: advanced
status: docs-checked
description: "Skip re-importing unchanged image tarballs at K3s startup with a .cache.json file in the images directory."
sources:
  - https://docs.k3s.io/add-ons/import-images
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: reduce startup delay caused by image archives.

By default K3s imports image archives every time it starts, so images are consistently available even if some were removed or pruned. The kubelet is not started until all archives have been processed, which delays startup.

To import only tarballs that changed since they were last imported, even across restarts, create the cache file:

```
touch /var/lib/rancher/k3s/agent/images/.cache.json
```

The cache file stores archive metadata as files are processed. Later restarts do not re-import an archive as long as its size and modification time stay the same.

Warning from the docs: with this enabled, K3s cannot ensure all images are available at every start. If an image was removed or pruned since the last start, reimport it manually by doing one of:

- import the archive with `ctr image import`;
- `touch` the archive to change its timestamp;
- clear the contents of .cache.json and restart K3s.

Pre-importing images is also essential when imagePullPolicy is Never. With the default IfNotPresent policy, containerd pulls on demand from upstream or your private registry with no extra configuration.

## Checked

2026-11-08. Read the full K3s Import Images page (docs/add-ons/import-images.md in the k3s-io/docs repo). Confirmed: default import on every start, kubelet delayed until archives are processed, the .cache.json file, size and modification time criteria, the three manual reimport options, imagePullPolicy Never, and IfNotPresent on-demand pulls. Nothing removed.

Method: documentation only; no commands were run.
