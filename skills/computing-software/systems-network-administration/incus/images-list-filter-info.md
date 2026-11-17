---
id: computing-software.systems-network-administration.incus.images-list-filter-info
name: images-list-filter-info
category: computing-software
field: systems-network-administration
product: incus
tags: [incus, images, image-list, image-info, properties, image-edit, image-delete]
level: intro
status: docs-checked
description: "List and filter Incus images, show info and properties, edit properties, and delete images; properties do not change Incus behaviour."
sources:
  - https://raw.githubusercontent.com/lxc/incus/main/doc/howto/images_manage.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# List, inspect and delete images

```
incus image list [<remote>:]
incus image list images: debian arm64
incus image list images: debian architecture=x86_64
incus image info <image_ID>
incus image show <image_ID>
incus image get-property <image_ID> <key>
incus image set-property <image_ID> <key>
incus image edit <image_ID>
incus image delete <image_ID>
```

- Without a remote, the default remote is listed.
- Filters are alias/fingerprint text or `key=value` properties.
- For remote images include the remote, e.g. `images:debian/12`.
- Properties are informational; they "do not configure Incus' behavior in any way."
- Deleting does not affect running instances. Cached remote images are re-downloaded on next use; manually created images are gone.

## Checked

2026-11-09. Confirmed against the Incus doc howto/images_manage.md (List, Filter, View, Edit, Delete sections): commands, filter forms, default remote, properties note and delete behaviour. Removed: nothing needed removing.

Method: documentation only; no commands were run.
