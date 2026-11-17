---
id: computing-software.systems-network-administration.incus.image-aliases-export
name: image-aliases-export
category: computing-software
field: systems-network-administration
product: incus
tags: [incus, images, alias, image-export, air-gapped, vm-image]
level: practitioner
status: docs-checked
description: "Manage Incus image aliases (list, create, delete, rename, repoint by recreate) and export images, with --vm for VM images."
sources:
  - https://raw.githubusercontent.com/lxc/incus/main/doc/howto/images_manage.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Image aliases and export

```
incus image alias list
incus image alias create <alias> <fingerprint>
incus image alias delete <alias>
incus image alias rename <alias> <new_alias>
incus image export [<remote>:]<image> [<output_directory_path>]
incus image export [<remote>:]<image> --vm
```

- Aliases can also be set during copy, import or publish.
- Renaming does not repoint an alias. To point it at a different image, delete and recreate it.
- Export a container image by default; add `--vm` for the VM variant.
- Typical uses: backups and transfers to air-gapped environments. The file layout is described in the image-format reference.

## Checked

2026-11-09. Confirmed against the Incus doc howto/images_manage.md (Configure image aliases, Export an image to a file): alias commands, repoint by delete and recreate, export commands, --vm, use cases. Removed: nothing needed removing.

Method: documentation only; no commands were run.
