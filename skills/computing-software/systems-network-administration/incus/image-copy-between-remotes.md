---
id: computing-software.systems-network-administration.incus.image-copy-between-remotes
name: image-copy-between-remotes
category: computing-software
field: systems-network-administration
product: incus
tags: [incus, images, image-copy, auto-update, copy-aliases, remotes]
level: practitioner
status: docs-checked
description: "Copy Incus images between remotes or into the local store with incus image copy: --alias, --copy-aliases, --auto-update, --vm."
sources:
  - https://raw.githubusercontent.com/lxc/incus/main/doc/howto/images_copy.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Copy images

```
incus image copy [<source_remote>:]<image> <target_remote>:
incus image copy images:debian/12 local: --alias debian12 --auto-update
```

- Use `local:` as target to copy into your local image store.
- `--alias` assigns an alias to the copy; `--copy-aliases` carries the source's aliases.
- `--auto-update` keeps the copy in sync with the original.
- `--vm` picks the VM-capable variant when copying from an alias.
- Using a remote image directly at launch is usually simpler than copying.

## Checked

2026-11-09. Confirmed against the Incus doc howto/images_copy.md (Copy an image from a remote): command form, local: target note and the four flags. The example command combines documented flags. Removed: nothing needed removing.

Method: documentation only; no commands were run.
