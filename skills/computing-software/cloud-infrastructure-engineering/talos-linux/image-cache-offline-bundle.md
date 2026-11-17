---
id: computing-software.cloud-infrastructure-engineering.talos-linux.image-cache-offline-bundle
name: image-cache-offline-bundle
category: computing-software
field: cloud-infrastructure-engineering
product: talos-linux
tags: [image-cache, imagecacheconfig, air-gapped, volumeconfig, imager, registryd]
level: advanced
status: docs-checked
description: "Build and enable the Talos local image cache: cache-create, imager --image-cache for ISO or disk, ImageCacheConfig, IMAGECACHE volume sizing, live updates, troubleshooting."
sources:
  - https://github.com/siderolabs/docs/blob/main/public/talos/v1.15/configure-your-talos-cluster/images-container-runtime/image-cache.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The image cache lets a node use container images without Internet access. It is per machine and managed by Talos once enabled.

Prepare the image list and OCI cache:

```bash
talosctl images k8s-bundle > images.txt
cat extra-images.txt >> images.txt
cat images.txt | talosctl images cache-create --image-cache-path ./image-cache.oci --images=-
```

For air gaps add Talos images (`talosctl images talos-bundle <version> >> images.txt`, 1.12+); the minimum are `installer` and `installer-base`. `--layer-cache` speeds repeated runs.

Bundle with imager: `... iso --image-cache /image-cache.oci` for an ISO, or `metal --image-cache /image-cache.oci` for a disk image (the `IMAGECACHE` partition is sized at the cache plus 20%). Ventoy is not supported.

Enable explicitly:

```yaml
apiVersion: v1alpha1
kind: ImageCacheConfig
local:
  enabled: true
```

With an ISO, size the volume so the cache is copied to disk (defaults: `minSize: 500MB`, `maxSize: 1GB`, system disk):

```yaml
apiVersion: v1alpha1
kind: VolumeConfig
name: IMAGECACHE
provisioning:
  diskSelector:
    match: 'system_disk'
  minSize: 2GB
  maxSize: 2GB
```

Refresh a live node by attaching new cache media; it is mounted and copied to `IMAGECACHE`. Only baked-in images are copied; for dynamic content use a registry mirror.

Boot blocks with `task install (1/1): waiting for the image cache` until available. Check `talosctl get imagecacheconfig -o yaml` (`status`, `copyStatus`, `roots`) and `talosctl logs registryd` for hits and misses.

## Checked

2026-11-04. Cache build commands, imager flags, ImageCacheConfig, IMAGECACHE defaults, live update limits and diagnostics confirmed on the Image Cache page.

Method: documentation only; no commands were run.
