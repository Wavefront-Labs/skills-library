---
id: computing-software.systems-network-administration.incus.image-import-files-and-urls
name: image-import-files-and-urls
category: computing-software
field: systems-network-administration
product: incus
tags: [incus, images, image-import, unified-image, split-image, http-headers, incus-image-hash]
level: advanced
status: docs-checked
description: "Import Incus images from unified or split files on disk or from a URL, including the Incus-Image-Hash and Incus-Image-URL headers."
sources:
  - https://raw.githubusercontent.com/lxc/incus/main/doc/howto/images_copy.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Import images

Files must follow the image format (from an export, distrobuilder, or a downloaded remote image).

```
incus image import <file_or_directory> [<target_remote>:]
incus image import <metadata_tarball> <rootfs_tarball> [<target_remote>:]
incus image import <URL>
```

- Unified image: one compressed file or a directory. Split image: metadata tarball plus rootfs tarball.
- `--alias` assigns a local alias in each case.
- URL import works against a plain web server, which must send custom headers: `Incus-Image-Hash` (SHA256 of the image) and `Incus-Image-URL` (download URL).
- Incus sends `Incus-Server-Architectures` (comma-separated) and `Incus-Server-Version` when querying.
- URL imports need unified images.

## Checked

2026-11-09. Confirmed against the Incus doc howto/images_copy.md (Import an image from files): import commands, unified and split formats, --alias, required and sent headers. Added: URL imports need unified images, which the page states. Removed: nothing else.

Method: documentation only; no commands were run.
