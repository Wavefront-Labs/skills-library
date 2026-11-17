---
id: computing-software.cloud-infrastructure-engineering.longhorn.backing-images
name: backing-images
category: computing-software
field: cloud-infrastructure-engineering
product: longhorn
tags: [backing-image, source-type, checksum, min-copies, storageclass]
level: practitioner
status: docs-checked
description: "Create Longhorn backing images by download, UI upload or export-from-volume with the BackingImage CRD, checksums, copy counts and StorageClass parameters."
sources:
  - https://longhorn.io/docs/1.13.0/advanced-resources/backing-image/backing-image/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: provide a shared base image for new volumes.

`BackingImage` (`longhorn.io/v1beta2`) spec:
- `dataEngine`: `v1` or `v2`
- `sourceType`: `download` or `export-from-volume`; the Longhorn UI also offers upload, but the page advises against upload through YAML or a StorageClass
- `sourceParameters`: `url` for download; `volume-name` and `export-type` for export
- `checksum`: SHA512 of the whole file
- `minNumberOfCopies`: copies to keep in the cluster
- `nodeSelector`, `diskSelector`: where files are stored

```yaml
apiVersion: longhorn.io/v1beta2
kind: BackingImage
metadata:
  name: bi-download
  namespace: longhorn-system
spec:
  dataEngine: v1
  minNumberOfCopies: 2
  sourceType: download
  sourceParameters:
    url: <URL>
  checksum: <SHA512>
```

StorageClass (`provisioner: driver.longhorn.io`): `backingImage`, `backingImageDataSourceType` (`download` or `export-from-volume`), `backingImageDataSourceParameters` (JSON string such as `'{"url": "<URL>"}'`), `backingImageChecksum`, `backingImageMinNumberOfCopies`, `backingImageNodeSelector`, `backingImageDiskSelector`, `dataEngine`. A PVC using it creates the image if absent; Longhorn prepares it on replica disks when a volume using it attaches.

Notes:
- Image size must be a multiple of 512 bytes.
- Provide the expected checksum at creation; otherwise Longhorn treats the first file it gets as correct.
- A backing image can be deleted only when no volume uses it.
- V2 backing images cannot be downloaded locally, exported from V2 volumes, cloned or backed up.
- Page conflicts: the backing-image prose says `backingImageName` while its examples use `backingImage`; this skill follows the examples. The backing-image page documents V2 backing images, but the CSI volume clone page calls them deprecated.

## Checked

2026-11-04: read the source page(s) in full against every claim above: https://longhorn.io/docs/1.13.0/advanced-resources/backing-image/backing-image/

Changed: upload wording softened (UI offers it; page advises against YAML or StorageClass upload). Added two page conflicts (backingImageName vs backingImage; V2 backing images documented here but called deprecated on the CSI volume clone page).

Method: documentation only; no commands were run.
