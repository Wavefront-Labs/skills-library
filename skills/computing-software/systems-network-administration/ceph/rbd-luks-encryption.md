---
id: computing-software.systems-network-administration.ceph.rbd-luks-encryption
name: rbd-luks-encryption
category: computing-software
field: systems-network-administration
product: ceph
tags: [ceph, rbd, encryption, luks, luks2, passphrase]
level: practitioner
status: docs-checked
description: "Format an RBD image with LUKS1 or LUKS2 encryption, work with clones, and map it with a passphrase file."
sources:
  - https://docs.ceph.com/en/latest/rbd/rbd-encryption/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Image-level encryption handled by RBD clients exists from the Pacific release. It is applied inside the image by formatting it:

```
rbd create --size 50G mypool/myimage
rbd encryption format [--cipher-alg {aes-128|aes-256}] mypool/myimage luks2 passphrase.bin
```

Formatting writes a LUKS header to the start of the image, with a single keyslot holding a randomly generated key protected by the passphrase. Any data written before formatting may become unreadable. The header makes the effective size smaller than the raw size, so grow the image afterwards, as the page does:

```
rbd resize --size 50G --encryption-passphrase-file passphrase.bin mypool/myimage
```

Map through NBD with the passphrase:

```
rbd device map -t nbd -o encryption-passphrase-file=passphrase.bin mypool/myimage
```

Clones: unless explicitly formatted, clones of an encrypted image use the same format and secret, and a clone of an encrypted image is always encrypted. A clone can be formatted with its own passphrase and format (`luks1` or `luks2`). To map or resize it, give the passphrase files starting with the clone's, then its parent's and so on up the hierarchy, repeating `--encryption-passphrase-file` (or `encryption-passphrase-file=` in `-o`).

Constraints from the page:

- The `krbd` kernel module does not support encryption; LUKS formats are supported on Linux-based systems only.
- Images with the journal feature enabled cannot be formatted and encrypted by RBD clients.
- Both LUKS1 and LUKS2 are supported, with AES-128 or AES-256 and `xts-plain64` the only mode. The default is AES-256.
- A formatted image is still treated as raw by RBD APIs, so raw I/O can damage the encryption metadata; an encryption load operation (done automatically by `rbd-nbd` mapping) is needed for safe encrypted I/O.
- Flattening or shrinking an explicitly formatted clone is not transparent; if encryption is not loaded first, previously accessible parent data may become unreadable.
- Adding or removing passphrases is not supported by RBD, but can be done on the raw data with tools such as `cryptsetup`.
- Writes smaller than or unaligned to a sector (4KiB default in LUKS2, 512 bytes in LUKS1) trigger a read-modify-write chain with a considerable latency penalty.

## Checked

Method: docs-only read of cited pages, 2026-11-08

Confirmed against "Image Encryption" on docs.ceph.com. Removed: the advice to keep the passphrase file outside the cluster and the "format only an empty image" phrasing (the page says earlier data may become unreadable).
